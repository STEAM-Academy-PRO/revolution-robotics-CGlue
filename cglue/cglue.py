import json
import os
from collections import defaultdict
from contextlib import suppress
from typing import Iterable

import chevron

from cglue.component import Component, ComponentCollection, ComponentInstanceCollection
from cglue.utils.common import to_underscore
from cglue.signal import SignalType
from cglue.data_types import TypeCollection, TypeWrapper

runtime_header_template = """#ifndef GENERATED_RUNTIME_H_
#define GENERATED_RUNTIME_H_

{{# type_includes }}
#include {{{ . }}}
{{/ type_includes }}

{{# types }}
{{{ . }}}
{{/ types }}

{{# components }}
#define COMPONENT_TYPES_{{ guard_def }}_H_
{{/ components }}

{{# components }}
#include "{{ components_dir }}/{{ name }}/{{ name }}.h"
{{/ components }}

{{# function_declarations }}
{{{ . }}};
{{/ function_declarations }}

#endif /* GENERATED_RUNTIME_H */
"""

component_header_template = '''#ifndef COMPONENT_{{ guard_def }}_H_
#define COMPONENT_{{ guard_def }}_H_

#ifndef COMPONENT_TYPES_{{ guard_def }}_H_
#define COMPONENT_TYPES_{{ guard_def }}_H_

{{# type_includes }}
#include {{{ . }}}
{{/ type_includes }}

{{# types }}
{{{ . }}}
{{/ types }}

#endif /* COMPONENT_TYPES_{{ guard_def }}_H_ */

{{# function_headers }}
{{{ . }}};
{{/ function_headers }}

#endif /* COMPONENT_{{ guard_def }}_H_ */
'''

source_template = '''{{# includes }}
#include {{{ . }}}
{{/ includes }}

{{# variables }}
{{{ . }}}
{{/ variables }}
{{# functions }}

{{{ . }}}{{/ functions }}'''


class Plugin:
    def __init__(self, name, handlers: dict, requires: list = None):
        self.name = name
        self._event_handlers = handlers
        self._owner = None
        self._requires = requires or []

    def bind(self, owner):
        for plugin in self._requires:
            if plugin not in owner._plugins:
                raise Exception(f'{self.name} requires unloaded plugin {plugin}')
        self._owner = owner

    def handle(self, event_name, args):
        try:
            handler = self._event_handlers[event_name]
        except KeyError:
            return

        print(f'Running {self.name}::{event_name}')
        handler(self._owner, *args)


class RuntimeGeneratorContext:
    def __init__(self, owner):
        self._owner = owner
        self._context = {
            'runtime': owner,
            'files': {},
            'functions': {},
            'declarations': [],
            'exported_function_declarations': [],
            'runtime_includes': {'"utils.h"'},
            'signals': defaultdict(lambda: defaultdict(list)),
            'used_types': []
        }
        self.component_instances = ComponentInstanceCollection()

    def __getitem__(self, item):
        return self._context[item]

    def __setitem__(self, key, value):
        self._context[key] = value

    @property
    def types(self):
        return self._owner.types

    @property
    def functions(self):
        return self._owner.functions

    def get_port(self, short_name):
        return self._owner.get_port(self.get_component_ref(short_name))

    def _split(self, short_name):
        component_name, port_name = short_name.split('/', 2)
        return self.component_instances[component_name], port_name

    def get_component_ref(self, short_name):
        component, port_name = self._split(short_name)
        return f'{component.component.name}/{port_name}'

    def get_component_instance(self, port_short_name):
        component, port = self._split(port_short_name)
        return component


class CGlue:
    def __init__(self, project_config_file):
        self._project_config_file = project_config_file
        self._basedir = os.path.dirname(project_config_file) or '.'
        self._plugins = {}
        self._project_config = {}
        self._components = ComponentCollection()
        self._types = TypeCollection()
        self._port_types = {}
        self._signal_types = {}
        self._functions = {}
        self._ports = {}

        self._print_warnings = ['unconnected_signals']

    def add_plugin(self, plugin: Plugin):
        self._plugins[plugin.name] = plugin
        plugin.bind(self)

    def load(self):
        self.raise_event('init')

        with open(self._project_config_file, "r") as file:
            project_config = json.load(file)

        self.raise_event('load_project_config', project_config)

        if 'settings' not in project_config:
            project_config['settings'] = {
                'name': 'Project Name',
                'components_folder': 'components',
                'required_plugins': []
            }

        print(f"Loaded configuration for {project_config['settings']['name']}")

        self._project_config = project_config

        for plugin_name in self.settings['required_plugins']:
            if plugin_name not in self._plugins:
                raise Exception(f'Project requires {plugin_name} plugin, which is not loaded')

        for component_name in project_config['components']:
            self._load_component_config(component_name)

        self.raise_event('project_config_loaded', project_config)

    def add_port_type(self, port_type_name, port_type):
        self._port_types[port_type_name] = port_type

    def _component_dir(self, component_name):
        return f'{self._basedir}/{self.settings["components_folder"]}/{component_name}'

    def _load_component_config(self, component_name):
        if component_name not in self._components:
            component_config_file = f'{self._component_dir(component_name)}/config.json'
            with open(component_config_file, "r") as file:
                component_config = json.load(file)
            self.add_component(Component(component_name, component_config, self.types))

    def add_component(self, component: Component):
        if component.name not in self._components:
            self._components.add(component)

            for dependency in component.dependencies:
                self._load_component_config(dependency)

            self.raise_event('load_component_config', component)
            if not component.config['ports']:
                print(f'Warning: {component.name} has no ports')

            for port_name, port_data in component.config['ports'].items():
                port_type = self._port_types[port_data['port_type']]
                processed_port = port_type.process_port(component, port_name, port_data)

                self._ports[processed_port.full_name] = processed_port

    @staticmethod
    def _get_type_includes(types: Iterable[TypeWrapper]):
        for type_wrapper in types:
            with suppress(KeyError):
                yield type_wrapper.get_attribute('defined_in')

    def _sort_types_by_dependency(self, type_objects, visited_types=None):
        if visited_types is None:
            visited_types = set()

        for type_obj in type_objects:
            if type_obj not in visited_types:
                try:
                    visited_types.add(type_obj)

                    dependencies = self.types.collect_type_dependencies(type_obj)
                    yield from self._sort_types_by_dependency(dependencies, visited_types)

                    yield type_obj
                except Exception:
                    print(f'Failed to process dependencies of {type_obj}')
                    raise

    def update_component(self, component_name):

        self._components.check_dependencies()

        component_folder = self._component_dir(component_name)
        source_file = f'{component_folder}/{component_name}.c'
        header_file = f'{component_folder}/{component_name}.h'
        config_file = f'{component_folder}/config.json'

        component_object = self._components[component_name]
        port_short_names = (f'{component_name}/{port_name}' for port_name in component_object.config['ports'])

        context = {
            'runtime': self,
            'component_folder': component_folder,
            'declarations': [],
            'files': {
                config_file: '',
                source_file: '',
                header_file: ''
            },
            'folders': [component_name],
            'functions': {short_name: self._ports[short_name].create_component_functions()
                          for short_name in port_short_names}
        }

        self.raise_event('before_generating_component', component_name, context)

        function_headers = []
        function_implementations = []
        includes = {
            f'"{component_name}.h"',
            '"utils.h"'
        }

        type_names = list(component_object.config['types'].keys())
        for c in component_object.dependencies:
            type_names += self._components[c]['types'].keys()

        for functions in context['functions'].values():
            for func in functions.values():
                function_headers.append(func.get_header())
                function_implementations.append(func.get_function())
                type_names += func.referenced_types
                includes.update(func.includes)

        sorted_type_objects = list(self._sort_types_by_dependency(self.types.get(type_names)))
        type_includes = set(self._get_type_includes(sorted_type_objects))
        typedefs = [t.render_typedef() for t in sorted_type_objects]

        ctx = {
            'includes': sorted(includes),
            'component_name': component_name,
            'guard_def': to_underscore(component_name).upper(),
            'variables': context['declarations'],
            'types': typedefs,
            'type_includes': sorted(type_includes),
            'functions': function_implementations,
            'function_headers': function_headers
        }

        context['files'][config_file] = self.dump_component_config(component_name)
        context['files'][source_file] = chevron.render(source_template, ctx)
        context['files'][header_file] = chevron.render(component_header_template, ctx)

        self.raise_event('generating_component', component_name, context)

        return context['files']

    def add_signal_type(self, name, signal_type: SignalType):
        self._signal_types[name] = signal_type

    def get_port(self, short_name):
        return self._ports[short_name]

    def get_project_structure(self):
        context = RuntimeGeneratorContext(self)

        self._components.check_dependencies()
        self._create_component_instances(context)

        port_functions = {name: port.create_runtime_functions() for name, port in self._ports.items()}
        self._functions.update(port_functions)

        for connection in self._project_config['runtime']['port_connections']:
            provider_name, port, attributes, all_signals = self._process_provider_port(context, connection)

            signals = defaultdict(list)

            for consumer_ref in connection['consumers']:
                self._process_consumer_ports(context, consumer_ref, port,
                                             attributes, provider_name, signals, all_signals)

            for signal_type, new_signals in signals.items():
                all_signals[signal_type] += new_signals

        return context

    def generate_runtime(self, filename):
        source_file_name = filename + '.c'
        header_file_name = filename + '.h'

        context = self.get_project_structure()

        context['files'][source_file_name] = ''
        context['files'][header_file_name] = ''

        self._generate_signals(context['signals'])

        if 'unconnected_signals' in self._print_warnings:
            for name, port in self._ports.items():
                if port.is_consumer and name not in context['functions']:
                    print(f'Warning: {name} port is not connected')

        self.raise_event('before_generating_runtime', context)

        type_names = context['used_types']
        for c in self._components:
            type_names += c['types'].keys()

        output_filename = os.path.basename(filename)
        includes = context['runtime_includes']
        includes.add(f'"{output_filename}.h"')

        function_headers = []
        function_implementations = []
        for port_name, funcs in context['functions'].items():
            export_functions = port_name in context['exported_function_declarations']
            for f in funcs.values():
                if export_functions:
                    function_headers.append(f.get_header())
                function_implementations.append(f.get_function())
                type_names += f.referenced_types
                includes.update(f.includes)

        sorted_type_objects = list(self._sort_types_by_dependency(self.types.get(type_names)))
        type_includes = set(self._get_type_includes(sorted_type_objects))
        typedefs = [t.render_typedef() for t in sorted_type_objects]

        instance_variables = [f'static {instance.component.instance_type} {instance.instance_var_name};'
                              for instance in context.component_instances
                              if instance.component.config['multiple_instances']]

        template_data = {
            'components_dir': self.settings['components_folder'],
            'includes': sorted(includes),
            'components': [
                {
                    'name': component.name,
                    'guard_def': to_underscore(component.name).upper()
                } for component in self._components if component.name != 'Runtime'],  # TODO
            'types': typedefs,
            'type_includes': sorted(type_includes),
            'function_declarations': function_headers,
            'functions':             function_implementations,
            'variables':             [*instance_variables, *context['declarations']]
        }

        context['files'][source_file_name] = chevron.render(source_template, template_data)
        context['files'][header_file_name] = chevron.render(runtime_header_template, template_data)

        self.raise_event('after_generating_runtime', context)

        return context['files']

    def _create_component_instances(self, context: RuntimeGeneratorContext):
        for component in self._components:
            if not component.config['multiple_instances']:
                context.component_instances.add(component.create_instance(component.name))

        for instance_name, component_name in self._project_config.get('instances', {}).items():
            component = self._components[component_name]
            context.component_instances.add(component.create_instance(instance_name))

    @staticmethod
    def _create_port_function(context, port):
        if port.full_name not in context['functions']:
            context['functions'][port.full_name] = port.create_runtime_functions()

    @staticmethod
    def _process_provider_port(context, connection):
        provider_ref = connection['provider']
        provider_short_name = provider_ref['short_name']

        provider_port = context.get_port(provider_short_name)
        provider_signals = context['signals'][provider_short_name]

        CGlue._create_port_function(context, provider_port)

        provider_attributes = {key: value for key, value in connection.items()
                               if key not in ('provider', 'consumer', 'consumers')}

        return provider_short_name, provider_port, provider_attributes, provider_signals

    @staticmethod
    def _generate_signals(sgnls):
        for signals in sgnls.values():
            for connections in signals.values():
                for connection in connections:
                    connection.generate()

    def _process_consumer_ports(self, context, consumer_ref, provider_port,
                                attrs, provider_name, provider_signals, all_signals):
        consumer_short_name = consumer_ref['short_name']
        consumer_port = context.get_port(consumer_short_name)

        # infer signal type
        consumed_signal_types = consumer_port.port_type['consumes']
        inferred_signal_type = provider_port.port_type['provides'].intersection(consumed_signal_types)

        if len(inferred_signal_type) == 1:
            signal_type_name = inferred_signal_type.pop()
        elif len(inferred_signal_type) == 0:
            raise Exception(f'Incompatible ports: {provider_port.full_name} and {consumer_port.full_name}')
        else:
            raise Exception("Connection type can't be inferred for " +
                            f"{provider_port.full_name} and {consumer_port.full_name}")

        signal_type = self._signal_types[signal_type_name]
        signals_of_current_type = provider_signals[signal_type_name]
        all_signals_of_current_type = all_signals[signal_type_name]

        # create consumer function
        self._create_port_function(context, consumer_port)

        def create_new_signal(new_signal_name):
            signals_of_current_type.append(
                signal_type.create_connection(context, new_signal_name, provider_name, attrs))

        # create signal connection
        signal_name = f'{provider_name}_{signal_type_name}'.replace('/', '_')

        if not signals_of_current_type:
            if all_signals_of_current_type:
                signal_name = f'{signal_name}{len(all_signals_of_current_type)}'

            create_new_signal(signal_name)
        else:
            if signal_type.consumers == 'multiple_signals':
                # create new signal in all cases
                create_new_signal(f'{signal_name}{len(all_signals_of_current_type)}')
            elif signal_type.consumers == 'single':
                raise Exception(f'Multiple consumers not allowed for {signal_type_name}'
                                f' signal (provided by {provider_port.full_name})')

        consumer_attributes = consumer_ref.get('attributes', {})
        signals_of_current_type[-1].add_consumer(consumer_short_name, consumer_attributes)

    def raise_event(self, event_name, *args):
        for plugin in self._plugins.values():
            try:
                plugin.handle(event_name, args)
            except Exception:
                print(f'Error while processing {plugin.name}::{event_name}')
                raise

    @property
    def functions(self):
        return self._functions

    @property
    def types(self):
        return self._types

    @property
    def port_types(self):
        return self._port_types

    @property
    def settings(self):
        return self._project_config['settings']

    def dump_component_config(self, component_name):
        config = self._components[component_name].export()
        self.raise_event('save_component_config', config)
        return json.dumps(config, indent=4)

    def dump_project_config(self):
        config = self._project_config.copy()
        self.raise_event('save_project_config', config)
        return json.dumps(config, indent=4)
