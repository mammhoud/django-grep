import logging
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.query import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    HelpPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

from django_grep.pipelines.models import DefaultBase

logger = logging.getLogger(__name__)


# @register_snippet÷
class EmailTemplate(DefaultBase):
    name = models.CharField(
        max_length=150,
        verbose_name=_("Template Name"),
        help_text=_("Name for internal reference, e.g., 'Default Newsletter Template'."),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Optional description of this email template."),
    )

    # ------------------------------------------------------------------
    # PUBLICATION SCHEDULING
    # ------------------------------------------------------------------
    go_live_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Go live at"),
        help_text=_("Schedule the template to become active at this date/time."),
    )

    expire_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expire at"),
        help_text=_("Schedule the template to expire at this date/time."),
    )

    # ------------------------------------------------------------------
    # TEMPLATE SOURCE CONFIGURATION (NEW)
    # ------------------------------------------------------------------
    TEMPLATE_SOURCE_CHOICES = [
        ("inline", _("Inline Content")),
        ("file", _("Uploaded Files")),
        ("path", _("Template Path")),
        ("external", _("External URL")),
    ]

    template_source = models.CharField(
        max_length=20,
        choices=TEMPLATE_SOURCE_CHOICES,
        default="inline",
        verbose_name=_("Template Source"),
        help_text=_("Where the template content comes from."),
    )

    template_path = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Template Path"),
        help_text=_(
            "Django template path (e.g., 'emails/newsletter.html'). "
            "Used when template source is 'path'."
        ),
    )

    external_url = models.URLField(
        blank=True,
        verbose_name=_("External URL"),
        help_text=_(
            "External URL to fetch template from. Used when template source is 'external'."
        ),
    )

    # ------------------------------------------------------------------
    # SUBJECT & PREVIEW (TRANSLATED)
    # ------------------------------------------------------------------
    subject_template = models.CharField(
        max_length=255,
        verbose_name=_("Subject Template"),
        help_text=_(
            "Subject line template. Use {{ title }}, {{ site_name }}, {{ user_name }}, etc."
        ),
    )

    preview_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Preview Text"),
        help_text=_("Text preview shown in email clients (usually 85-100 characters)."),
    )

    # ------------------------------------------------------------------
    # TEMPLATE FILES & INLINE CONTENT (TRANSLATED)
    # ------------------------------------------------------------------
    html_file = models.FileField(
        upload_to="email_templates/html/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name=_("HTML Template File"),
        help_text=_("Upload a complete HTML email template file (.html, .htm)."),
    )

    css_file = models.FileField(
        upload_to="email_templates/css/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name=_("CSS Stylesheet File"),
        help_text=_("Upload a CSS file for styling (.css)."),
    )

    html_content = models.TextField(
        blank=True,
        verbose_name=_("Inline HTML Content"),
        help_text=_(
            "HTML markup with placeholders like {{ title }}, {{ content }}, "
            "{{ preview_text }}, {{ header_image_url }}, {{ unsubscribe_url }}, "
            "{{ site_url }}, {{ current_year }}."
        ),
    )

    css_content = models.TextField(
        blank=True,
        verbose_name=_("Inline CSS Styles"),
        help_text=_("Inline CSS styles (used if no CSS file is uploaded)."),
    )

    text_content = models.TextField(
        blank=True,
        verbose_name=_("Plain Text Content"),
        help_text=_("Plain text fallback for non-HTML email clients."),
    )

    # ------------------------------------------------------------------
    # VISUAL ASSETS (TRANSLATED)
    # ------------------------------------------------------------------
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Header Image"),
        help_text=_("Default header image for the email template."),
    )

    logo_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo Image"),
        help_text=_("Logo to display in the email header."),
    )

    footer_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Footer Image"),
        help_text=_("Image for the email footer (e.g., social media icons)."),
    )

    # ------------------------------------------------------------------
    # TEMPLATE METADATA & CONFIGURATION (TRANSLATED)
    # ------------------------------------------------------------------
    template_type = models.CharField(
        max_length=50,
        choices=[
            ("invitation", _("Invitation")),
            ("notification", _("Notification")),
            ("newsletter", _("Newsletter")),
            ("transactional", _("Transactional")),
            ("welcome", _("Welcome")),
            ("password_reset", _("Password Reset")),
            ("order_confirmation", _("Order Confirmation")),
            ("system_alert", _("System Alert")),
            ("campaign", _("Campaign")),
            ("promotional", _("Promotional")),
            ("abandoned_cart", _("Abandoned Cart")),
            ("receipt", _("Receipt")),
            ("feedback", _("Feedback")),
            ("announcement", _("Announcement")),
        ],
        default="newsletter",
        verbose_name=_("Template Type"),
        help_text=_("Category for organizing templates."),
    )

    language = models.CharField(
        max_length=10,
        default="en",
        choices=[
            ("en", _("English")),
            ("es", _("Spanish")),
            ("fr", _("French")),
            ("de", _("German")),
            ("it", _("Italian")),
            ("pt", _("Portuguese")),
            ("ru", _("Russian")),
            ("zh", _("Chinese")),
            ("ja", _("Japanese")),
            ("ar", _("Arabic")),
            ("ko", _("Korean")),
            ("hi", _("Hindi")),
            ("tr", _("Turkish")),
            ("nl", _("Dutch")),
            ("pl", _("Polish")),
        ],
        verbose_name=_("Language"),
        help_text=_("Primary language for this template."),
    )

    version = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Version"),
        help_text=_("Template version number."),
    )

    # ------------------------------------------------------------------
    # STATUS & BEHAVIOR (TRANSLATED)
    # ------------------------------------------------------------------
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Set as Default"),
        help_text=_("Mark as default template for this type."),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether this template can be used for sending emails."),
    )

    is_system = models.BooleanField(
        default=False,
        verbose_name=_("System Template"),
        help_text=_("System templates cannot be deleted or deactivated."),
    )

    is_draft = models.BooleanField(
        default=False,
        verbose_name=_("Is Draft"),
        help_text=_("Mark as draft - not ready for production use."),
    )

    # ------------------------------------------------------------------
    # ADVANCED SETTINGS (TRANSLATED)
    # ------------------------------------------------------------------
    reply_to_email = models.EmailField(
        blank=True,
        verbose_name=_("Reply-To Email"),
        help_text=_("Default reply-to address for emails using this template."),
    )

    from_email = models.EmailField(
        blank=True, verbose_name=_("From Email"), help_text=_("Default sender email address.")
    )

    from_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("From Name"),
        help_text=_("Display name for the sender."),
    )

    unsubscribe_url = models.URLField(
        blank=True,
        verbose_name=_("Unsubscribe URL"),
        help_text=_("Default unsubscribe link for newsletters."),
    )

    # ------------------------------------------------------------------
    # CATEGORIZATION & TAGGING
    # ------------------------------------------------------------------
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Category"),
        help_text=_(
            "Optional category for grouping templates (e.g., 'Marketing', 'Transactional')."
        ),
    )

    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Tags"),
        help_text=_("List of tags for filtering and organizing templates."),
    )

    # ------------------------------------------------------------------
    # CACHING & PERFORMANCE
    # ------------------------------------------------------------------
    cache_key = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Cache Key"),
        help_text=_("Auto-generated cache key for template rendering."),
    )

    last_rendered = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Rendered"),
        help_text=_("When this template was last rendered."),
    )

    render_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Render Count"),
        help_text=_("How many times this template has been rendered."),
    )

    # ------------------------------------------------------------------
    # PERFORMANCE METRICS
    # ------------------------------------------------------------------
    open_rate = models.FloatField(
        default=0.0,
        verbose_name=_("Open Rate"),
        help_text=_("Historical open rate percentage for this template."),
    )

    click_rate = models.FloatField(
        default=0.0,
        verbose_name=_("Click Rate"),
        help_text=_("Historical click rate percentage for this template."),
    )

    conversion_rate = models.FloatField(
        default=0.0,
        verbose_name=_("Conversion Rate"),
        help_text=_("Historical conversion rate percentage for this template."),
    )

    bounce_rate = models.FloatField(
        default=0.0,
        verbose_name=_("Bounce Rate"),
        help_text=_("Historical bounce rate percentage for this template."),
    )

    # ------------------------------------------------------------------
    # ORGANIZED PANELS WITH TRANSLATIONS
    # ------------------------------------------------------------------
    basic_info_panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
                FieldPanel("category"),
                FieldPanel("tags"),
            ],
            heading=_("Basic Information"),
        ),
    ]

    scheduling_panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("go_live_at"),
                        FieldPanel("expire_at"),
                    ]
                ),
                HelpPanel(
                    content=_(
                        "Schedule when this template should be active. "
                        "Leave empty for immediate/indefinite availability."
                    )
                ),
            ],
            heading=_("Scheduling"),
        ),
    ]

    source_panels = [
        MultiFieldPanel(
            [
                FieldPanel("template_source"),
                FieldRowPanel(
                    [
                        FieldPanel("template_path"),
                        FieldPanel("external_url"),
                    ]
                ),
                HelpPanel(
                    content=_(
                        "Choose template source: "
                        "<b>Inline Content</b> - Edit HTML/CSS directly; "
                        "<b>Uploaded Files</b> - Upload HTML/CSS files; "
                        "<b>Template Path</b> - Use Django template from filesystem; "
                        "<b>External URL</b> - Fetch template from external source."
                    )
                ),
            ],
            heading=_("Template Source"),
        ),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("html_file"),
                FieldPanel("css_file"),
                HelpPanel(
                    content=_(
                        "Upload HTML/CSS files. Files will automatically populate inline fields."
                    )
                ),
            ],
            heading=_("Upload Files"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("html_content"),
                FieldPanel("css_content"),
                FieldPanel("text_content"),
                HelpPanel(
                    content=_(
                        "Use placeholders like {{ variable_name }} for dynamic content. "
                        "Common variables: {{ title }}, {{ content }}, {{ user_name }}, "
                        "{{ site_url }}, {{ unsubscribe_url }}, {{ current_year }}."
                    )
                ),
            ],
            heading=_("Inline Content"),
        ),
    ]

    subject_panels = [
        MultiFieldPanel(
            [
                FieldPanel("subject_template"),
                FieldPanel("preview_text"),
            ],
            heading=_("Subject & Preview"),
        ),
    ]

    visual_panels = [
        MultiFieldPanel(
            [
                FieldPanel("header_image"),
                FieldPanel("logo_image"),
                FieldPanel("footer_image"),
            ],
            heading=_("Visual Assets"),
        ),
    ]

    configuration_panels = [
        MultiFieldPanel(
            [
                FieldPanel("template_type"),
                FieldPanel("language"),
                # FieldPanel("base_template"),
                FieldPanel("version"),
            ],
            heading=_("Template Configuration"),
        ),
    ]

    email_settings_panels = [
        # InlinePanel("variables", heading=_("Template Variables"), label=_("Variable")),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_email"),
                        FieldPanel("from_name"),
                    ]
                ),
                FieldPanel("reply_to_email"),
                FieldPanel("unsubscribe_url"),
            ],
            heading=_("Email Settings"),
        ),
    ]

    status_panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("is_default"),
                        FieldPanel("is_active"),
                        FieldPanel("is_system"),
                        FieldPanel("is_draft"),
                    ]
                ),
                HelpPanel(
                    content=_(
                        "Only one template per type can be set as default. "
                        "System templates are protected. Draft templates are not available for use."
                    )
                ),
            ],
            heading=_("Status & Behavior"),
        ),
    ]

    metrics_panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("open_rate", read_only=True),
                        FieldPanel("click_rate", read_only=True),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("conversion_rate", read_only=True),
                        FieldPanel("bounce_rate", read_only=True),
                    ]
                ),
                FieldPanel("render_count", read_only=True),
                FieldPanel("last_rendered", read_only=True),
                HelpPanel(
                    content=_(
                        "Performance metrics are automatically updated based on email campaigns. "
                        "These are read-only fields for monitoring template effectiveness."
                    )
                ),
            ],
            heading=_("Performance Metrics"),
        ),
    ]

    # ------------------------------------------------------------------
    # WAGTAIL TAB UI CONFIGURATION
    # ------------------------------------------------------------------
    edit_handler = TabbedInterface(
        [
            ObjectList(basic_info_panels, heading=_("Basic Info")),
            ObjectList(scheduling_panels, heading=_("Scheduling")),
            ObjectList(source_panels, heading=_("Source")),
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(subject_panels, heading=_("Subject")),
            ObjectList(visual_panels, heading=_("Visuals")),
            ObjectList(configuration_panels, heading=_("Configuration")),
            ObjectList(email_settings_panels, heading=_("Email Settings")),
            ObjectList(status_panels, heading=_("Status")),
            ObjectList(metrics_panels, heading=_("Metrics")),
            ObjectList(DefaultBase.promote_panels, heading=_("Promote")),
        ]
    )

    # ------------------------------------------------------------------
    # META CONFIG
    # ------------------------------------------------------------------
    class Meta:
        verbose_name = _("Email Template")
        verbose_name_plural = _("Email Templates")
        ordering = ["template_type", "name", "version"]
        # db_table = "email_templates"
        unique_together = ["template_type", "language", "is_default", "version"]
        indexes = [
            models.Index(fields=["template_type", "is_active"]),
            models.Index(fields=["language", "is_active"]),
            models.Index(fields=["is_default", "is_active"]),
            models.Index(fields=["template_source"]),
            models.Index(fields=["cache_key"]),
            models.Index(fields=["go_live_at"]),
            models.Index(fields=["expire_at"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_draft", "is_active"]),
        ]

    # ------------------------------------------------------------------
    # METHODS
    # ------------------------------------------------------------------
    def save(self, *args, **kwargs):
        """Ensure only one template is marked as default per type and language."""
        if self.is_default and not self.is_system:
            # Clear default flag for other templates of same type and language
            EmailTemplate.objects.filter(
                template_type=self.template_type,
                language=self.language,
                is_default=True,
            ).exclude(pk=self.pk).update(is_default=False)
        # Validate go_live_at and expire_at
        if self.go_live_at and self.expire_at and self.go_live_at >= self.expire_at:
            raise ValueError("go_live_at must be before expire_at")
        # Auto-generate slug from name if not set
        if not self.slug and self.name:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        # Generate cache key
        self.cache_key = self._generate_cache_key()
        super().save(*args, **kwargs)

    def _generate_cache_key(self):
        """Generate a unique cache key for this template."""
        import hashlib
        import json

        # Create a unique identifier based on template properties
        template_data = {
            "id": self.id,
            "name": self.name,
            "template_source": self.template_source,
            "template_path": self.template_path,
            "version": self.version,
            "updated_at": str(self.updated_at) if self.updated_at else "",
        }
        # Generate MD5 hash
        data_str = json.dumps(template_data, sort_keys=True)
        return f"template_{hashlib.md5(data_str.encode()).hexdigest()}"

    def delete(self, *args, **kwargs):
        """Prevent deletion of system templates."""
        if self.is_system:
            raise models.ProtectedError(_("Cannot delete system templates."), [self])
        super().delete(*args, **kwargs)

    def __str__(self):
        if self.template_source == "path" and self.template_path:
            return f"{self.name} ({self.template_path})"
        return f"{self.name} ({self.get_template_type_display()} - {self.get_language_display()})"

    # ------------------------------------------------------------------
    # PROPERTIES FOR STATUS CHECKING
    # ------------------------------------------------------------------
    @property
    def is_live(self):
        """Check if template is currently live based on scheduling."""
        now = timezone.now()
        # Check draft status
        if self.is_draft:
            return False
        # Check active status
        if not self.is_active:
            return False
        # Check scheduling
        if self.go_live_at and now < self.go_live_at:
            return False
        if self.expire_at and now > self.expire_at:
            return False

        return True

    @property
    def scheduled_status(self):
        """Get human-readable scheduling status."""
        now = timezone.now()
        if self.is_draft:
            return _("Draft")
        if not self.is_active:
            return _("Inactive")
        if self.go_live_at and now < self.go_live_at:
            days_until = (self.go_live_at - now).days
            return _("Scheduled (in {} days)").format(days_until)
        if self.expire_at and now > self.expire_at:
            return _("Expired")
        if self.go_live_at and self.expire_at:
            days_left = (self.expire_at - now).days
            return _("Active ({} days left)").format(days_left)
        return _("Active")

    @property
    def time_until_live(self):
        """Get time until template goes live (if scheduled)."""
        if self.go_live_at and timezone.now() < self.go_live_at:
            return self.go_live_at - timezone.now()
        return None

    @property
    def time_until_expire(self):
        """Get time until template expires (if scheduled)."""
        if self.expire_at and timezone.now() < self.expire_at:
            return self.expire_at - timezone.now()
        return None

    # ------------------------------------------------------------------
    # SCHEDULING METHODS
    # ------------------------------------------------------------------
    def schedule_for(self, go_live_at=None, expire_at=None):
        """Schedule template activation and expiration."""
        if go_live_at:
            self.go_live_at = go_live_at
        if expire_at:
            self.expire_at = expire_at
        self.save()

    def activate_immediately(self):
        """Activate template immediately (clear scheduling)."""
        self.go_live_at = None
        self.expire_at = None
        self.is_active = True
        self.is_draft = False
        self.save()

    def expire_immediately(self):
        """Expire template immediately."""
        self.expire_at = timezone.now()
        self.save()

    def mark_as_draft(self):
        """Mark template as draft."""
        self.is_draft = True
        self.save()

    def publish(self):
        """Publish template (clear draft status)."""
        self.is_draft = False
        self.save()

    # ------------------------------------------------------------------
    # FILE UPLOAD HANDLING METHODS
    # ------------------------------------------------------------------
    def update_html_from_file(self):
        """Read HTML file content and update the html_content field."""
        if self.html_file and self.html_file.name:
            try:
                self.html_file.open("r")
                content = self.html_file.read().decode("utf-8")
                self.html_content = content
                logger.info(f"Updated HTML content from file for template: {self.name}")
                return True
            except Exception as e:
                logger.error(f"Failed to read HTML file for template {self.name}: {str(e)}")
                return False
            finally:
                if hasattr(self.html_file, "close"):
                    self.html_file.close()
        return False

    def update_css_from_file(self):
        """Read CSS file content and update the css_content field."""
        if self.css_file and self.css_file.name:
            try:
                self.css_file.open("r")
                content = self.css_file.read().decode("utf-8")
                self.css_content = content
                logger.info(f"Updated CSS content from file for template: {self.name}")
                return True
            except Exception as e:
                logger.error(f"Failed to read CSS file for template {self.name}: {str(e)}")
                return False
            finally:
                if hasattr(self.css_file, "close"):
                    self.css_file.close()
        return False

    def create_file_from_content(self, file_type="html"):
        """Create a physical file from inline content."""
        if file_type == "html" and self.html_content and not self.html_file:
            filename = f"{self.slug or self.name.lower().replace(' ', '_')}.html"
            content_file = ContentFile(self.html_content.encode("utf-8"))
            self.html_file.save(filename, content_file, save=False)
            logger.info(f"Created HTML file from content for template: {self.name}")
            return True

        elif file_type == "css" and self.css_content and not self.css_file:
            filename = f"{self.slug or self.name.lower().replace(' ', '_')}.css"
            content_file = ContentFile(self.css_content.encode("utf-8"))
            self.css_file.save(filename, content_file, save=False)
            logger.info(f"Created CSS file from content for template: {self.name}")
            return True

        return False

    # ------------------------------------------------------------------
    # TEMPLATE RENDERING METHODS
    # ------------------------------------------------------------------
    def get_rendered_content(self, context=None, use_cache=True, validate_live=True):
        """
        Render the template with context based on template source.
        Returns dict with html, css, text, subject, preview_text
        """
        if validate_live and not self.is_live:
            raise ValueError(
                _("Template is not currently live. Status: {}").format(self.scheduled_status)
            )

        if context is None:
            context = {}

        # Check cache first
        if use_cache:
            cached = self._get_cached_rendering(context)
            if cached:
                return cached

        # Add default context
        default_context = self.get_default_context()
        default_context.update(context)

        # Get content based on template source
        if self.template_source == "path" and self.template_path:
            content = self._render_from_template_path(default_context)
        elif self.template_source == "external" and self.external_url:
            content = self._render_from_external_url(default_context)
        elif self.template_source == "file" and self.has_files:
            content = self._render_from_files(default_context)
        else:
            # Default to inline content
            content = self._render_from_inline(default_context)

        # Update render statistics
        self._update_render_stats()

        # Cache the rendering
        if use_cache:
            self._cache_rendering(content, context)

        return content

    def _render_from_template_path(self, context):
        """Render template from Django template path."""
        from django.template.loader import render_to_string

        try:
            # Render HTML from template path
            html_content = render_to_string(self.template_path, context)

            # Try to find corresponding CSS template
            css_path = self.template_path.replace(".html", ".css")
            css_content = ""
            try:
                css_content = render_to_string(css_path, context)
            except:
                # If no CSS template, use inline CSS
                css_content = self.css_content

            return {
                "html": html_content,
                "css": css_content,
                "text": self.text_content or self._generate_text_from_html(html_content),
                "subject": self._replace_placeholders(self.subject_template, context),
                "preview_text": self.preview_text,
            }
        except Exception as e:
            logger.error(f"Failed to render template from path {self.template_path}: {str(e)}")
            # Fallback to inline content
            return self._render_from_inline(context)

    def _render_from_external_url(self, context):
        """Fetch and render template from external URL."""
        import requests
        from django.template import Context, Template

        try:
            # Fetch template from external URL
            response = requests.get(self.external_url, timeout=10)
            response.raise_for_status()

            # Create Django template from response
            template = Template(response.text)
            html_content = template.render(Context(context))

            return {
                "html": html_content,
                "css": self.css_content,
                "text": self.text_content or self._generate_text_from_html(html_content),
                "subject": self._replace_placeholders(self.subject_template, context),
                "preview_text": self.preview_text,
            }
        except Exception as e:
            logger.error(f"Failed to fetch template from URL {self.external_url}: {str(e)}")
            # Fallback to inline content
            return self._render_from_inline(context)

    def _render_from_files(self, context):
        """Render template from uploaded files."""
        html_to_render = self.get_active_html()
        css_to_render = self.get_active_css()

        rendered_html = self._replace_placeholders(html_to_render, context)
        rendered_css = self._replace_placeholders(css_to_render, context)

        return {
            "html": rendered_html,
            "css": rendered_css,
            "text": self.text_content or self._generate_text_from_html(rendered_html),
            "subject": self._replace_placeholders(self.subject_template, context),
            "preview_text": self.preview_text,
        }

    def _render_from_inline(self, context):
        """Render template from inline content."""
        rendered_html = self._replace_placeholders(self.html_content, context)
        rendered_css = self._replace_placeholders(self.css_content, context)
        rendered_text = self._replace_placeholders(self.text_content, context)

        return {
            "html": rendered_html,
            "css": rendered_css,
            "text": rendered_text,
            "subject": self._replace_placeholders(self.subject_template, context),
            "preview_text": self.preview_text,
        }

    def _generate_text_from_html(self, html_content):
        """Generate plain text from HTML content."""
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            return text
        except ImportError:
            # Fallback: simple HTML tag removal
            import re

            text = re.sub(r"<[^>]*>", " ", html_content)
            text = re.sub(r"\s+", " ", text).strip()
            return text

    def _replace_placeholders(self, content, context):
        """Replace {{ placeholder }} with values from context."""
        if not content:
            return content

        from django.template import Context, Template

        try:
            template = Template(content)
            return template.render(Context(context))
        except:
            # Fallback: simple replacement
            for key, value in context.items():
                placeholder = f"{{{{{key}}}}}"
                content = content.replace(placeholder, str(value))
            return content

    def _update_render_stats(self):
        """Update rendering statistics."""
        from django.utils import timezone

        self.last_rendered = timezone.now()
        self.render_count += 1
        self.save(update_fields=["last_rendered", "render_count"])

    def _get_cached_rendering(self, context):
        """Get cached rendering for this context."""
        from django.core.cache import cache

        cache_key = f"{self.cache_key}_context_{self._get_context_hash(context)}"
        return cache.get(cache_key)

    def _cache_rendering(self, content, context):
        """Cache the rendering result."""
        from django.core.cache import cache

        cache_key = f"{self.cache_key}_context_{self._get_context_hash(context)}"
        cache_timeout = getattr(settings, "EMAIL_TEMPLATE_CACHE_TIMEOUT", 3600)  # 1 hour default
        cache.set(cache_key, content, cache_timeout)

    def _get_context_hash(self, context):
        """Generate hash for context dictionary."""
        import hashlib
        import json

        # Sort keys for consistent hashing
        sorted_context = json.dumps(context, sort_keys=True)
        return hashlib.md5(sorted_context.encode()).hexdigest()

    def get_default_context(self):
        """Get default context variables for template rendering."""
        from django.conf import settings
        from django.utils import timezone
        from wagtail.models import Site

        current_site = Site.find_for_request(None)

        return {
            "site_name": current_site.site_name
            if current_site
            else getattr(settings, "SITE_NAME", ""),
            "site_url": current_site.root_url
            if current_site
            else getattr(settings, "SITE_URL", ""),
            "current_year": timezone.now().year,
            "logo_url": self.logo_image.file.url
            if self.logo_image and self.logo_image.file
            else "",
            "header_image_url": self.header_image.file.url
            if self.header_image and self.header_image.file
            else "",
            "footer_image_url": self.footer_image.file.url
            if self.footer_image and self.footer_image.file
            else "",
            "unsubscribe_url": self.unsubscribe_url or "#",
            "template_name": self.name,
            "template_type": self.get_template_type_display(),
            "template": self,  # Reference to template instance
            "go_live_at": self.go_live_at,
            "expire_at": self.expire_at,
            "is_live": self.is_live,
        }

    def render_for_email(self, context=None, email_type=None, validate_live=True):
        """Render template for email sending."""
        rendered = self.get_rendered_content(context, validate_live=validate_live)

        # Combine HTML and CSS
        if rendered["css"]:
            # Insert CSS into HTML
            css_inserted = self._insert_css_into_html(rendered["html"], rendered["css"])
            final_html = css_inserted
        else:
            final_html = rendered["html"]

        return {
            "subject": rendered["subject"],
            "html": final_html,
            "text": rendered["text"],
            "preview_text": rendered["preview_text"],
            "from_email": self.from_email or getattr(settings, "DEFAULT_FROM_EMAIL", ""),
            "from_name": self.from_name,
            "reply_to": self.reply_to_email,
        }

    def _insert_css_into_html(self, html, css):
        """Insert CSS into HTML, either inline or in style tag."""
        from bs4 import BeautifulSoup

        try:
            soup = BeautifulSoup(html, "html.parser")

            # Check if there's already a style tag in head
            head = soup.find("head")
            if head:
                style_tag = soup.new_tag("style")
                style_tag.string = css
                head.append(style_tag)
            else:
                # Create head tag if it doesn't exist
                head = soup.new_tag("head")
                style_tag = soup.new_tag("style")
                style_tag.string = css
                head.append(style_tag)
                soup.html.insert(0, head)

            return str(soup)
        except:
            # Fallback: simple insertion
            return f"<style>{css}</style>\n{html}"

    # ------------------------------------------------------------------
    # OBJECT RENDERING METHODS
    # ------------------------------------------------------------------
    def render_for_object(self, obj, context=None, validate_live=True):
        """
        Render template for a specific object.

        Args:
            obj: The object to render template for
            context: Additional context
            validate_live: Check if template is live before rendering

        Returns:
            dict with rendered email content
        """
        if context is None:
            context = {}

        # Get object's default context if it has the method
        if hasattr(obj, "get_email_context"):
            obj_context = obj.get_email_context()
            context.update(obj_context)

        # Add object reference
        context["object"] = obj
        context["obj"] = obj

        # Render template
        return self.render_for_email(context, validate_live=validate_live)

    # ------------------------------------------------------------------
    # PERFORMANCE METRICS METHODS
    # ------------------------------------------------------------------
    def update_metrics(self, opens=0, clicks=0, conversions=0, bounces=0, deliveries=0):
        """Update template performance metrics."""
        if deliveries > 0:
            self.open_rate = (opens / deliveries) * 100
            self.click_rate = (clicks / deliveries) * 100
            self.conversion_rate = (conversions / deliveries) * 100
            self.bounce_rate = (bounces / deliveries) * 100

        self.save(update_fields=["open_rate", "click_rate", "conversion_rate", "bounce_rate"])

    def reset_metrics(self):
        """Reset all performance metrics to zero."""
        self.open_rate = 0.0
        self.click_rate = 0.0
        self.conversion_rate = 0.0
        self.bounce_rate = 0.0
        self.save(update_fields=["open_rate", "click_rate", "conversion_rate", "bounce_rate"])

    # ------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------
    @property
    def template_display_path(self):
        """Display the template path in a user-friendly way."""
        if self.template_source == "path" and self.template_path:
            return self.template_path
        elif self.template_source == "external" and self.external_url:
            return self.external_url
        elif self.template_source == "file" and self.has_files:
            return "Uploaded Files"
        else:
            return "Inline Content"

    @property
    def active_html(self):
        """Get active HTML content based on template source."""
        if self.template_source == "path" and self.template_path:
            try:
                from django.template.loader import get_template

                template = get_template(self.template_path)
                return template.template.source
            except:
                return self.html_content
        elif self.template_source == "file" and self.html_file:
            return self.get_active_html()
        else:
            return self.html_content

    @property
    def active_css(self):
        """Get active CSS content based on template source."""
        if self.template_source == "path" and self.template_path:
            # Try to find corresponding CSS template
            css_path = self.template_path.replace(".html", ".css")
            try:
                from django.template.loader import get_template

                template = get_template(css_path)
                return template.template.source
            except:
                return self.css_content
        elif self.template_source == "file" and self.css_file:
            return self.get_active_css()
        else:
            return self.css_content

    def get_active_html(self, use_files=True):
        """Get HTML content from files if available."""
        if use_files and self.html_file and self.html_file.name:
            try:
                self.html_file.open("r")
                content = self.html_file.read().decode("utf-8")
                return content
            except Exception:
                return self.html_content
            finally:
                if hasattr(self.html_file, "close"):
                    self.html_file.close()
        return self.html_content

    def get_active_css(self, use_files=True):
        """Get CSS content from files if available."""
        if use_files and self.css_file and self.css_file.name:
            try:
                self.css_file.open("r")
                content = self.css_file.read().decode("utf-8")
                return content
            except Exception:
                return self.css_content
            finally:
                if hasattr(self.css_file, "close"):
                    self.css_file.close()
        return self.css_content

    @property
    def file_info(self):
        """Get information about uploaded files."""
        info = {}
        if self.html_file:
            info["html"] = {
                "name": os.path.basename(self.html_file.name),
                "size": self.html_file.size,
                "url": self.html_file.url,
            }
        if self.css_file:
            info["css"] = {
                "name": os.path.basename(self.css_file.name),
                "size": self.css_file.size,
                "url": self.css_file.url,
            }
        return info

    @property
    def has_files(self):
        """Check if template has uploaded files."""
        return bool(self.html_file or self.css_file)

    @property
    def has_inline_content(self):
        """Check if template has inline content."""
        return bool(self.html_content or self.css_content or self.text_content)

    @property
    def is_scheduled(self):
        """Check if template has scheduling."""
        return bool(self.go_live_at or self.expire_at)

    @property
    def schedule_summary(self):
        """Get schedule summary."""
        if not self.go_live_at and not self.expire_at:
            return _("No scheduling")

        parts = []
        if self.go_live_at:
            parts.append(_("Goes live: {}").format(self.go_live_at.strftime("%Y-%m-%d %H:%M")))

        if self.expire_at:
            parts.append(_("Expires: {}").format(self.expire_at.strftime("%Y-%m-%d %H:%M")))

        return " | ".join(parts)

    # ------------------------------------------------------------------
    # CLASS METHODS
    # ------------------------------------------------------------------
    @classmethod
    def get_default_for_type(cls, template_type, language="en", include_scheduled=True):
        """Get default template for a specific type and language."""
        try:
            qs = cls.objects.filter(
                template_type=template_type,
                language=language,
                is_default=True,
                is_active=True,
                is_draft=False,
            )

            if not include_scheduled:
                # Exclude scheduled templates
                now = timezone.now()
                qs = qs.filter(
                    Q(go_live_at__isnull=True) | Q(go_live_at__lte=now),
                    Q(expire_at__isnull=True) | Q(expire_at__gte=now),
                )

            return qs.get()
        except cls.DoesNotExist:
            # Fallback to any active template of this type and language
            try:
                qs = cls.objects.filter(
                    template_type=template_type,
                    language=language,
                    is_active=True,
                    is_draft=False,
                ).order_by("-is_default", "-version", "-created_at")

                if not include_scheduled:
                    # Exclude scheduled templates
                    now = timezone.now()
                    qs = qs.filter(
                        Q(go_live_at__isnull=True) | Q(go_live_at__lte=now),
                        Q(expire_at__isnull=True) | Q(expire_at__gte=now),
                    )

                return qs.first()
            except cls.DoesNotExist:
                return None

    @classmethod
    def get_live_templates(cls, template_type=None, language=None):
        """Get all live templates, optionally filtered by type and language."""
        now = timezone.now()

        qs = cls.objects.filter(is_active=True, is_draft=False).filter(
            Q(go_live_at__isnull=True) | Q(go_live_at__lte=now),
            Q(expire_at__isnull=True) | Q(expire_at__gte=now),
        )

        if template_type:
            qs = qs.filter(template_type=template_type)

        if language:
            qs = qs.filter(language=language)

        return qs.order_by("template_type", "name")

    @classmethod
    def get_by_path(cls, template_path, language="en", include_scheduled=True):
        """Get template by Django template path."""
        try:
            qs = cls.objects.filter(template_path=template_path, language=language, is_active=True)

            if not include_scheduled:
                # Exclude scheduled templates
                now = timezone.now()
                qs = qs.filter(
                    Q(go_live_at__isnull=True) | Q(go_live_at__lte=now),
                    Q(expire_at__isnull=True) | Q(expire_at__gte=now),
                )

            return qs.get()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_system_template(cls, template_type, language="en"):
        """Get system template (creates if doesn't exist)."""
        try:
            return cls.objects.get(template_type=template_type, language=language, is_system=True)
        except cls.DoesNotExist:
            # Create a basic system template
            template = cls(
                name=f"System {template_type.title()} Template",
                template_type=template_type,
                language=language,
                is_system=True,
                is_active=True,
                is_draft=False,
                subject_template=f"{{{{ title }}}} - {{{{ site_name }}}}",  # noqa: F541
                html_content=cls._get_default_html_template(template_type),
                text_content=cls._get_default_text_template(template_type),
            )
            template.save()
            return template

    @classmethod
    def find_for_object(cls, obj, template_type=None, language=None, include_scheduled=True):
        """
        Find appropriate template for an object.

        Args:
            obj: The object
            template_type: Optional template type filter
            language: Optional language filter
            include_scheduled: Include scheduled templates

        Returns:
            EmailTemplate or None
        """
        # Determine template type from object if not provided
        if not template_type:
            model_name = obj._meta.model_name.lower()
            if "invitation" in model_name:
                template_type = "invitation"
            elif "newsletter" in model_name:
                template_type = "newsletter"
            elif "user" in model_name:
                template_type = "welcome"
            else:
                template_type = "notification"

        # Determine language from object if available
        if not language and hasattr(obj, "language"):
            language = obj.language

        return cls.get_default_for_type(template_type, language or "en", include_scheduled)

    @classmethod
    def cleanup_expired(cls):
        """Deactivate expired templates."""
        now = timezone.now()
        expired = cls.objects.filter(
            is_active=True,
            expire_at__lt=now,
            expire_at__isnull=False,
        )

        count = expired.count()
        expired.update(is_active=False)

        logger.info(f"Deactivated {count} expired email templates")
        return count

    @classmethod
    def activate_scheduled(cls):
        """Activate templates that have reached their go_live_at date."""
        now = timezone.now()
        scheduled = cls.objects.filter(
            is_active=False,
            go_live_at__lte=now,
            go_live_at__isnull=False,
        )

        count = scheduled.count()
        scheduled.update(is_active=True)

        logger.info(f"Activated {count} scheduled email templates")
        return count

    @classmethod
    def _get_default_html_template(cls, template_type):
        """Get default HTML template for a type."""
        templates = {
            "invitation": """<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background-color: #f8f9fa; padding: 20px; text-align: center; }
                    .content { padding: 30px; background-color: #fff; }
                    .footer { background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
                    .button { display: inline-block; padding: 12px 24px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>You're Invited!</h1>
                    </div>
                    <div class="content">
                        <p>Hello,</p>
                        <p>You've been invited to join {{ site_name }}.</p>
                        <p style="text-align: center; margin: 30px 0;">
                            <a href="{{ invitation_url }}" class="button">Accept Invitation</a>
                        </p>
                        <p>This invitation expires on {{ expiry_date }}.</p>
                        <p>Best regards,<br>The {{ site_name }} Team</p>
                    </div>
                    <div class="footer">
                        <p>&copy; {{ current_year }} {{ site_name }}. All rights reserved.</p>
                        <p><a href="{{ unsubscribe_url }}">Unsubscribe</a> | <a href="{{ site_url }}">Visit Website</a></p>
                    </div>
                </div>
            </body>
            </html>""",
            "newsletter": """<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
                    .container { max-width: 600px; margin: 0 auto; }
                    .header { background-color: #f8f9fa; padding: 20px; text-align: center; }
                    .content { padding: 30px; background-color: #fff; }
                    .article { margin-bottom: 30px; }
                    .footer { background-color: #343a40; color: #fff; padding: 20px; text-align: center; font-size: 12px; }
                    .unsubscribe { color: #6c757d; font-size: 11px; margin-top: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>{{ title }}</h1>
                        <p>{{ preview_text }}</p>
                    </div>
                    <div class="content">
                        {{ content }}
                    </div>
                    <div class="footer">
                        <p>&copy; {{ current_year }} {{ site_name }}. All rights reserved.</p>
                        <p class="unsubscribe">
                            <a href="{{ unsubscribe_url }}" style="color: #6c757d;">Unsubscribe from this list</a> |
                            <a href="{{ site_url }}" style="color: #6c757d;">Visit our website</a>
                        </p>
                    </div>
                </div>
            </body>
            </html>""",
        }
        return templates.get(
            template_type,
            """<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ title }}</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .content { background-color: #fff; padding: 30px; border-radius: 5px; }
                    .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="content">
                        <h1>{{ title }}</h1>
                        {{ content }}
                    </div>
                    <div class="footer">
                        <p>&copy; {{ current_year }} {{ site_name }}</p>
                    </div>
                </div>
            </body>
            </html>""",
        )

    @classmethod
    def _get_default_text_template(cls, template_type):
        """Get default text template for a type."""
        templates = {
            "invitation": """You're Invited!

            Hello,

            You've been invited to join {{ site_name }}.

            Accept your invitation here:
            {{ invitation_url }}

            This invitation expires on {{ expiry_date }}.

            Best regards,
            The {{ site_name }} Team

            ---
            {{ site_name }}
            {{ site_url }}

            Unsubscribe: {{ unsubscribe_url }}""",
            "newsletter": """{{ title }}

            {{ preview_text }}

            {{ content }}

            ---
            {{ site_name }}
            {{ site_url }}

            Unsubscribe: {{ unsubscribe_url }}""",
        }
        return templates.get(
            template_type,
            """{{ title }}

            {{ content }}

            ---
            {{ site_name }}
            {{ site_url }}""",
        )


# ------------------------------------------------------------------
# INLINE MODEL FOR TEMPLATE VARIABLES
# ------------------------------------------------------------------
class TemplateVariable(Orderable):
    """
    Reusable variables/placeholders for email templates.
    """

    # template = ParentalKey(
    #     EmailTemplate,
    #     on_delete=models.CASCADE,
    #     related_name='variables'
    # )

    name = models.CharField(
        max_length=50,
        verbose_name=_("Variable Name"),
        help_text=_("Name used in templates as {{ variable_name }}"),
    )

    description = models.CharField(
        max_length=200,
        verbose_name=_("Description"),
        help_text=_("What this variable represents"),
    )

    default_value = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Default Value"),
        help_text=_("Default value if not provided in context"),
    )

    is_required = models.BooleanField(
        default=False,
        verbose_name=_("Required"),
        help_text=_("This variable must be provided in context"),
    )

    variable_type = models.CharField(
        max_length=20,
        choices=[
            ("text", _("Text")),
            ("url", _("URL")),
            ("email", _("Email")),
            ("date", _("Date")),
            ("number", _("Number")),
            ("boolean", _("Boolean")),
            ("color", _("Color")),
            ("image", _("Image")),
            ("file", _("File")),
        ],
        default="text",
        verbose_name=_("Type"),
    )

    validation_regex = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Validation Regex"),
        help_text=_("Regular expression for validating this variable (optional)"),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("default_value"),
        FieldRowPanel(
            [
                FieldPanel("is_required"),
                FieldPanel("variable_type"),
            ]
        ),
        FieldPanel("validation_regex"),
    ]

    class Meta:
        verbose_name = _("Template Variable")
        verbose_name_plural = _("Template Variables")
        ordering = ["name"]

    def __str__(self):
        return f"{{{{ {self.name} }}}}"

    def validate_value(self, value):
        """Validate a value against this variable's constraints."""
        if self.is_required and not value:
            return False, _("This field is required")

        if self.validation_regex and value:
            import re

            if not re.match(self.validation_regex, str(value)):
                return False, _("Value does not match required format")

        # Type-specific validation
        if self.variable_type == "email" and value:
            import re

            if not re.match(r"[^@]+@[^@]+\.[^@]+", str(value)):
                return False, _("Invalid email address")

        elif self.variable_type == "url" and value:
            import re

            url_pattern = re.compile(
                r"^(https?://)?"  # http:// or https://
                r"([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"  # domain
                r"(:\d+)?"  # port
                r"(/.*)?$"  # path
            )
            if not url_pattern.match(str(value)):
                return False, _("Invalid URL")

        elif self.variable_type == "number" and value:
            try:
                float(value)
            except ValueError:
                return False, _("Must be a valid number")

        elif self.variable_type == "boolean" and value:
            if str(value).lower() not in ["true", "false", "0", "1", "yes", "no"]:
                return False, _("Must be a boolean value")

        elif self.variable_type == "color" and value:
            import re

            color_pattern = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
            if not color_pattern.match(str(value)):
                return False, _("Must be a valid hex color (e.g., #FF0000)")

        return True, ""
