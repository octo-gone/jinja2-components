import unittest

from jinja2 import Environment

from jinja2_components import Component, ComponentsExtension, register_component

env1 = Environment(
    extensions=["jinja2_components.ext.components"],
)

env2 = Environment(
    extensions=["jinja2.ext.i18n"],
)

env3 = Environment(
    extensions=["jinja2_components.ext.components"],
)


@env1.register_component(name="A")  # type: ignore
class A(Component):
    pass


@env3.register_component(name="B")  # type: ignore
class B(Component):
    pass


@env1.register_component(name="C")  # type: ignore
@env3.register_component(name="C")  # type: ignore
class C(Component):
    pass


@register_component(name="D", env=env3)
class D(Component):
    pass


class TestLoad(unittest.TestCase):
    def test_loading_by_name(self) -> None:
        self.assertTrue(any([isinstance(ext, ComponentsExtension) for ext in env1.extensions.values()]))

    def test_multiple_envs(self) -> None:
        self.assertFalse(any([isinstance(ext, ComponentsExtension) for ext in env2.extensions.values()]))

        ext1_components = {
            component
            for ext in env1.extensions.values()
            if isinstance(ext, ComponentsExtension)
            for component in ext.components
        }
        ext3_components = {
            component
            for ext in env3.extensions.values()
            if isinstance(ext, ComponentsExtension)
            for component in ext.components
        }

        self.assertSetEqual(ext1_components, {"A", "C"})
        self.assertSetEqual(ext3_components, {"B", "C", "D"})
