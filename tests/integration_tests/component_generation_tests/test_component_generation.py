import os
import unittest

from cglue import cglue
from cglue.plugins.BuiltinDataTypes import builtin_data_types
from cglue.plugins.RuntimeEvents import runtime_events
from cglue.plugins.ProjectConfigCompactor import project_config_compactor


class TestComponentGeneration(unittest.TestCase):
    def test_complex_connection_does_not_cause_error_when_consumer_is_in_list(self):
        os.chdir(os.path.dirname(__file__))

        generator = cglue.CGlue("fixtures/00-demo-test/project_consumer_list.json")

        generator.add_plugin(project_config_compactor())
        generator.add_plugin(builtin_data_types())
        generator.add_plugin(runtime_events())

        generator.load()

        generator.generate_runtime('runtime_file.c')

    def test_complex_connection_does_not_cause_error_when_consumer_is_by_itself(self):
        os.chdir(os.path.dirname(__file__))

        generator = cglue.CGlue("fixtures/00-demo-test/project_single_consumer.json")

        generator.add_plugin(project_config_compactor())
        generator.add_plugin(builtin_data_types())
        generator.add_plugin(runtime_events())

        generator.load()

        generator.generate_runtime('runtime_file.c')
