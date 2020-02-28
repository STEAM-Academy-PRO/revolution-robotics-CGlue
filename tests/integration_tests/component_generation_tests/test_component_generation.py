import os
import unittest

from cglue import cglue
from cglue.plugins.BuiltinDataTypes import builtin_data_types
from cglue.plugins.RuntimeEvents import runtime_events
from cglue.plugins.ProjectConfigCompactor import project_config_compactor


class TestComponentGeneration(unittest.TestCase):
    def test_component_generation_does_not_raise_error(self):
        os.chdir(os.path.dirname(__file__))

        generator = cglue.CGlue("../fixtures/00-demo-test/project_consumer_list.json")

        generator.add_plugin(project_config_compactor())
        generator.add_plugin(builtin_data_types())
        generator.add_plugin(runtime_events())

        generator.load()

        generator.update_component('foo')

    def test_typedefs_of_required_component_are_generated(self):
        os.chdir(os.path.dirname(__file__))
        root = '../fixtures/01-component-dependency'

        generator = cglue.CGlue(f"{root}/project.json")

        generator.add_plugin(project_config_compactor())
        generator.add_plugin(builtin_data_types())
        generator.add_plugin(runtime_events())

        generator.load()

        files = generator.update_component('foo')
        with open(f'{root}/foo.expected.h', 'r') as f:
            expected = f.read()
        self.assertEqual(expected, files[f'{root}/components/foo/foo.h'])

    def test_runnables_can_implement_func_ptrs(self):
        os.chdir(os.path.dirname(__file__))
        root = '../fixtures/02-funcptr-runnable'

        generator = cglue.CGlue(f"{root}/project.json")

        generator.add_plugin(project_config_compactor())
        generator.add_plugin(builtin_data_types())
        generator.add_plugin(runtime_events())

        generator.load()

        files = generator.update_component('foo')
        with open(f'{root}/foo.expected.h', 'r') as f:
            expected = f.read()
        self.assertEqual(expected, files[f'{root}/components/foo/foo.h'])
