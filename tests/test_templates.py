import unittest

from jinja2 import Environment, Template, loaders
from jinja2.exceptions import TemplateSyntaxError
from jinja2_components import ComponentsExtension, Component, register

env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@register(name="tag")
class Tag(Component):
    template = Template("replacement")


@register(name="tag_name")
class TagName(Component):
    template_name = "template_file_tag.j2"


@register(name="tag_str")
class TagStr(Component):
    template_str = "replacement3"


class TestComponent(unittest.TestCase):
    def test_template(self):
        template = env.from_string("{% tag %}")
        self.assertEqual(template.render(), "replacement")

    def test_template(self):
        template = env.from_string("{% tag_name %}")
        self.assertEqual(template.render(), "replacement2")

    def test_template_str(self):
        template = env.from_string("{% tag_str %}")
        self.assertEqual(template.render(), "replacement3")
