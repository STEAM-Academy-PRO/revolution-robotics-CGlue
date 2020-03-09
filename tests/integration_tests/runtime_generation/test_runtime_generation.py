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

    def _test_generated_files(self, project_file, expectations):
        os.chdir(os.path.dirname(__file__))

        root = os.path.dirname('../fixtures/' + project_file)
        generator = _create_generator('../fixtures/' + project_file)

        files = generator.generate_runtime('runtime')

        self.maxDiff = None

        for generated_file, expected_file in expectations.items():
            with open(f'{root}/{expected_file}', 'r') as f:
                file_contents = f.read()

            self.assertEqual(file_contents, files[generated_file])

    def test_expected_header_is_generated(self):
        self._test_generated_files("00-demo-test/project_consumer_list.json", {
            'runtime.h': 'runtime.expected.h'
        })

    def test_complex_connection_does_not_cause_error_when_consumer_is_by_itself(self):
        self._test_generated_files("00-demo-test/project_single_consumer.json", {})

    def test_runtime_types_are_generated_in_dependency_order(self):
        self._test_generated_files("01-component-dependency/project.json", {
            'runtime.h': 'runtime.expected.h'
        })

    def test_multiple_component_instances(self):
        self._test_generated_files("03-multiple-instance/project.json", {
            'runtime.h': 'runtime.expected.h',
            'runtime.c': 'runtime.expected.c'
        })
