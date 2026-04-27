import unittest

from jinja2 import Environment, Template, TemplateSyntaxError, loaders

from jinja2_components import Component, ComponentsExtension

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@env.register_component(name="best_number")  # type: ignore
class BestNumber(Component):
    template = Template("73")


class TestAssign(unittest.TestCase):
    def test_rendering(self) -> None:
        template = env.from_string("{% best_number %}")
        self.assertEqual(template.render(), "73")

    def test_assign(self) -> None:
        template = env.from_string("{% best_number as value %}")
        self.assertEqual(template.render(), "")

    def test_assign_rendering(self) -> None:
        template = env.from_string("{% best_number as value %}{{ value }}")
        self.assertEqual(template.render(), "73")

    def test_incomplete_assign(self) -> None:
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% best_number as %}")
        self.assertEqual(exc.exception.message, "expected token 'name', got 'end of statement block'")

    def test_after_assign(self) -> None:
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% best_number as value, something %}")
        self.assertEqual(exc.exception.message, "expected token 'block_end', got ','")
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% best_number as value something %}")
        self.assertEqual(exc.exception.message, "expected token 'block_end', got 'something'")
