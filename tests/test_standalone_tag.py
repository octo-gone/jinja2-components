import unittest

from jinja2 import Environment, Template, loaders

from jinja2_components import Component, ComponentsExtension

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@env.register_component(name="tag1")  # type: ignore
class TemplateTag(Component):
    template = Template("replacement1")


@env.register_component(name="tag2")  # type: ignore
class TemplateFileTag(Component):
    template_name = "template_file_tag.j2"


class TestStandaloneTag(unittest.TestCase):
    def test_template_tag(self) -> None:
        template = env.from_string("{% tag1 %}")
        self.assertEqual(template.render(), "replacement1")

    def test_template_file_tag(self) -> None:
        template = env.from_string("{% tag2 %}")
        self.assertEqual(template.render(), "replacement2")

    def test_both_tags(self) -> None:
        template = env.from_string("{% tag1 %}{% tag2 %}")
        self.assertEqual(template.render(), "replacement1replacement2")
