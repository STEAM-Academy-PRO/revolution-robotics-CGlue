import re
from typing import Any, Sequence


def to_underscore(name):
    """
    >>> to_underscore('ADC')
    'adc'
    >>> to_underscore('FizzBuzz')
    'fizz_buzz'
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def chevron_list_mark_last(data, last_key='last'):
    if data:
        data[-1][last_key] = True
    return data


def list_to_chevron_list(data, key_name, last_key=None):
    """Transform a list of key-value pairs to a list of dicts with given key and value names.

    This is useful for passing dictionaries to chevron.
    If the last_key is given, the last item has an extra element with the last_key as key and True as value.

    >>> list_to_chevron_list(['foo', 'bar'], 'key')
    [{'key': 'foo'}, {'key': 'bar'}]
    >>> list_to_chevron_list(['foo', 'bar'], 'key', 'last')
    [{'key': 'foo'}, {'key': 'bar', 'last': True}]
    """
    chevron_list = [{key_name: value} for value in data]
    if last_key:
        chevron_list_mark_last(chevron_list, last_key)
    return chevron_list


def dict_to_chevron_list(data, key_name, value_name, last_key=None):
    """Transform a list of key-value pairs to a list of dicts with given key and value names.

    This is useful for passing dictionaries to chevron.
    If the last_key is given, the last item has an extra element with the last_key as key and True as value.

    >>> dict_to_chevron_list({'foo': 'bar'}, 'key', 'value')
    [{'key': 'foo', 'value': 'bar'}]
    >>> dict_to_chevron_list({'foo': 'bar', 'bar': 'baz'}, 'key', 'value', 'last')
    [{'key': 'foo', 'value': 'bar'}, {'key': 'bar', 'value': 'baz', 'last': True}]
    """
    chevron_list = [{key_name: key, value_name: value} for key, value in data.items()]
    if last_key:
        chevron_list_mark_last(chevron_list, last_key)
    return chevron_list


indent_re = re.compile(r'^([ \t]*\S[^\n]*)$', flags=re.MULTILINE)


def indent(text, spaces=4):
    """
    >>> indent('')
    ''
    >>> indent(' ')
    ' '
    >>> indent('foobar', spaces=2)
    '  foobar'
    >>> indent(' s')
    '     s'
    >>> indent('f o o \\n\\nbar')
    '    f o o \\n\\n    bar'
    """
    indent_prefix = spaces * ' '
    return indent_re.sub(rf'{indent_prefix}\1', text)


trailing_ws_re = re.compile(r'[ \t]+$', flags=re.MULTILINE)


def remove_trailing_spaces(text):
    """
    >>> remove_trailing_spaces('foobar   ')
    'foobar'
    >>> remove_trailing_spaces('foobar  \\n ')
    'foobar\\n'
    """
    return trailing_ws_re.sub('', text)


def rpad(string, length, char=' '):
    """
    >>> rpad('foo', 6)
    'foo   '
    >>> rpad('foo', 2)
    'foo'
    >>> rpad('foo', 6, '#')
    'foo###'
    """
    if len(string) < length:
        string += char * (length - len(string))
    return string


def split(data: Sequence[Any], chunk_size: int):
    """
    >>> list(split([], 5))
    []
    >>> list(split(b'apple', 5))
    [b'apple']
    >>> list(split(b'apple', 7))
    [b'apple']
    >>> list(split([1, 2, 3, 4], 2))
    [[1, 2], [3, 4]]
    >>> list(split([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    >>> list(split(b'apple', 3))
    [b'app', b'le']
    """
    return (data[i:i + chunk_size] for i in range(0, len(data), chunk_size))
