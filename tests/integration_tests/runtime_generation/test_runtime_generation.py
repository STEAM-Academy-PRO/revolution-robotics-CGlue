import unittest
import os

from cglue import cglue
from cglue.plugins.BuiltinDataTypes import builtin_data_types
from cglue.plugins.RuntimeEvents import runtime_events
from cglue.plugins.ProjectConfigCompactor import project_config_compactor


def _create_generator(project_config_path):
    generator = cglue.CGlue(project_config_path)

    generator.add_plugin(project_config_compactor())
    generator.add_plugin(builtin_data_types())
    generator.add_plugin(runtime_events())

    generator.load()
    return generator


class TestRuntimeGeneration(unittest.TestCase):
    def test_expected_header_is_generated(self):
        os.chdir(os.path.dirname(__file__))

        root = "../fixtures/00-demo-test"
        generator = _create_generator(f"{root}/project_consumer_list.json")

        files = generator.generate_runtime('runtime_file')

        with open(f'{root}/runtime.expected.h', 'r') as f:
            expected = f.read()
        self.assertEqual(expected, files[f'runtime_file.h'])

    def test_complex_connection_does_not_cause_error_when_consumer_is_in_list(self):
        os.chdir(os.path.dirname(__file__))

        root = "../fixtures/00-demo-test"
        generator = _create_generator(f"{root}/project_consumer_list.json")

        generator.generate_runtime('runtime_file')

    def test_complex_connection_does_not_cause_error_when_consumer_is_by_itself(self):
        os.chdir(os.path.dirname(__file__))

        root = "../fixtures/00-demo-test"
        generator = _create_generator(f"{root}/project_single_consumer.json")

        generator.generate_runtime('runtime_file')

    def test_can_generate_runtime_with_dependent_components(self):
        os.chdir(os.path.dirname(__file__))

        root = "../fixtures/01-component-dependency"
        generator = _create_generator(f"{root}/project.json")

        generator.generate_runtime('runtime_file')

    def test_runtime_types_are_generated_in_dependency_order(self):
        os.chdir(os.path.dirname(__file__))

        root = "../fixtures/01-component-dependency"
        generator = _create_generator(f"{root}/project.json")

        files = generator.generate_runtime('runtime_file')

        with open(f'{root}/runtime.expected.h', 'r') as f:
            expected = f.read()
        self.assertEqual(expected, files[f'runtime_file.h'])

    def test_multiple_component_instances(self):
        os.chdir(os.path.dirname(__file__))

        root = "../fixtures/03-multiple-instance"
        generator = _create_generator(f"{root}/project.json")

        files = generator.generate_runtime('runtime')

        with open(f'{root}/runtime.expected.h', 'r') as f:
            expected_h = f.read()
        with open(f'{root}/runtime.expected.c', 'r') as f:
            expected_c = f.read()

        self.maxDiff = None

        self.assertEqual(expected_h, files[f'runtime.h'])
        self.assertEqual(expected_c, files[f'runtime.c'])
