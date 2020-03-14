from cglue.utils.common import process_dict


class SignalConnection:
    def __init__(self, context, name, signal: 'SignalType', provider_name, attributes):
        self.name = name
        self.signal = signal
        self.provider = provider_name
        self.attributes = attributes
        self.consumers = []
        self.context = context

        try:
            signal.create(context, self)
        except Exception as e:
            raise Exception(f'Failed to generate signal implementation for {self.name}') from e

    def add_consumer(self, consumer_name, consumer_attributes):
        self.consumers.append((consumer_name, self.signal.process_attributes(self.attributes, consumer_attributes)))

    def generate(self):
        # collect implementations in a list
        try:
            function_mods_list = [self.signal.generate_provider(self.context, self, self.provider)]
        except Exception as e:
            raise Exception(f'Failed to generate provider implementation for {self.name}') from e

        for consumer, attributes in self.consumers:
            try:
                function_mods = self.signal.generate_consumer(self.context, self, consumer, attributes)
                function_mods_list.append(function_mods)
            except Exception as e:
                raise Exception(f'Failed to generate consumer implementation for '
                                f'{self.name} (consumer: {consumer})') from e

        self.context['runtime'].raise_event('signal_generated', self, function_mods_list)

        self._apply_mods(self.context['functions'], function_mods_list)

    @staticmethod
    def _apply_mods(functions, function_mods_list):
        for function_mods in function_mods_list:
            for port_name, mods in function_mods.items():
                port_functions = functions[port_name]
                for func_type, mod in mods.items():
                    if func_type in port_functions:
                        SignalConnection._apply_mod(port_functions[func_type], mod)

    @staticmethod
    def _apply_mod(func, mod):
        if 'body' in mod:
            func.add_body(mod['body'])

        if 'return_statement' in mod:
            func.set_return_statement(mod['return_statement'])

        if 'used_arguments' in mod:
            for argument in mod['used_arguments']:
                func.mark_argument_used(argument)

    def __str__(self):
        return self.name


class SignalType:
    def __init__(self, consumers='multiple', attributes=None):
        self._consumers = consumers
        self._attributes = attributes

    @property
    def consumers(self):
        return self._consumers

    def create(self, context, connection: SignalConnection):
        pass

    def generate_provider(self, context, connection: SignalConnection, provider_name):
        return {}

    def generate_consumer(self, context, connection: SignalConnection, consumer_name, attributes):
        return {}

    def create_connection(self, context, name, provider, attributes):
        return SignalConnection(context, name, self, provider, process_dict(
            attributes,
            required=self._attributes['required'],
            optional=self._attributes['optional']))

    def process_attributes(self, attributes, consumer_attributes):
        return process_dict(
            {**attributes, **consumer_attributes},
            required=self._attributes['required'],
            optional=self._attributes['optional'])
