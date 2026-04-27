import unittest

from jinja2 import Environment, loaders
from jinja2.exceptions import TemplateSyntaxError

from jinja2_components import Component, ComponentsExtension

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@env.register_component(name="empty")  # type: ignore
class Empty(Component):
    pass


class TestComponent(unittest.TestCase):
    def test_empty(self) -> None:
        with self.assertRaises(RuntimeError) as exc:
            env.from_string("{% empty %}").render()
        self.assertEqual(
            exc.exception.args[0],
            "Either template_name, template_str or template must be set for component 'Empty'.",
        )

    def test_unregistered(self) -> None:
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% unregistered_tag %}")
        self.assertEqual(
            exc.exception.message,
            "Encountered unknown tag 'unregistered_tag'.",
        )
