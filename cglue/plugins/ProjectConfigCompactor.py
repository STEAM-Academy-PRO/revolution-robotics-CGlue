from cglue.cglue import Plugin, CGlue


def process_port_ref_shorthand(port, port_key='port'):
    """Parse shorthand form of port reference into a dictionary"""
    if type(port) is str:
        parts = port.split('/')
        port = {
            'short_name': port,
            'component':  parts[0],
            port_key:     parts[1]
        }
    else:
        port['short_name'] = f"{port['component']}/{port[port_key]}"

    return port


def expand_port(runnable, port_key):
    if type(runnable) is list:
        runnable, attributes = runnable
    else:
        attributes = {}

    return {
        **process_port_ref_shorthand(runnable, port_key),
        'attributes': attributes
    }


def expand_port_connection(port_connection):
    try:
        consumers = port_connection['consumers']
    except KeyError:
        consumers = [port_connection['consumer']]

    connection = {
        'consumers': [expand_port(consumer, 'port') for consumer in consumers],
        'provider': process_port_ref_shorthand(port_connection['provider'], 'port')
    }

    attrs = {k: v for k, v in port_connection.items() if k not in ('provider', 'consumer', 'consumers')}
    connection.update(attrs)

    return connection


def expand_project_config(owner, project_config):
    """Expand shorthand forms in project configuration"""
    processed_runnables = {}
    raw_runnables = project_config['runtime'].get('runnables', {})
    raw_port_connections = project_config['runtime'].get('port_connections', [])

    for runnable_group, runnables in raw_runnables.items():
        processed_runnables[runnable_group] = [expand_port(runnable, 'runnable') for runnable in runnables]

    project_config['runtime']['runnables'] = processed_runnables
    project_config['runtime']['port_connections'] = [expand_port_connection(port_connection)
                                                     for port_connection in raw_port_connections]


def _compact_ref(ref):
    if type(ref) is str:
        return ref

    if 'attributes' in ref:
        if not ref['attributes'].get('arguments', True):
            del ref['attributes']['arguments']

        if not ref['attributes']:
            del ref['attributes']

    if set(ref.keys()).difference(('short_name', 'component', 'port', 'runnable', 'attributes')):
        return {key: ref[key] for key in ref if key != 'short_name'}

    if 'attributes' in ref:
        return [ref['short_name'], ref['attributes']]
    else:
        return ref['short_name']


def compact_project_config(owner: CGlue, config):
    """Simplify parts that don't need to remain in their expanded forms"""
    types = {}

    component_types = list(component_data.config.get('types', {}) for component_data in owner._components)
    for t in owner.types.export():
        if t in config['types'] and not any(t in types for types in component_types):
            types[t] = config['types'][t]

    expanded_runtime = config['runtime'].copy()

    compacted_runtime = {
        'runnables':        {},
        'port_connections': []
    }

    for group, runnables in expanded_runtime['runnables'].items():
        compacted_runtime['runnables'][group] = list(map(_compact_ref, runnables))

    for connection in expanded_runtime['port_connections']:
        compacted_connection = {
            'provider': _compact_ref(connection['provider'])
        }

        consumers = list(map(_compact_ref, connection['consumers']))
        if len(consumers) == 1:
            compacted_connection['consumer'] = consumers[0]
        else:
            compacted_connection['consumers'] = consumers

        compacted_connection.update(
            {key: value for key, value in connection.items() if key not in ('provider', 'consumers')})

        compacted_runtime['port_connections'].append(compacted_connection)

    config['runtime'] = compacted_runtime
    config['types'] = types


def project_config_compactor():
    """Plugin that expands project configuration on load and compacts it on save"""
    handlers = {
        'load_project_config': expand_project_config,
        'save_project_config': compact_project_config
    }
    return Plugin("ProjectConfigCompactor", handlers)
