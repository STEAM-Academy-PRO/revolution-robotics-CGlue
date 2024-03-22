from cglue.utils.version import Version, VersionConstraint


class Component:
    "A software component definition."

    @staticmethod
    def create_empty_config(name):
        return Component.normalize_config({"name": name, "source_files": [f"{name}.c"]})

    @staticmethod
    def normalize_config(config):
        defaults = {
            "name": "ComponentName",
            "version": "1.0.0",
            "requires": {},
            "source_files": [],
            "multiple_instances": False,
            "instance_variables": {},
            "types": {},
            "runnables": {},
            "ports": {},
        }

        defaults.update(config)
        return defaults

    def __init__(self, name, config, types):
        self._name = name
        self.types = types
        self._config = self.normalize_config(config)

        self._version = Version(self._config["version"])
        self._dependencies = {
            component: VersionConstraint(constraint)
            for component, constraint in self._config["requires"].items()
        }

        if (
            self._config["instance_variables"]
            and not self._config["multiple_instances"]
        ):
            raise ValueError(
                f"Component {name} has instance variables but does not support multiple instances"
            )

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        self._config[key] = value

    def export(self):
        return self._config.copy()

    @property
    def version(self):
        return self._version

    @property
    def name(self):
        return self._name

    @property
    def config(self):
        return self._config

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def instance_type(self):
        assert self._config["multiple_instances"], "Component has no instance variable"
        return f"{self._name}_Instance_t"

    def create_instance(self, name):
        return ComponentInstance(self, name)


class ComponentCollection:
    "A collection of components."

    def __init__(self):
        self._components = {}

    def add(self, component: Component):
        self._components[component.name] = component

    def __delitem__(self, key):
        del self._components[key]

    def __iter__(self):
        yield from self._components.values()

    def __getitem__(self, item):
        return self._components[item]

    def __contains__(self, item):
        return item in self._components

    def check_all_dependencies(self) -> list:
        failures = []

        for component in self._components.values():
            failures.extend(self.check_dependencies(component.name))

        return failures

    def check_dependencies(self, checked_component: str) -> list:
        failures = []

        for required_component_name, version_constraint in self._components[
            checked_component
        ].dependencies.items():
            required_component = self._components[required_component_name]
            if not version_constraint.check(required_component.version):
                failures.append(
                    f"Component {checked_component} failed to meet requirement"
                    f" of {checked_component} ({version_constraint})"
                )

        return failures


class ComponentInstance:
    def __init__(self, component: Component, name):
        self._name = name
        self._prototype = component

        if name != component.name:
            assert component.config[
                "multiple_instances"
            ], f"Component {component.name} does not support instantiating"

    @property
    def name(self):
        return self._name

    @property
    def component_name(self):
        return self._prototype.name

    @property
    def component(self):
        return self._prototype

    @property
    def instance_var_name(self):
        assert self._prototype.config[
            "multiple_instances"
        ], "Component has no instance variable"
        return f"{self._prototype.name}_instance_{self._name}"


class ComponentInstanceCollection:
    def __init__(self):
        self._instances = {}

    def add(self, value: ComponentInstance):
        if value.name in self._instances:
            instance_component = self._instances[value.name]
            raise ValueError(
                f"Component instance {value.name} already exists "
                f"(instance of component {instance_component.component_name}"
            )
        self._instances[value.name] = value

    def __getitem__(self, item):
        return self._instances[item]

    def __iter__(self):
        yield from self._instances.values()
