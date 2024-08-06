import json
import unittest

from jinja2 import Environment, Template, TemplateSyntaxError, loaders
from jinja2_components import ComponentsExtension, Component, register

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@register(name="jsonify")
class Jsonify(Component):
    template = Template("{{ result }}")

    @classmethod
    def get_context(cls, *args, **kwargs):
        return {"result": json.dumps({"args": args, "kwargs": kwargs})}


class TestArguments(unittest.TestCase):
    def test_empty(self):
        template = env.from_string("{% jsonify %}")
        self.assertEqual(template.render(), '{"args": [], "kwargs": {}}')

    def test_args(self):
        template = env.from_string("{% jsonify 1, 2, 3 %}")
        self.assertEqual(template.render(), '{"args": [1, 2, 3], "kwargs": {}}')

    def test_kwargs(self):
        template = env.from_string("{% jsonify a=1, b=3, something='something' %}")
        self.assertEqual(
            template.render(),
            '{"args": [], "kwargs": {"a": 1, "b": 3, "something": "something"}}',
        )

    def test_args_kwargs(self):
        template = env.from_string(
            "{% jsonify 1, 2, 3, a=1, b=3, something='something' %}"
        )
        self.assertEqual(
            template.render(),
            '{"args": [1, 2, 3], "kwargs": {"a": 1, "b": 3, "something": "something"}}',
        )

    def test_wrong_order(self):
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% jsonify 1, a=1, 2, something='something' %}")
        self.assertEqual(exc.exception.message, "Invalid argument syntax")

    def test_trailing_comma(self):
        template = env.from_string("{% jsonify 1, 2, 3, %}")
        self.assertEqual(template.render(), '{"args": [1, 2, 3], "kwargs": {}}')
