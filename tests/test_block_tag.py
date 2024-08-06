import unittest

from jinja2 import Environment, Template, TemplateSyntaxError, loaders
from jinja2_components import ComponentsExtension, Component, register


env = Environment(
    loader=loaders.FileSystemLoader("tests/templates"),
    extensions=[ComponentsExtension],
)


@register(name="blocktag")
class BlockTag(Component):
    template = Template("block")
    block = True


class TestBlockTag(unittest.TestCase):
    def test_block_tag(self):
        template = env.from_string("{% blocktag %}{% endblocktag %}")
        self.assertEqual(template.render(), "block")

    def test_incomplete_block_tag(self):
        with self.assertRaises(TemplateSyntaxError) as exc:
            env.from_string("{% blocktag %}")
        self.assertEqual(
            exc.exception.message,
            "Unexpected end of template. Jinja was looking for "
            "the following tags: 'endblocktag'. The innermost "
            "block that needs to be closed is 'blocktag'.",
        )

    def test_replacement(self):
        template = env.from_string("{% blocktag %}73{% endblocktag %}")
        self.assertEqual(template.render(), "block")

    def test_assignment(self):
        template = env.from_string("{% blocktag as res %}73{% endblocktag %}")
        self.assertEqual(template.render(), "")
        template = env.from_string("{% blocktag as res %}73{% endblocktag %}{{ res }}")
        self.assertEqual(template.render(), "block")
