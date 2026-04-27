import json
import typing as t
import unittest

from jinja2 import Environment, Template, TemplateSyntaxError, loaders

from jinja2_components import Component, ComponentsExtension

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@env.register_component(name="jsonify")  # type: ignore
class Jsonify(Component):
    template = Template("{{ result }}")

    @classmethod
    def get_context(cls, *args: t.Any, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        return {"result": json.dumps({"args": args, "kwargs": kwargs})}


class TestArguments(unittest.TestCase):
    def test_empty(self) -> None:
        template = env.from_string("{% jsonify %}")
        self.assertEqual(template.render(), '{"args": [], "kwargs": {}}')

    def test_args(self) -> None:
        template = env.from_string("{% jsonify 1, 2, 3 %}")
        self.assertEqual(template.render(), '{"args": [1, 2, 3], "kwargs": {}}')

    def test_kwargs(self) -> None:
        template = env.from_string("{% jsonify a=1, b=3, something='something' %}")
        self.assertEqual(
            template.render(),
            '{"args": [], "kwargs": {"a": 1, "b": 3, "something": "something"}}',
        )

    def test_args_kwargs(self) -> None:
        template = env.from_string("{% jsonify 1, 2, 3, a=1, b=3, something='something' %}")
        self.assertEqual(
            template.render(),
            '{"args": [1, 2, 3], "kwargs": {"a": 1, "b": 3, "something": "something"}}',
        )

    def test_wrong_order(self) -> None:
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% jsonify 1, a=1, 2, something='something' %}")
        self.assertEqual(exc.exception.message, "Invalid argument syntax")

    def test_trailing_comma(self) -> None:
        template = env.from_string("{% jsonify 1, 2, 3, %}")
        self.assertEqual(template.render(), '{"args": [1, 2, 3], "kwargs": {}}')
