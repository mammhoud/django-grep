# Components System: Core Architecture & Usage

The `django-grep` component system is a high-performance, modular framework for building interactive web interfaces in Django and Wagtail. It provides isolated contexts, asset management, slot-based nesting, and a unique dynamic rendering engine.

---

## 🚀 The `comp` Tag

The `{% comp %}` tag is the primary way to render components. It is faster, more powerful, and cleaner than standard Django `{% include %}`.

### Basic Usage
```html
{% load components %}

{# Standard component #}
{% comp "content.card" title="Hello World" %}
    <p>This is the card content inside the default slot.</p>
{% endcomp %}

{# Self-closing component #}
{% comp "navigation.top_menu" / %}
```

### Advanced Modifiers
- **`only`**: Isolates the context, preventing the component from accessing parent template variables.
  `{% comp "my.comp" title="Secret" only / %}`
- **`with`**: Alias for passing multiple variables at once.
- **`slot`**: Used within a block call to target specific named areas.

---

## ⚡️ Dynamic Rendering Engine

`django-grep` features a native dynamic renderer that allows for run-time compilation of HTML templates, perfect for CMS-managed components like Wagtail Snippets.

### 1. Unified Trigger: `component_name`
The system reserves a special identifier (defined in `SystemComponentName.DYNAMIC`) to trigger the dynamic renderer.

```html
{# Rendering a template from a Wagtail snippet or database field #}
{% comp "component_name" html_file=my_snippet.html_file / %}
```

### 2. Variable Provenance: `component_var`
When using the dynamic trigger, the renderer automatically injects `component_var` into the context, containing the raw name of the variable passed as the `html_file`.

```html
<!-- Inside the dynamic HTML -->
<p>Context source: {{ component_var }}</p>
```

---

## 🛠️ Full Component Example (Enhanced)

This example demonstrates a complex component with props, slots, assets, and HTMX integration.

### 1. The Template: `components/ui/modal.html`
```html
{% load components %}
{# 1. Define Props #}
{% prop name="id" default="modal-default" %}
{% prop name="title" default="Modal" %}
{% prop name="size" default="md" %}

{# 2. Component Assets #}
{% asset "css" %}
<style>
    .comp-modal { display: none; position: fixed; z-index: 1000; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); }
    .comp-modal--open { display: flex; align-items: center; justify-content: center; }
    .comp-modal__content { background: white; border-radius: 8px; max-width: 600px; width: 90%; }
    .comp-modal__header { padding: 1rem; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; }
    .comp-modal__body { padding: 1.5rem; }
    .comp-modal__footer { padding: 1rem; border-top: 1px solid #ddd; text-align: right; }
</style>
{% endasset %}

<div id="{{ props.id }}" class="comp-modal comp-modal--{{ props.size }}" data-comp="modal">
    <div class="comp-modal__content">
        <header class="comp-modal__header">
            <h3>{{ props.title }}</h3>
            <button onclick="document.getElementById('{{ props.id }}').classList.remove('comp-modal--open')">&times;</button>
        </header>

        <div class="comp-modal__body">
            {% slot %}{% endslot %} {# Default slot: The Body #}
        </div>

        {% if slots.footer %}
            <footer class="comp-modal__footer">
                {{ slots.footer }}
            </footer>
        {% endif %}
    </div>
</div>

{% asset "js" %}
<script>
    (function() {
        console.log("Modal [{{ props.id }}] initialized.");
        // Component-specific logic...
    })();
</script>
{% endasset %}
```

### 2. Usage in Parent Template
```html
{# Trigger a dynamic component inside a modal #}
{% comp "ui.modal" title="Custom Content" id="myModal" %}

    <div class="dynamic-wrapper">
        {% if custom_snippet %}
            {% comp "component_name" html_file=custom_snippet.html_file / %}
        {% else %}
            <p>No custom content uploaded.</p>
        {% endif %}
    </div>

    {% slot "footer" %}
        <button class="btn btn-secondary" onclick="closeModal()">Close</button>
        <button class="btn btn-primary" hx-post="/save/" hx-target="#myModal">Save Changes</button>
    {% endslot %}

{% endcomp %}
```

---

## 🧩 Virtual Components

Virtual components allow the registry to handle identifiers that don't match a filesystem path.

- **Purpose**: Primarily used for dynamic triggers or system-generated components.
- **Behavior**: If `COMPONENTS["COMPONENT_NAME_ATTR"]` is called, the registry skips the file search and initializes a template-less component that delegates rendering to a specialized renderer (like `DynamicComponentRenderer`).

---

## ⚙️ Configuration

Customizing behavior via `settings.py`:

```python
COMPONENTS = {
    "RENDERER_VARIABLE": "html_file",        # Variable to look for in dynamic renders
    "COMPONENT_NAME_ATTR": "component_name",  # The virtual trigger name
    "ENABLE_BLOCK_ATTRS": True,               # Adds debug data-attrs to HTML (id, name)
    "COMPONENT_DIRS": ["custom_components"],  # Extra lookup paths
}
```

---

## 📦 Extension: Wagtail Snippets Pattern

A common pattern is to bridge Wagtail Snippets with `django-grep`:

1.  **Model**: A snippet with a `FileField` (html) and a choice field using `SystemComponentName.choices()`.
2.  **Renderer**: A custom `DynamicComponentRenderer` that handles the `html_file`.
3.  **Template**:
    ```html
    {# Selectable global component #}
    {% with html=settings.core.SiteSettings.custom_header.html_file %}
        {% comp "component_name" html_file=html / %}
    {% endwith %}
    ```
