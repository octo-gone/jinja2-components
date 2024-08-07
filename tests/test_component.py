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


class TestComponent(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(RuntimeError) as exc:
            env.from_string("{% empty %}").render()
        self.assertEqual(
            exc.exception.args[0],
            "Either template_name, template_str or template "
            "must be set for component 'Empty'.",
        )

    def test_unregistered(self):
        print(ComponentsExtension.tags)
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% unregistered_tag %}")
        self.assertEqual(
            exc.exception.message,
            "Encountered unknown tag 'unregistered_tag'.",
        )
