from cglue.function import ArgumentList
from cglue.utils.common import process_dict


class TypeCategory:
    def __init__(self, type_collection, name, attributes):
        self._name = name
        self._attributes = attributes
        self._type_collection = type_collection

    def __str__(self):
        return f'TypeCategory({self._name})'

    def can_process(self, type_data):
        for attr in self._attributes['required']:
            if attr not in type_data:
                return False
        return True

    def process_type(self, type_data):
        return {
            **self._attributes['static'],
            **process_dict(type_data, required=self._attributes['required'], optional=self._attributes['optional'])
        }

    def render_typedef(self, type_name, type_data):
        raise NotImplementedError

    def render_value(self, type_name, type_data, value, context='assignment'):
        return str(value)

    @property
    def name(self):
        return self._name

    @property
    def attributes(self):
        return self._attributes

    def attribute(self, type_name, type_data: dict, attr_name):
        """Return a specific attribute of the given type"""
        return type_data[attr_name]

    def referenced_types(self, type_name, type_data):
        yield type_name


class TypeAlias(TypeCategory):
    def __init__(self, type_collection):
        attributes = {
            'required': ['aliases'],
            'optional': {'default_value': None, 'pass_semantic': None},
            'static': {
                'type': TypeCollection.ALIAS
            }
        }
        super().__init__(type_collection, "type_alias", attributes)

    def render_typedef(self, type_name, type_data):
        return f"typedef {type_data['aliases']} {type_name};"

    def render_value(self, type_name, type_data, value, context='assignment'):
        # call the render of aliased type
        return self.aliased_type(type_data).render_value(value, context)

    def attribute(self, type_name, type_data: dict, attr_name):
        return type_data.get(attr_name) or self.aliased_type(type_data).get_attribute(attr_name)

    def referenced_types(self, type_name, type_data):
        yield type_data['aliases']
        yield from super().referenced_types(type_name, type_data)

    def aliased_type(self, type_data):
        return self._type_collection.get(type_data['aliases'])


class BuiltinType(TypeCategory):
    def __init__(self, type_collection):
        attributes = {}
        super().__init__(type_collection, 'builtin', attributes)

    def can_process(self, type_data):
        return False

    def render_typedef(self, type_name, type_data):
        pass


class ExternalType(TypeCategory):
    def __init__(self, type_collection):
        attributes = {
            'required': ['defined_in', 'default_value'],
            'optional': {'pass_semantic': TypeCollection.PASS_BY_VALUE},
            'static': {
                'type': TypeCollection.EXTERNAL_DEF
            }
        }
        super().__init__(type_collection, 'external_type_def', attributes)

    def render_typedef(self, type_name, type_data):
        pass


class FunctionPointerType(TypeCategory):
    def __init__(self, type_collection):
        attributes = {
            'required': ['return_type', 'arguments'],
            'optional': {'pass_semantic': TypeCollection.PASS_BY_VALUE},
            'static': {
                'type': TypeCollection.FUNC_PTR
            }
        }
        super().__init__(type_collection, 'func_ptr', attributes)

    def render_typedef(self, type_name, type_data):
        args = ArgumentList()
        for arg_name, arg_data in type_data['arguments'].items():
            args.add(arg_name, arg_data['direction'], self._type_collection.get(arg_data['data_type']))

        return f"typedef {type_data['return_type']} (*{type_name})({args.get_argument_list()});"

    def referenced_types(self, type_name, type_data):
        yield type_data['return_type']
        yield from {arg['data_type'] for arg in type_data['arguments'].values()}

        yield from super().referenced_types(type_name, type_data)


class TypeWrapper:
    def __init__(self, type_name, type_data, type_category, defined_by):
        self._type_name = type_name
        self._defined_by = defined_by
        self._type_data = type_data
        self._type_category = type_category

    @property
    def name(self):
        return self._type_name

    @property
    def category(self):
        return self._type_category

    @property
    def data(self):
        return self._type_data

    @property
    def defined_by(self):
        return self._defined_by

    def __getitem__(self, item):
        return self._type_data[item]

    def __contains__(self, item):
        return item in self._type_data

    def get(self, item, default=None):
        return self._type_data.get(item, default)

    def render_value(self, value, context='assignment'):
        if value is None:
            value = self.default_value()

        return self.category.render_value(self.name, self._type_data, value, context)

    def get_attribute(self, attr_name):
        return self.category.attribute(self.name, self._type_data, attr_name)

    def default_value(self):
        return self.get_attribute('default_value')

    def passed_by(self):
        return self.get_attribute('pass_semantic')

    def render_typedef(self):
        return self.category.render_typedef(self.name, self._type_data)

    def __eq__(self, o: object) -> bool:
        if type(o) is TypeWrapper:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            o = o._type_data

        return o == self._type_data

    def __hash__(self) -> int:
        return id(self)

    def __str__(self):
        return f'TypeWrapper({self._type_name}, {self._type_category})'


class TypeCollection:
    BUILTIN = 'builtin'
    ALIAS = 'type_alias'
    EXTERNAL_DEF = 'external_type_def'
    FUNC_PTR = 'func_ptr'

    PASS_BY_VALUE = 'value'
    PASS_BY_POINTER = 'pointer'

    def __init__(self):
        self._type_data = {}
        self._type_categories = {}

        self.add_category(TypeAlias(self))
        self.add_category(BuiltinType(self))
        self.add_category(ExternalType(self))
        self.add_category(FunctionPointerType(self))

        default_types = {
            'void':  {
                'type':          TypeCollection.BUILTIN,
                'pass_semantic': TypeCollection.PASS_BY_VALUE,
                'default_value': None
            },
            'void*': {
                'type':          TypeCollection.BUILTIN,
                'pass_semantic': TypeCollection.PASS_BY_VALUE,
                'default_value': 'NULL'
            }
        }

        for name, data in default_types.items():
            self.add(name, data, 'builtin type')

    def add_category(self, info: TypeCategory):
        self._type_categories[info.name] = info

    def category(self, type_category):
        return self._type_categories[type_category]

    def add(self, type_name, info, defined_by):
        try:
            # if the type is already known, check if the definitions are compatible
            existing_type = self.get(type_name)

            print(f'Warning: Duplicate type {type_name} defined in {defined_by}, '
                  f'already added from {existing_type.defined_by}')

            if info != existing_type:
                raise Exception(f'Conflicting definitions exist for {type_name}')
        except KeyError:
            # type is not yet known, add it
            self._type_data[type_name] = TypeWrapper(type_name, info, self._type_categories[info['type']], defined_by)

    def get(self, type_name):
        if type(type_name) is not str:
            return (self._type_data[t] for t in type_name)

        return self._type_data[type_name]

    def export(self):
        def strip(data):
            data = data._type_data.copy()
            if data['type'] in (TypeCollection.ALIAS, TypeCollection.EXTERNAL_DEF):
                del data['type']

            return data

        return {name: strip(data) for name, data in self._type_data.items() if data['type'] != TypeCollection.BUILTIN}

    def collect_type_dependencies(self, type_data: TypeWrapper):
        for referenced_type_name in sorted(type_data.category.referenced_types(type_data.name, type_data)):
            referenced_type = self.get(referenced_type_name)
            if referenced_type != type_data:
                yield from self.collect_type_dependencies(referenced_type)
            else:
                yield referenced_type

    def normalize_type_name(self, type_name):
        if type(type_name) is not str:
            return (self.normalize_type_name(t) for t in type_name)

        try:
            self.get(type_name)
        except KeyError:
            type_name = type_name.replace('const ', '').replace('*', '').replace(' ', '')

        return type_name

    def process_type_definition(self, type_name, type_def):
        if 'type' in type_def:
            type_data = type_def.copy()
            type_category = type_data['type']
            try:
                category = self._type_categories[type_category]
                del type_data['type']
            except KeyError as e:
                raise Exception(f'Unknown type category {type_category} set for {type_name}') from e
        else:
            type_data = type_def

            for type_category, category in self._type_categories.items():
                if category.can_process(type_data):
                    break
            else:
                raise Exception(f'Invalid type definition for {type_name}, maybe missing type specifier?')

        try:
            return category.process_type(type_data)
        except Exception as e:
            raise Exception(f'Type {type_name} ({type_category}) definition is not valid: {e}') from e
