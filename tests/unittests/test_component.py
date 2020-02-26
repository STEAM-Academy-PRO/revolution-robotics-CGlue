import unittest

from cglue.component import Component, ComponentCollection
from cglue.utils.version import Version


class TestComponent(unittest.TestCase):
    def test_default_version_is_added_if_missing(self):
        config = {}
        component = Component('Test', config)
        self.assertEqual(Version('1.0.0'), component.version)


class TestComponentCollection(unittest.TestCase):
    def test_no_exception_when_requirements_are_met(self):
        collection = ComponentCollection()

        component1 = Component('Test1', {'requires': {'Test2': '[1.0.0, 2.0.0)'}, 'version': '1.5.3'})
        component2 = Component('Test2', {'requires': {'Test1': '[1.0.0, 2.0.0)'}, 'version': '1.0.0'})

        collection.add(component1)
        collection.add(component2)
        collection.check_dependencies()

    def test_exception_when_requirements_are_not_met(self):
        collection = ComponentCollection()

        component1 = Component('Test1', {'requires': {'Test2': '[1.0.0, 2.0.0)'}, 'version': '1.5.3'})
        component2 = Component('Test2', {'requires': {'Test1': '[1.0.0, 2.0.0)'}, 'version': '2.0.0'})

        collection.add(component1)
        collection.add(component2)
        self.assertRaises(Exception, collection.check_dependencies)

    def test_minimum_requirement_only(self):
        collection = ComponentCollection()

        component1 = Component('Test1', {'requires': {'Test2': '[1.0.0,'}, 'version': '1.5.3'})
        component2 = Component('Test2', {'requires': {'Test1': '[1.0.0, 2.0.0)'}, 'version': '3.0.0'})

        collection.add(component1)
        collection.add(component2)
        collection.check_dependencies()
