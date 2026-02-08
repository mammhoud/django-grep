"""
Reusable mixins for authentication forms.
Provides common functionality across different form types.
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row, Submit
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class SecurityMixin:
    """Mixin providing security features for forms."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_security_fields()

    def add_security_fields(self):
        """Add security-related fields to form."""
        # Honeypot field for bot protection
        self.fields["security_check"] = forms.CharField(
            required=False, widget=forms.HiddenInput(), label="", help_text=""
        )

        # Timestamp to prevent replay attacks
        self.fields["timestamp"] = forms.CharField(
            widget=forms.HiddenInput(), initial=self.get_timestamp_hash()
        )

    def get_timestamp_hash(self):
        """Generate timestamp hash for form validation."""
        import hashlib
        import time

        timestamp = str(int(time.time()))
        return hashlib.sha256(timestamp.encode()).hexdigest()[:10]

    def clean_security_check(self):
        """Clean security check field (honeypot)."""
        data = self.cleaned_data.get("security_check", "")
        if data:  # Bots will fill this field
            raise forms.ValidationError(_("Security check failed."))
        return data


class LayoutMixin:
    """Mixin providing layout configuration for forms."""

    def setup_layout(self, fields, submit_text=None, show_links=True):
        """Setup form layout with proper styling."""
        style = self.get_styling("form")
        helper = self.get_form_helper()

        layout_fields = []

        for field_name in fields:
            if field_name in self.fields:
                field = self.fields[field_name]

                # Determine field type for styling
                if isinstance(field.widget, forms.CheckboxInput):
                    field_type = "checkbox"
                elif isinstance(field.widget, forms.RadioSelect):
                    field_type = "radio"
                elif isinstance(field.widget, forms.Select):
                    field_type = "select"
                elif isinstance(field.widget, forms.Textarea):
                    field_type = "textarea"
                else:
                    field_type = (
                        field.widget.input_type if hasattr(field.widget, "input_type") else "text"
                    )

                # Apply styling
                self.apply_field_styling(field, field_type=field_type, placeholder=field.label)

                # Add to layout
                layout_fields.append(Field(field_name))

        # Add submit button
        if submit_text:
            button_class = self.get_styling("button", "class")
            button_type_class = self.get_styling("button", "types").get("primary", "")
            button_size_class = self.get_styling("button", "size_class").get("default", "")
            button_block_class = self.get_styling("button", "block_class", "")

            button_classes = (
                f"{button_class} {button_type_class} {button_size_class} {button_block_class}"
            )

            layout_fields.append(Submit("submit", submit_text, css_class=button_classes.strip()))

        # Add links if needed
        if show_links and hasattr(self, "get_form_links"):
            layout_fields.extend(self.get_form_links())

        helper.layout = Layout(*layout_fields)
        self.helper = helper

    def get_form_helper(self):
        """Get form helper with configured styling."""
        helper = FormHelper()
        helper.form_method = "post"
        helper.form_class = self.get_styling("form", "class", "")
        helper.label_class = self.get_styling("label", "class", "")
        helper.field_class = self.get_styling("helper", "field_class", "")
        return helper

    def get_form_links(self):
        """Get form navigation links."""
        links = []
        style = self.get_styling("button", "types")

        if hasattr(self, "login_url"):
            links.append(
                HTML(f'''
                    <div class="text-center mt-3">
                        <a href="{self.login_url}" 
                           class="text-decoration-none {style.get("secondary", "")}">
                            {_("Already have an account? Sign in")}
                        </a>
                    </div>
                ''')
            )

        return links


class ValidationMixin:
    """Mixin providing enhanced validation capabilities."""

    def add_error_highlighting(self):
        """Add CSS classes for error highlighting."""
        for field_name, errors in self.errors.items():
            if field_name in self.fields:
                field = self.fields[field_name]
                invalid_class = self.get_styling("validation", "invalid", "")

                if "class" in field.widget.attrs:
                    field.widget.attrs["class"] += f" {invalid_class}"
                else:
                    field.widget.attrs["class"] = invalid_class

    def get_field_with_errors(self, field_name):
        """Get field HTML with error messages."""
        field = self[field_name]
        errors = self.errors.get(field_name, [])

        if errors:
            error_class = self.get_styling("validation", "feedback_invalid", "")
            error_html = f'<div class="{error_class}">{" ".join(errors)}</div>'
            return mark_safe(f"{field}{error_html}")
        return field
