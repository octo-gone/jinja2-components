"""Jinja2 extension for component tags."""

import typing as t

from jinja2 import Environment, nodes
from jinja2.ext import Extension
from jinja2.lexer import describe_token

from jinja2_components.component import Component

if t.TYPE_CHECKING:
    from jinja2.parser import Parser

T = t.TypeVar("T", bound=Component)


class _ComponentsEnvironment(Environment):
    """Type hinting class for environments with register_component method."""

    def register_component(self, name: str) -> t.Callable[[t.Type[T]], t.Type[T]]: ...  # type: ignore  # pylint: disable=missing-function-docstring,unused-argument


class ComponentsExtension(Extension):
    """Jinja2 extension that enables component tag parsing."""

    def __init__(self, environment: "Environment") -> None:  # pylint: disable=super-init-not-called
        """Initialize the extension.

        Args:
            environment: The Jinja2 environment.
        """
        self.environment = environment
        self.components: t.Dict[str, t.Type["Component"]] = {}
        environment.extend(register_component=self.register_component, components=[])

    def register_component(self, name: str) -> t.Callable[[t.Type[T]], t.Type[T]]:
        """Returns a decorator to register a component class.

        Args:
            name: The tag name for the component.

        Returns:
            A decorator function.
        """

        def _register_component(cls: t.Type[T]) -> t.Type[T]:  # pylint: disable=unused-argument
            self.tags.add(name)
            self.components[name] = cls
            return cls

        return _register_component

    def parse(self, parser: "Parser") -> nodes.Node:
        """Parses a component tag.

        Args:
            parser: The Jinja2 parser.

        Returns:
            The parsed AST node.
        """
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
                return nodes.AssignBlock(assign_target, None, [call_block], lineno=lineno)
            return call_block

        if assign_target is not None:
            return nodes.Assign(assign_target, call_node, lineno=lineno)
        return nodes.Output([call_node], lineno=lineno)

    def parse_args(self, parser: "Parser") -> t.Tuple[t.List[nodes.Expr], t.List[nodes.Keyword], t.Optional[str]]:
        """Parses arguments for the component tag.

        Args:
            parser: The Jinja2 parser.

        Returns:
            A tuple of (args, kwargs, variable).
        """
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

            if parser.stream.current.type == "name" and parser.stream.look().type == "assign":
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

    def render(self, tag: str, *args: t.Any, **kwargs: t.Any) -> str:
        """Renders a component.

        Args:
            tag: The component tag name.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The rendered component as a string.
        """
        component = self.components[tag]
        return component(self.environment, *args, **kwargs)  # type: ignore


components = ComponentsExtension  # pylint: disable=invalid-name
