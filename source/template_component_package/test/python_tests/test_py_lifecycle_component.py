import pytest

from template_component_package.py_lifecycle_component import PyLifecycleComponent


@pytest.fixture()
def py_lifecycle_component(ros_context):
    yield PyLifecycleComponent('py_lifecycle_component')


def test_construction(py_lifecycle_component):
    assert py_lifecycle_component.get_name() == 'py_lifecycle_component'
