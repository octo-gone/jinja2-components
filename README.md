# Jinja2 Components

Template components for Jinja2, inspiration from `django-components` and `jinja2-simple-tags`.

## Usage

Standalone tag replacement with specified template

```python
from jinja2 import Environment, Template
from jinja2_components import ComponentsExtension, Component, register

env = Environment(extensions=[ComponentsExtension])

@register(name="hello")
class Hello(Component):
    template = Template("hello")

template = env.from_string("{% hello %} world")
print(template.render())
# hello world
```

Processing body of tag

```python
from base64 import b64encode

from jinja2 import Environment, Template
from jinja2_components import ComponentsExtension, Component, register

env = Environment(extensions=[ComponentsExtension])

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