import unittest

from jinja2 import Environment, Template, loaders

from jinja2_components import Component, ComponentsExtension

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@env.register_component(name="tag")  # type: ignore
class Tag(Component):
    template = Template("replacement")


@env.register_component(name="tag_name")  # type: ignore
class TagName(Component):
    template_name = "template_file_tag.j2"


@env.register_component(name="tag_str")  # type: ignore
class TagStr(Component):
    template_str = "replacement3"


class TestComponent(unittest.TestCase):
    def test_template(self) -> None:
        template = env.from_string("{% tag %}")
        self.assertEqual(template.render(), "replacement")

    def test_template_2(self) -> None:
        template = env.from_string("{% tag_name %}")
        self.assertEqual(template.render(), "replacement2")

    def test_template_str(self) -> None:
        template = env.from_string("{% tag_str %}")
        self.assertEqual(template.render(), "replacement3")
