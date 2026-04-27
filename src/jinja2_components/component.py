"""Component base class for Jinja2 Components."""

import typing as t

if t.TYPE_CHECKING:
    from jinja2 import Environment, Template


class Component:
    """Base class for creating reusable template components.

    Class Variables:
        template: A pre-compiled Jinja2 template instance.
        template_str: Template content as a string, compiled using the environment.
        template_name: Name of a template file to load from the environment.
        block: Set to True for block tags that wrap content (default: False).
    """

    template: t.ClassVar[t.Optional["Template"]]
    template_str: t.ClassVar[t.Optional[str]]
    template_name: t.ClassVar[t.Optional[str]]
    block: t.ClassVar[bool] = False

    def __new__(cls, env: "Environment", *args: t.Any, **kwargs: t.Any) -> str:  # type: ignore[misc]  # pylint: disable=unused-argument
        """Creates and renders a component instance.

        Args:
            env: The Jinja2 environment.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The rendered component as a string.
        """
        template = cls.get_template(env, *args, **kwargs)
        return template.render(cls.get_context(*args, **kwargs))

    @classmethod
    def get_context(cls, *args: t.Any, **kwargs: t.Any) -> t.Dict[str, t.Any]:  # pylint: disable=unused-argument
        """Prepares the rendering context.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            A dictionary of context variables.
        """
        return kwargs

    @classmethod
    def get_template(cls, env: "Environment", *args: t.Any, **kwargs: t.Any) -> "Template":  # pylint: disable=unused-argument
        """Retrieves or creates the template instance.

        Args:
            env: The Jinja2 environment.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The Jinja2 template instance.
        """
        if hasattr(cls, "template") and cls.template is not None:
            return cls.template
        if hasattr(cls, "template_str") and cls.template_str is not None:
            cls.template = env.from_string(cls.template_str)
        elif hasattr(cls, "template_name") and cls.template_name is not None:
            cls.template = env.get_template(cls.template_name)
        else:
            raise RuntimeError(
                f"Either template_name, template_str or template must be set for component '{cls.__name__}'."
            )
        return cls.template
