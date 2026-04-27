"""Jinja2 Components library for reusable template components."""

import typing as t

from jinja2_components.component import Component
from jinja2_components.ext import ComponentsExtension

if t.TYPE_CHECKING:
    from jinja2.environment import Environment


def register_component(name: str, env: "Environment"):  # type: ignore
    """Helper function to register a component with a Jinja2 environment.

    Args:
        name: The tag name for the component.
        env: The Jinja2 environment.

    Returns:
        A decorator function to register the component class.
    """
    return env.register_component(name)  # type: ignore


__all__ = ["Component", "ComponentsExtension", "register_component"]
