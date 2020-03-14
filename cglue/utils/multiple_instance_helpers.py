from cglue.component import ComponentInstance
from cglue.utils.common import indent


def add_instance_check(body_to_wrap, component_instance: ComponentInstance, instance_arg_name='instance'):
    return f'if ({instance_arg_name} == &{component_instance.instance_var_name})\n' \
           f'{{\n' \
           f'{indent(body_to_wrap)}\n' \
           f'}}'


def get_instance_argument(argument_names, component_instance: ComponentInstance):
    instance_var_name = None
    if port_component_is_instanced(component_instance):
        instance_var_name = argument_names.pop(0)

    return instance_var_name


def port_component_is_instanced(component_instance: ComponentInstance):
    return component_instance.component.config['multiple_instances']
