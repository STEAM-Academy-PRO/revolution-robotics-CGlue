import chevron

from data_types import TypeCollection, TypeWrapper


class ArgumentList(dict):
    def __init__(self, args: dict = None):
        super().__init__()

        if args:
            for arg_name, arg_data in args.items():
                if type(arg_data) is not dict:
                    arg_data = {
                        'direction': 'in',
                        'data_type': arg_data
                    }
                self.add(arg_name, arg_data['direction'], arg_data['data_type'])

    def add(self, name, direction, data_type: TypeWrapper):
        self[name] = {'direction': direction, 'data_type': data_type}


class FunctionPrototype:
    def __init__(self, name, return_type='void', args=None):
        self._name = name
        self._return_type = return_type

        self._arguments = ArgumentList(args)

    @property
    def function_name(self):
        return self._name

    @property
    def arguments(self):
        return self._arguments

    @property
    def return_type(self):
        return self._return_type

    def generate_call(self, arguments):
        required_args = set(self.arguments.keys())
        missing_args = required_args - arguments.keys()
        if missing_args:
            raise Exception('Arguments are missing from call of {}: {}'
                            .format(self.function_name, ', '.join(missing_args)))

        return '{}({})'.format(self.function_name, ', '.join([str(arguments[name]) for name in self.arguments]))

    @property
    def referenced_types(self):
        return [data['data_type'].name for data in self.arguments.values()] + [self.return_type]

    def generate_header(self):
        def generate_parameter(name, data):

            try:
                pass_by_ptr = data['data_type']['pass_semantic'] == TypeCollection.PASS_BY_POINTER
            except KeyError:
                arg_is_ptr = '*' in data['data_type'].name
                pass_by_ptr = not arg_is_ptr  # pointers can be passed by value, otherwise assume pass-by-pointer

            if data['direction'] == 'in':
                if pass_by_ptr:
                    pattern = 'const {}* {}'
                else:
                    pattern = '{} {}'

            elif data['direction'] in ['out', 'inout']:
                pattern = '{}* {}'

            else:
                raise Exception('Unknown argument direction {}'.format(data['direction']))

            return pattern.format(data['data_type'].name, name)

        args = [generate_parameter(name, data) for name, data in self.arguments.items()]

        return '{} {}({})'.format(self.return_type, self.function_name, 'void' if not args else ', '.join(args))


class FunctionImplementation:

    def __init__(self, func_prototype: FunctionPrototype):
        self._prototype = func_prototype

        self._used_arguments = set()
        self._asserts = set()
        self._return_statement = None
        self._body = []
        self._attributes = set()
        self.includes = set()

    @property
    def prototype(self):
        return self._prototype

    def mark_argument_used(self, arg):
        self._used_arguments.add(arg)

    @property
    def attributes(self):
        return self._attributes

    def add_input_assert(self, statements):
        self.includes.add('"utils_assert.h"')
        if type(statements) is str:
            self._asserts.add('ASSERT({});'.format(statements))
        else:
            for statement in statements:
                self.add_input_assert(statement)

    def add_body(self, body):
        if type(body) is str:
            self._body.append(body)
        else:
            self._body += body

    def prepend_body(self, body):
        self._body.insert(0, body)

    def set_return_statement(self, statement):
        if self._return_statement:
            raise Exception('Return statement already set for {}'.format(self.function_name))

        if statement:
            if self.return_type == 'void':
                raise Exception('Function {} is void'.format(self.function_name))

            self._return_statement = statement

    def get_header(self):
        return self._prototype.generate_header()

    def get_function(self):
        body = list(sorted(self._asserts))
        body += [chunk.replace('\n', '\n    ') for chunk in self._body]
        if self._return_statement:
            body.append('return {};'.format(self._return_statement))

        def remove_trailing_spaces(l):
            return '\n'.join([line.rstrip(' ') for line in l.split('\n')])

        unused_arguments = self.arguments.keys() - self._used_arguments

        for arg in sorted(unused_arguments):
            body.insert(0, '(void) {};'.format(arg))

        ctx = {
            'template': "{{# attributes }}__attribute__(({{ . }}))\n{{/ attributes }}"
                        "{{ header }}\n"
                        "{\n"
                        "{{# body }}\n"
                        "    {{{ . }}}\n"
                        "{{/ body }}\n"
                        "}\n",

            'data': {
                'header': self.get_header(),
                'attributes': list(self._attributes),
                'body': [remove_trailing_spaces(line) for line in body]
            }
        }
        return chevron.render(**ctx)

    @property
    def return_type(self):
        return self._prototype.return_type

    @property
    def arguments(self):
        return self._prototype.arguments

    @property
    def function_name(self):
        return self._prototype.function_name

    @property
    def referenced_types(self):
        return self._prototype.referenced_types

    def function_call(self, arguments):
        return self._prototype.generate_call(arguments)

    def __str__(self) -> str:
        return 'FunctionDescriptor of {}'.format(self.function_name)
