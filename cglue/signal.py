class SignalConnection:
    def __init__(self, context, name, signal, provider_name, attributes):
        self.name = name
        self.signal = signal
        self.provider = provider_name
        self.attributes = attributes
        self.consumers = []
        self.context = context

        try:
            signal.create(context, self)
        except Exception:
            print(f'Failed to generate signal implementation for {self.name}')
            raise

    def add_consumer(self, consumer_name, consumer_attributes):
        self.consumers.append((consumer_name, consumer_attributes))

    def generate(self):
        # collect implementations in a list
        function_mods_list = []
        try:
            function_mods = self.signal.generate_provider(self.context, self, self.provider)
            function_mods_list.append(function_mods)
        except Exception:
            print(f'Failed to generate provider implementation for {self.name}')
            raise

        for consumer, attributes in self.consumers:
            try:
                function_mods = self.signal.generate_consumer(self.context, self, consumer, attributes)
                function_mods_list.append(function_mods)
            except Exception:
                print(f'Failed to generate consumer implementation for {self.name} (consumer: {consumer})')
                raise

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
    def __init__(self, consumers='multiple', required_attributes=None):
        if required_attributes is None:
            required_attributes = []

        self._consumers = consumers
        self.required_attributes = frozenset(required_attributes)

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
        missing_attributes = self.required_attributes.difference(attributes.keys())
        if missing_attributes:
            missing_list = ", ".join(missing_attributes)
            raise Exception(f'{missing_list} attributes are missing from connection provided by {provider}')
        return SignalConnection(context, name, self, provider, attributes)
