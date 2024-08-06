import typing as t

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.lexer import describe_token

if t.TYPE_CHECKING:
    from jinja2_components.component import Component
    from jinja2.parser import Parser


class ComponentsExtension(Extension):
    components: t.ClassVar[t.Dict[str, t.Type["Component"]]] = {}

    def parse(self, parser: "Parser") -> nodes.Node:
        lineno = parser.stream.current.lineno
        tag = parser.stream.current.value
        parser.stream.skip(1)

        args, kwargs, variable = self.parse_args(parser)
        assign_target = None
        if variable is not None:
            assign_target = nodes.Name(variable, "store", lineno=lineno)

        args.insert(0, nodes.Const(tag))
        call_node = self.call_method("render", args, kwargs, lineno=lineno)

        component = self.components[tag]
        if component.block:
            body = parser.parse_statements((f"name:end{tag}",), drop_needle=True)
            call_block = nodes.CallBlock(call_node, [], [], body).set_lineno(lineno)

            if assign_target is not None:
                return nodes.AssignBlock(
                    assign_target, None, [call_block], lineno=lineno
                )
            return call_block

        if assign_target is not None:
            return nodes.Assign(assign_target, call_node, lineno=lineno)
        return nodes.Output([call_node], lineno=lineno)

    def parse_args(self, parser: "Parser"):
        args: t.List[nodes.Expr] = []
        kwargs: t.List[nodes.Keyword] = []
        variable: t.Optional[str] = None

        comma = False
        while parser.stream.current.type != "block_end":
            if parser.stream.current.test("name:as"):
                parser.stream.skip(1)
                variable = parser.stream.expect("name").value
                if not parser.stream.current.test("block_end"):
                    parser.fail(
                        f"expected token 'block_end', got {describe_token(parser.stream.current)!r}",
                        parser.stream.current.lineno,
                    )
                break

            if comma:
                parser.stream.expect("comma")
                if parser.stream.current.type == "block_end":
                    break

            if (
                parser.stream.current.type == "name"
                and parser.stream.look().type == "assign"
            ):
                key = parser.stream.current.value
                parser.stream.skip(2)
                value = parser.parse_expression()
                kwargs.append(nodes.Keyword(key, value, lineno=value.lineno))
            elif kwargs:
                parser.fail("Invalid argument syntax", parser.stream.current.lineno)
            else:
                args.append(parser.parse_expression())

            comma = True

        return args, kwargs, variable

    def render(self, tag: str, *args, **kwargs):
        component = self.components[tag]
        template = component.get_template(self.environment, *args, **kwargs)
        return template.render(component.get_context(*args, **kwargs))
