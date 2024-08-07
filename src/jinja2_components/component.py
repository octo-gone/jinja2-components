import typing as t

if t.TYPE_CHECKING:
    from jinja2 import Template, Environment


class Component:
    template: t.ClassVar[t.Optional["Template"]]
    template_str: t.ClassVar[t.Optional[str]]
    template_name: t.ClassVar[t.Optional[str]]
    block: t.ClassVar[bool] = False

    @classmethod
    def get_context(cls, *args, **kwargs):
        return kwargs

    @classmethod
    def get_template(cls, env: "Environment", *args, **kwargs):
        if hasattr(cls, "template") and cls.template is not None:
            return cls.template
        elif hasattr(cls, "template_str") and cls.template_str is not None:
            cls.template = env.from_string(cls.template_str)
        elif hasattr(cls, "template_name") and cls.template_name is not None:
            cls.template = env.get_template(cls.template_name)
        else:
            raise RuntimeError(
                "Either template_name, template_str or template must "
                f"be set for component '{cls.__name__}'."
            )
        return cls.template
