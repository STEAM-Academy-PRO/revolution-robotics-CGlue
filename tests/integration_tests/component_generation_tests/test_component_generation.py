import os
import unittest

from cglue import cglue
from cglue.plugins.BuiltinDataTypes import builtin_data_types
from cglue.plugins.RuntimeEvents import runtime_events
from cglue.plugins.ProjectConfigCompactor import project_config_compactor
from cglue.plugins.AsyncServerCalls import async_server_calls
from cglue.plugins.UserCodePlugin import user_code_plugin


def _create_generator(path):
    generator = cglue.CGlue(path)

    generator.add_plugin(project_config_compactor())
    generator.add_plugin(builtin_data_types())
    generator.add_plugin(runtime_events())
    generator.add_plugin(async_server_calls())
    generator.add_plugin(user_code_plugin())

    generator.load()
    return generator


class TestComponentGeneration(unittest.TestCase):

    def _test_generated_files(self, project_file, component, expectations):
        os.chdir(os.path.dirname(__file__))

        root = os.path.dirname('../fixtures/' + project_file)
        generator = _create_generator('../fixtures/' + project_file)

        files = generator.update_component(component)

        self.maxDiff = None
        
        # to bless the output, uncomment this and run the test
        # for generated_file, expected_file in expectations.items():
        #     with open(f'{root}/{expected_file}', 'w') as f:
        #         f.write(files[f'{root}/components/{component}/{generated_file}'])

        for generated_file, expected_file in expectations.items():
            with open(f'{root}/{expected_file}', 'r') as f:
                file_contents = f.read()

            self.assertEqual(file_contents, files[f'{root}/components/{component}/{generated_file}'])

    def test_component_generation_does_not_raise_error(self):
        self._test_generated_files('00-demo-test/project_consumer_list.json', 'foo', {})

    def test_typedefs_of_required_component_are_generated(self):
        self._test_generated_files('01-component-dependency/project.json', 'foo', {
            'foo.h': 'foo.expected.h'
        })

    def test_async_call_stubs_are_generated(self):
        self._test_generated_files('00-async-calls/project.json', 'foo', {
            'foo.h': 'foo.expected.h'
        })
        self._test_generated_files('00-async-calls/project.json', 'bar', {
            'bar.h': 'bar.expected.h'
        })

    def test_runnables_can_implement_func_ptrs(self):
        self._test_generated_files('02-funcptr-runnable/project.json', 'foo', {
            'foo.h': 'foo.expected.h'
        })

    def test_multiple_component_instances(self):
        self._test_generated_files('03-multiple-instance/project.json', 'foo', {
            'foo.h': 'foo.expected.h'
        })

    def test_multiple_instance_async(self):
        self._test_generated_files('03-multiple-instance-async/project.json', 'foo', {
            'foo.h': 'foo.expected.h'
        })
        self._test_generated_files('03-multiple-instance-async/project.json', 'bar', {
            'bar.h': 'bar.expected.h'
        })
