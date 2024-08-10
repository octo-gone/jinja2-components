import typing as t

# Public API
from jinja2_components.component import Component
from jinja2_components.ext import ComponentsExtension

TComponent = t.TypeVar("TComponent", bound=Component)


def register(
    name: str,
    ext_base_cls: t.Type[ComponentsExtension] = ComponentsExtension,
):
    def _register_component(cls: t.Type[TComponent]) -> t.Type[TComponent]:
        ext_base_cls.tags.add(name)
        ext_base_cls.components[name] = cls
        return cls

    return _register_component
