import unittest

from jinja2 import Environment, Template, loaders
from jinja2.exceptions import TemplateSyntaxError
from jinja2_components import ComponentsExtension, Component, register

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@register(name="empty")
class Empty(Component):
    pass


class Unregistered(Component):
    template = Template("replacement")


class TestComponent(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(RuntimeError) as exc:
            env.from_string("{% empty %}").render()
        self.assertEqual(
            exc.exception.args[0],
            "Either template_name or template must be set for component 'Empty'.",
        )

    def test_unregistered(self):
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% tag %}")
        self.assertEqual(exc.exception.message, "Encountered unknown tag 'tag'.")
