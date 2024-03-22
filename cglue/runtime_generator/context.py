from collections import defaultdict

from cglue.component import ComponentInstanceCollection
from cglue.ports import Port


class RuntimeGeneratorContext:
    def __init__(self, owner):
        self._owner = owner
        self._context = {
            "runtime": owner,
            "files": {},
            "functions": {},
            "declarations": [],
            "exported_function_declarations": [],
            "runtime_includes": {'"utils.h"'},
            "signals": defaultdict(lambda: defaultdict(list)),
            "used_types": [],
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

    def get_port(self, short_name) -> Port:
        return self._owner.get_port(self.get_component_ref(short_name))

    def _split(self, short_name):
        component_name, port_name = short_name.split("/", 2)
        return self.component_instances[component_name], port_name

    def get_component_ref(self, short_name):
        component, port_name = self._split(short_name)
        return f"{component.component.name}/{port_name}"

    def get_component_instance(self, port_short_name):
        component, port = self._split(port_short_name)
        return component
