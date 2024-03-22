import unittest

from cglue.function import FunctionPrototype, FunctionCallGenerationException
from cglue.data_types import TypeWrapper, BuiltinType, TypeCollection

tc = TypeCollection()
float_type = TypeWrapper("float", {"pass_semantic": "value"}, BuiltinType(tc), "test")
some_object_type = TypeWrapper(
    "Object_t", {"pass_semantic": "pointer"}, BuiltinType(tc), "test"
)


class TestFunctionPrototype(unittest.TestCase):
    def test_generate_call_without_parameters(self):
        fp = FunctionPrototype("foonction")
        self.assertEqual("foonction()", fp.generate_call({}))

    def test_generate_declaration_without_parameters_adds_void(self):
        fp = FunctionPrototype("foonction")
        self.assertEqual("void foonction(void)", fp.generate_header())

    def test_generate_call_fails_if_expected_parameter_is_not_given(self):
        fp = FunctionPrototype(
            "foonction", args={"arg1": {"direction": "in", "data_type": float_type}}
        )
        self.assertRaises(FunctionCallGenerationException, lambda: fp.generate_call({}))

    def test_default_arg_direction_is_in(self):
        fp = FunctionPrototype("foonction", args={"arg1": float_type})
        self.assertEqual("void foonction(float arg1)", fp.generate_header())

    def test_generate_call_with_single_argument(self):
        fp = FunctionPrototype(
            "foonction", args={"arg1": {"direction": "in", "data_type": float_type}}
        )
        self.assertEqual("foonction(4.25)", fp.generate_call({"arg1": 4.25}))

    def test_generate_call_with_multiple_arguments(self):
        fp = FunctionPrototype(
            "foonction",
            args={
                "arg1": {"direction": "in", "data_type": float_type},
                "arg2": {"direction": "out", "data_type": float_type},
            },
        )
        self.assertEqual(
            "foonction(4.25, &varname)",
            fp.generate_call({"arg2": "&varname", "arg1": 4.25}),
        )

    def test_generate_header_out_args_are_pointers(self):
        fp = FunctionPrototype(
            "foonction",
            args={
                "arg1": {"direction": "in", "data_type": float_type},
                "arg2": {"direction": "out", "data_type": float_type},
            },
        )
        self.assertEqual(
            "void foonction(float arg1, float* arg2)", fp.generate_header()
        )

    def test_generate_header_in_pointers_are_const(self):
        fp = FunctionPrototype(
            "foonction",
            args={"arg1": {"direction": "in", "data_type": some_object_type}},
        )
        self.assertEqual("void foonction(const Object_t* arg1)", fp.generate_header())
