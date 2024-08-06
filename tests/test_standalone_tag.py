import unittest

from jinja2 import Environment, Template, loaders
from jinja2_components import ComponentsExtension, Component, register


env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@register(name="tag1")
class TemplateTag(Component):
    template = Template("replacement1")


@register(name="tag2")
class TemplateFileTag(Component):
    template_name = "template_file_tag.j2"


class TestStandaloneTag(unittest.TestCase):
    def test_template_tag(self):
        template = env.from_string("{% tag1 %}")
        self.assertEqual(template.render(), "replacement1")

    def test_template_file_tag(self):
        template = env.from_string("{% tag2 %}")
        self.assertEqual(template.render(), "replacement2")

    def test_both_tags(self):
        template = env.from_string("{% tag1 %}{% tag2 %}")
        self.assertEqual(template.render(), "replacement1replacement2")
