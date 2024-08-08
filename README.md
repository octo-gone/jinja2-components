# Jinja2 Components

Jinja2 Components offers a streamlined way to build and reuse your Jinja2 templates from code, inspired by `django-components` and `jinja2-simple-tags`.

**Note:** This library is under active development, so the API may change.

## Key Ideas

-   **Modular Design.** Break down your templates into reusable components for cleaner code and easier maintenance.
-   **Simple Syntax.** Use Jinja2 syntax to only use your components, lower you templates depth.
-   **Extensible Framework.** Customize your components using Python code.

## Usage

1. Install the library.

    ```sh
    pip install jinja2-components
    ```

2. Add extension to the Jinja2 environment.

    ```python
    from jinja2 import Environment
    from jinja2_components import ComponentsExtension

    env = Environment(extensions=[ComponentsExtension])
    ```

3. Define a component and it's template.

    ```python
    from jinja2 import Template
    from jinja2_components import Component, register

    @register(name="hello")
    class Hello(Component):
        template = Template("hello")
    ```

4. Use component inside template as a tag.

    ```python
    template = env.from_string("{% hello %} world")
    print(template.render())
    # hello world
    ```

## Examples

### Standalone tag

```python
@register(name="hello")
class Hello(Component):
    template = Template("hello")

template = env.from_string("{% hello %} world")
print(template.render())
# hello world
```

### Block tag with body

```python
@register(name="button")
class Button(Component):
    template = Template("<button>{{ body }}</button>")
    block = True

    @classmethod
    def get_context(cls, caller):
        return {"body": str(caller())}

template = env.from_string("{% button %}Hello!{% endbutton %}")
print(template.render())
# <button>Hello!</button>
```

### Replacing body

```python
@register(name="base64")
class Base64(Component):
    template = Template("{{ result }}")
    block = True

    @classmethod
    def get_context(cls, caller):
        content = str(caller()).encode()
        return {"result": b64encode(content).decode()}

template = env.from_string("{% base64 %}hello world{% endbase64 %}")
print(template.render())
# aGVsbG8gd29ybGQ=

template = env.from_string("""\
{% base64 as hw_base64 %}hello world{% endbase64 %}\
Base64 of 'hello world': {{ hw_base64 }}
""")
print(template.render())
# Base64 of 'hello world': aGVsbG8gd29ybGQ=
```

### Component in component

If the component's template was set directly, then this template also requires extensions. You can pass extensions where required or as a workaround use `env.from_string`.

But it possible to use `template_str` and `template_name` class variables for later instantiation from environment.

```python
@register(name="button")
class Button(Component):
    template_str = "<button>{{ body }}</button>"

@register(name="menu")
class Menu(Component):
    template_str = """\
<div class="menu">\
{% for btn in buttons %}
  {% button body=btn %}\
{% endfor %}
</button>
"""

template = env.from_string("{% menu buttons=[1, 2, 3] %}")
print(template.render())
# <div class="menu">
#   <button>1</button>
#   <button>2</button>
#   <button>3</button>
# </button>
```

### Rendering component from code

The idea behind this feature is to pass arguments and get rendered component inside the code.

```python
@register(name="button")
class Button(Component):
    template_str = "<button>{{ body }}</button>"

@register(name="menu")
class Menu(Component):
    template_str = """\
<div class="menu">\
{% for btn in buttons %}
  {% button body=btn %}\
{% endfor %}
</button>
"""

template = env.from_string("{% menu buttons=[1, 2, 3] %}")
print(template.render())
# <div class="menu">
#   <button>1</button>
#   <button>2</button>
#   <button>3</button>
# </button>

print(Menu(env, buttons=[1, 2, 3]))
# <div class="menu">
#   <button>1</button>
#   <button>2</button>
#   <button>3</button>
# </button>
```

Also it is possible to pass initialized components (because the are strings).

```python
@register(name="menu")
class Menu(Component):
    template_str = """\
<div class="menu">\
{% for btn in buttons %}
  {{ btn }}\
{% endfor %}
</button>
"""

rendered = Menu(env, buttons=[Button(env, body=1), Button(env, body=2), Button(env, body=3)])
print(rendered)
# <div class="menu">
#   <button>1</button>
#   <button>2</button>
#   <button>3</button>
# </button>
```