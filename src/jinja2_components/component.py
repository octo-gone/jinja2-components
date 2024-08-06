import typing as t

if t.TYPE_CHECKING:
    from jinja2 import Template, Environment


class Component:
    template: t.ClassVar[t.Optional["Template"]]
    template_name: t.ClassVar[t.Optional[str]]
    block: t.ClassVar[bool] = False

    @classmethod
    def get_context(cls, *args, **kwargs):
        return kwargs

    @classmethod
    def get_template(cls, env: "Environment", *args, **kwargs):
        if hasattr(cls, "template") and cls.template is not None:
            return cls.template
        if not hasattr(cls, "template_name") or cls.template_name is None:
            raise RuntimeError(
                "Either template_name or template must "
                f"be set for component '{cls.__name__}'."
            )
        cls.template = env.get_template(cls.template_name)
        return cls.template
