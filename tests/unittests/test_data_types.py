import unittest

from cglue.data_types import TypeCollection, FunctionPointerType


class TestFunctionPointer(unittest.TestCase):
    def test_(self):
        tc = TypeCollection()
        tc.add('uint8_t', {
            'type': 'external_type_def',
            "pass_semantic": "value",
            "defined_in": "<stdint.h>",
            "default_value": "0u"
        })
        fp = FunctionPointerType(tc)
        self.assertEqual('typedef uint8_t (*test_function)(uint8_t* p);', fp.render_typedef('test_function', {
            'return_type': 'uint8_t',
            'arguments': {
                'p': {
                    'data_type': tc.get('uint8_t'),
                    'direction': 'out'
                }
            }
        }))
