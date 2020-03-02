from collections import OrderedDict

from cglue.function import FunctionPrototype, FunctionImplementation
from cglue.ports import PortType
from cglue.cglue import Plugin, CGlue
from cglue.signal import SignalConnection, SignalType
from cglue.component import Component
from cglue.data_types import TypeCollection


def collect_arguments(attributes, consumer_name, consumer_arguments, caller_args, manual_args=None):
    user_arguments = attributes.get('arguments', {})
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
                raise Exception(f'Caller of {consumer_name} has matching '
                                f'argument {arg_name} but types are different')
            passed_arguments[arg_name] = arg_name
        else:
            raise Exception(f'Unable to connect argument {arg_name} of {consumer_name}')

    return passed_arguments


class EventSignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple')

    def generate_consumer(self, context, connection: SignalConnection, consumer_name, attributes):
        caller_fn = context.get_port(connection.provider).functions['run']
        fn_to_call = context.get_port(consumer_name).functions['run']

        manual_args = {}
        consumer_component_name = consumer_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_name]
        consumer_component = consumer_instance.component
        if consumer_component.config['multiple_instances']:
            manual_args['instance'] = f'&{consumer_instance.instance_var_name}'

        passed_arguments = collect_arguments(attributes, consumer_name,
                                             fn_to_call.arguments, caller_fn.arguments, manual_args)

        call_code = fn_to_call.generate_call(passed_arguments)

        return {
            connection.provider: {
                'run': {
                    'body': call_code + ';',
                    'used_arguments': passed_arguments.keys()
                },
                'write': {
                    'body': call_code + ';',
                    'used_arguments': passed_arguments.keys()
                }
            }
        }


class ServerCallSignal(SignalType):
    def __init__(self):
        super().__init__(consumers='multiple')

    def generate_consumer(self, context, connection: SignalConnection, consumer_name, attributes):
        consumer_port_data = context.get_port(consumer_name)
        caller_fn = consumer_port_data.functions['run']
        fn_to_call = context.get_port(connection.provider).functions['run']

        manual_args = {}
        consumer_component_name = consumer_name.split('/', 2)[0]
        consumer_instance = context['component_instances'][consumer_component_name]
        consumer_component = consumer_instance.component
        if consumer_component.config['multiple_instances']:
            manual_args['instance'] = f'&{consumer_instance.instance_var_name}'

        passed_arguments = collect_arguments(attributes, consumer_name,
                                             fn_to_call.arguments, caller_fn.arguments, manual_args)

        call_code = fn_to_call.generate_call(passed_arguments)

        if caller_fn.return_type == 'void':
            return {
                consumer_name: {
                    'run': {
                        'body': call_code + ';',
                        'used_arguments': passed_arguments.keys()
                    }
                }
            }

        else:
            if caller_fn.return_type != fn_to_call.return_type:
                raise Exception(f'Callee return type is incompatible ({consumer_port_data["return_type"]} '
                                f'instead of {caller_fn.return_type})')

            return {
                consumer_name: {
                    'run': {
                        'body':             f"{consumer_port_data['return_type']} return_value = {call_code};",
                        'used_arguments':   passed_arguments.keys(),
                        'return_statement': 'return_value'
                    }
                }
            }


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

        function = FunctionPrototype(fn_name, port['return_type'])

        for name, arg_data in port.get('arguments', {}).items():
            if type(arg_data) is str:
                function.arguments.add(name, 'in', self._types.get(arg_data))
            else:
                function.arguments.add(name, arg_data['direction'], self._types.get(arg_data['data_type']))

        return {'run': function}

    def create_component_functions(self, port):
        prototype = port.functions['run']

        function = FunctionImplementation(prototype)

        for arg in function.arguments:
            function.mark_argument_used(arg)

        return {'run': function}

    def create_runtime_functions(self, port):
        return {}


def _create_callee_function(port, types, fn_name, return_type):
    function = FunctionPrototype(fn_name, return_type)

    for name, arg_data in port.get('arguments', {}).items():
        if type(arg_data) is str:
            function.arguments.add(name, 'in', types.get(arg_data))
        else:
            function.arguments.add(name, arg_data['direction'], types.get(arg_data['data_type']))

    return {'run': function}


class EventPortType(PortType):
    def __init__(self, types):
        super().__init__(types, {
            'order':          1,
            'provides':       {'event'},
            'def_attributes': {
                'required': [],
                'optional': {'arguments': {}},
                'static':   {'return_type': 'void'}
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
                    'arguments':   {}
                },
                'static':   {}
            }
        })

    def declare_functions(self, port):
        fn_name = f'{port.component_name}_Call_{port.port_name}'
        return _create_callee_function(port, self._types, fn_name, port['return_type'])

    def create_component_functions(self, port):
        prototype = port.functions['run']

        function = FunctionImplementation(prototype)
        function.attributes.add('weak')

        if function.return_type != 'void':
            function_return_type = self._types.get(port['return_type'])
            return_value = function_return_type.render_value(port.get('return_value'))
            function.set_return_statement(return_value)

        return {'run': function}

    def create_runtime_functions(self, port):
        function = FunctionImplementation(port.functions['run'])

        return {'run': function}


def create_port_ref(port):
    if type(port) is str:
        parts = port.split('/')
        return {
            'short_name': port,
            'component':  parts[0],
            'port':       parts[1]
        }
    elif type(port) is dict:
        return {
            'short_name': port['short_name'],
            'component':  port['component'],
            'port':       port.get('runnable') or port.get('port')
        }
    else:
        raise TypeError("port must either be a dict or a str")


def expand_runtime_events(owner: CGlue, project_config):
    runtime_config = project_config['runtime']
    runtime_component = Component.create_empty_config('Runtime')
    runtime_component['source_files'] = []

    runtime_runnables = runtime_config['runnables']

    runtime_component['ports'] = {event: {'port_type': 'Event'} for event in runtime_runnables}
    event_connections = [{
            'provider': create_port_ref(f'Runtime/{event}'),
            'consumers': handlers
        } for event, handlers in runtime_runnables.items()]

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
    instance_type_name = f'{component.name}_Instance_t'

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

            if 'instance' in runnable_data['arguments']:
                if runnable_data['arguments']['instance']['data_type'] != instance_type_name:
                    instance_type = runnable_data["arguments"]["instance"]["data_type"]
                    raise TypeError(f'Runnable has argument named "instance" but '
                                    f'its type ({instance_type.name}) '
                                    f'does not match instance type')
            else:
                args['instance'] = {
                    'data_type': instance_type_name,
                    'direction': 'inout'
                }

            if 'arguments' in runnable_data:
                args.update(runnable_data['arguments'])

            runnable_data['arguments'] = args

        component.config['ports'][runnable_name] = {
            'port_type': 'Runnable',
            **runnable_data
        }


def add_exported_declarations(owner: CGlue, context):
    runtime_funcs = [short_name for short_name in context['functions'] if short_name.startswith('Runtime/')]
    context['exported_function_declarations'] += runtime_funcs

    sort_functions(owner, context)


def sort_functions(owner: CGlue, context):
    def sort_by_port_type(fn):
        if fn.startswith('Runtime/'):
            weight = 0
        else:
            weight = context.get_port(fn).port_type.config.get('order', 3)

        return weight

    by_port_type = sorted(context['functions'], key=sort_by_port_type)
    context['functions'] = {fn: context['functions'][fn] for fn in by_port_type}


def remove_runtime_component(owner: CGlue, config):
    del owner._components['Runtime']
    port_connections = []
    for connection in config['runtime']['port_connections']:
        provider = connection['provider']
        if type(provider) is str:
            if not provider.startswith('Runtime/'):
                port_connections.append(connection)
        else:
            if provider['component'] != 'Runtime':
                port_connections.append(connection)

    config['runtime']['port_connections'] = port_connections


def cleanup_component(owner: CGlue, component_name, ctx):
    # remove automatically generated runnable ports
    component_data = owner._components[component_name]
    component_data['ports'] = {name: port for name, port in component_data['ports'].items() if
                               name not in component_data['runnables']}

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
