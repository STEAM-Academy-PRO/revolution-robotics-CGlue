from collections import OrderedDict

from cglue.function import FunctionImplementation
from cglue.ports import PortType
from cglue.cglue import Plugin, CGlue
from cglue.signal import SignalConnection, SignalType
from cglue.component import Component
from cglue.data_types import TypeCollection
from cglue.utils.common import indent
from cglue.utils.multiple_instance_helpers import add_instance_check, get_instance_argument


def collect_arguments(attributes, consumer_name, consumer_arguments, caller_args, manual_args=None):
    user_arguments = attributes['arguments']
    if manual_args is None:
        manual_args = {}

    for arg in user_arguments:
        if arg not in consumer_arguments:
            print(f"Warning: Runnable {consumer_name} does not have an argument named '{arg}'")

    passed_arguments = {}
    for arg_name, arg_type in consumer_arguments.items():
        if arg_name in user_arguments:
            passed_arguments[arg_name] = user_arguments[arg_name]

        elif arg_name in manual_args:
            passed_arguments[arg_name] = manual_args[arg_name]

        elif arg_name in caller_args:
            if arg_type != caller_args[arg_name]:
                raise Exception(f'Caller of {consumer_name} has matching argument {arg_name} but types are different')
            passed_arguments[arg_name] = arg_name
        else:
            raise Exception(f'Unable to connect argument {arg_name} of {consumer_name}')

    return passed_arguments


class EventSignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple', attributes={
            'required': {},
            'optional': {
                'arguments': {}
            }
        })

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        caller_fn = context.get_port(connection.provider).functions['run']
        fn_to_call = context.get_port(consumer_instance_name).functions['run']

        manual_args = {}
        consumer_instance = context.get_component_instance(consumer_instance_name)
        provider_instance = context.get_component_instance(connection.provider)

        callee_instance_arg_name = get_instance_argument(list(fn_to_call.arguments.keys()), consumer_instance)
        if callee_instance_arg_name:
            manual_args[callee_instance_arg_name] = '&' + consumer_instance.instance_var_name

        caller_args = caller_fn.arguments.copy()
        passed_arguments = collect_arguments(attributes, consumer_instance_name,
                                             fn_to_call.arguments, caller_args, manual_args)

        provider_port_name = context.get_component_ref(connection.provider)
        body = fn_to_call.generate_call(passed_arguments) + ';'

        used_args = list(passed_arguments.keys())

        instance_arg_name = get_instance_argument(list(caller_args.keys()), provider_instance)
        if instance_arg_name:
            used_args.append(instance_arg_name)
            body = add_instance_check(body, provider_instance, instance_arg_name=instance_arg_name)

        return {
            provider_port_name: {
                'run': {
                    'body': body,
                    'used_arguments': used_args
                },
                'write': {
                    'body': body,
                    'used_arguments': used_args
                }
            }
        }


class ServerCallSignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple', attributes={
            'required': {},
            'optional': {
                'conditions': {},
                'arguments': {}
            }
        })

    def generate_consumer(self, context, connection: SignalConnection, consumer_instance_name, attributes):
        consumer_port_data = context.get_port(consumer_instance_name)
        caller_fn = consumer_port_data.functions['run']
        fn_to_call = context.get_port(connection.provider).functions['run']

        manual_args = {}
        consumer_instance = context.get_component_instance(consumer_instance_name)
        provider_instance = context.get_component_instance(connection.provider)

        instance_arg_name = get_instance_argument(list(caller_fn.arguments.keys()), consumer_instance)

        provider_instance_arg_name = get_instance_argument(list(fn_to_call.arguments.keys()), provider_instance)
        if provider_instance_arg_name:
            manual_args[provider_instance_arg_name] = '&' + provider_instance.instance_var_name

        passed_arguments = collect_arguments(attributes, consumer_instance_name,
                                             fn_to_call.arguments, caller_fn.arguments, manual_args)

        consumer_port_name = context.get_component_ref(consumer_instance_name)

        return_statement = None
        if caller_fn.return_type != 'void':
            if caller_fn.return_type != fn_to_call.return_type:
                raise Exception(f'Callee return type is incompatible ({consumer_port_data["return_type"]} '
                                f'instead of {caller_fn.return_type})')

            body = f"return {fn_to_call.generate_call(passed_arguments)};"
            if provider_instance_arg_name:
                return_statement = context.types.get(caller_fn.return_type).render_value(None)
        else:
            body = fn_to_call.generate_call(passed_arguments) + ';'

        if attributes['conditions']:
            used_args = [*passed_arguments.keys(), *attributes['conditions'].keys()]
            conditions = (f'{arg} == {value}' for arg, value in attributes['conditions'].items())
            body = f'if ({" && ".join(conditions)})\n' \
                   f'{{\n' \
                   f'{indent(body)}\n' \
                   f'}}'
        else:
            used_args = passed_arguments.keys()

        if instance_arg_name:
            body = add_instance_check(body, consumer_instance, instance_arg_name=instance_arg_name)

        mod = {
            'body': body,
            'used_arguments': used_args
        }
        if return_statement:
            mod['return_statement'] = return_statement

        return {
            consumer_port_name: {
                'run': mod
            }
        }


def _create_callee_function(port, types: TypeCollection, fn_name, return_type):
    args = {}
    for name, arg_data in port['arguments'].items():
        if type(arg_data) is str:
            args[name] = types.get(arg_data)
        else:
            args[name] = {
                'direction': arg_data['direction'],
                'data_type': types.get(arg_data['data_type'])
            }

    function = port.declare_function(fn_name, return_type, args)

    return {'run': function}


class RunnablePortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order':          0,
            'consumes':       {'event': 'multiple'},
            'provides': {'call'},
            'def_attributes': {
                'required': [],
                'optional': {'arguments': {}, 'return_type': 'void'},
                'static':   {}
            }
        })

    def declare_functions(self, port):
        fn_name = f'{port.component_name}_Run_{port.port_name}'
        return _create_callee_function(port, self._types, fn_name, port['return_type'])

    def create_component_functions(self, port):
        function = FunctionImplementation(port.functions['run'])

        for arg in function.arguments:
            function.mark_argument_used(arg)

        return {'run': function}

    def create_runtime_functions(self, port):
        return {}


class EventPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order':          1,
            'provides':       {'event'},
            'def_attributes': {
                'required': [],
                'optional': {'arguments': {}},
                'static':   {}
            }
        })

    def declare_functions(self, port):
        fn_name = f'{port.component_name}_RaiseEvent_{port.port_name}'
        return _create_callee_function(port, self._types, fn_name, 'void')

    def create_component_functions(self, port):
        function = FunctionImplementation(port.functions['run'])
        function.attributes.add('weak')

        return {'run': function}

    def create_runtime_functions(self, port):
        function = FunctionImplementation(port.functions['run'])

        return {'run': function}


class ServerCallPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order':          2,
            'consumes':       {'call': 'multiple'},
            'def_attributes': {
                'required': [],
                'optional': {
                    'return_type': 'void',
                    'return_value': None,
                    'arguments':   {}
                },
                'static':   {}
            }
        })

    def declare_functions(self, port):
        fn_name = f'{port.component_name}_Call_{port.port_name}'
        return _create_callee_function(port, self._types, fn_name, port['return_type'])

    def create_component_functions(self, port):
        function = FunctionImplementation(port.functions['run'])
        function.attributes.add('weak')

        if function.return_type != 'void':
            function_return_type = self._types.get(function.return_type)
            return_value = function_return_type.render_value(port['return_value'])
            function.set_return_statement(return_value)

        return {'run': function}

    def create_runtime_functions(self, port):
        function = FunctionImplementation(port.functions['run'])

        return {'run': function}


def expand_runtime_events(owner: CGlue, project_config):
    runtime_config = project_config['runtime']
    runtime_component = Component.create_empty_config('Runtime')
    runtime_component['source_files'] = []

    runtime_runnables = runtime_config['runnables']

    runtime_component['ports'] = {event: {'port_type': 'Event'} for event in runtime_runnables}
    event_connections = ({
            'provider': {
                'short_name': f'Runtime/{event}',
                'component':  'Runtime',
                'port':       event
            },
            'consumers': handlers
        } for event, handlers in runtime_runnables.items())

    owner.add_component(Component('Runtime', runtime_component, owner.types))
    runtime_config['port_connections'] += event_connections


known_port_types = {
    'Runnable': RunnablePortType,
    'Event': EventPortType,
    'ServerCall': ServerCallPortType,
}


def init(owner: CGlue):
    add_event_to = ['WriteData', 'WriteIndexedData']
    for port_type, port_type_data in owner.port_types.items():
        if port_type in add_event_to:
            port_type_data['provides'].add('event')

    owner.add_signal_type('event', EventSignal())
    owner.add_signal_type('call', ServerCallSignal())

    for port_type_name, port_type_class in known_port_types.items():
        owner.add_port_type(port_type_name, port_type_class(owner.types))


def create_runnable_ports(owner: CGlue, component: Component):
    for runnable_name, runnable_data in component.config['runnables'].items():
        if type(runnable_data) is str:
            type_data = owner.types.get(runnable_data)
            if type_data.category.name != TypeCollection.FUNC_PTR:
                raise ValueError('Runnable config must either be an object or the name of a function pointer type')
            runnable_data = {
                'return_type': type_data.data['return_type'],
                'arguments': type_data.data['arguments']
            }

        if component.config['multiple_instances']:
            args = OrderedDict()

            runnable_arguments = runnable_data.get('arguments', {})
            if 'instance' in runnable_arguments:
                instance_type = runnable_arguments["instance"]["data_type"]
                if instance_type != component.instance_type:
                    raise TypeError(f'Runnable has argument named "instance" but '
                                    f'its type ({instance_type.name}) does not match instance type')
            else:
                args['instance'] = {
                    'data_type': component.instance_type,
                    'direction': 'inout'
                }

            args.update(runnable_arguments)
            runnable_data['arguments'] = args

        component.config['ports'][runnable_name] = {
            'port_type': 'Runnable',
            **runnable_data
        }


def add_exported_declarations(owner: CGlue, context):
    context['exported_function_declarations'] += (short_name
                                                  for short_name in context['functions']
                                                  if short_name.startswith('Runtime/'))

    sort_functions(owner, context)


def sort_functions(owner: CGlue, context):
    def sort_by_port_type(fn):
        if fn.startswith('Runtime/'):
            weight = 0
        else:
            if type(context) is dict:
                port = owner.get_port(fn)
            else:
                try:
                    port = context.get_port(fn)
                except KeyError:
                    port = owner.get_port(fn)
            weight = port.port_type.config.get('order', 3)

        return weight

    by_port_type = sorted(context['functions'], key=sort_by_port_type)
    context['functions'] = {fn: context['functions'][fn] for fn in by_port_type}


def remove_runtime_component(owner: CGlue, config):
    del owner._components['Runtime']

    def is_provided_by_runtime(connection):
        provider = connection['provider']
        if type(provider) is str:
            return provider.startswith('Runtime/')
        else:
            return provider['component'] == 'Runtime'

    config['runtime']['port_connections'] = (connection
                                             for connection in config['runtime']['port_connections']
                                             if not is_provided_by_runtime(connection))


def cleanup_component(owner: CGlue, component_name, ctx):
    # remove automatically generated runnable ports
    component_data = owner._components[component_name]
    component_data['ports'] = {name: port
                               for name, port in component_data['ports'].items()
                               if name not in component_data['runnables']}

    sort_functions(owner, ctx)


def runtime_events():
    """Plugin that provides support for simple runtime event creation and configuration"""
    return Plugin("RuntimeEvents", {
        'init':                        init,
        'load_component_config':       create_runnable_ports,
        'project_config_loaded':       expand_runtime_events,
        'before_generating_component': cleanup_component,
        'before_generating_runtime':   add_exported_declarations,
        'save_project_config':         remove_runtime_component
    }, requires=['BuiltinDataTypes'])
