from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
)
from wagtail.fields import StreamField
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
)
from wagtail.search import index

from django_grep.components.blocks import ContactMethodsStreamBlock
from django_grep.components.blocks.contact.socialLinks import SocialLinkBlock
from django_grep.components.blocks.contact.websiteLinks import ContactProfileBlock

LANGUAGE_CODE = settings.LANGUAGE_CODE


# =======================================
# WEBSITE SETTINGS
# =======================================
class SiteSettings(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    ClusterableModel,
    index.Indexed,
):
    """
    Global website branding, metadata, and visual identity settings.
    """

    # --- Branding ---
    site_name = models.CharField(
        _("Site Name"),
        max_length=150,
        default="Xellent Hub",
        help_text=_("Main brand name used across the website."),
    )
    tagline = models.CharField(
        _("Tagline"),
        max_length=255,
        blank=True,
        default="Empowering Digital Transformation",
        help_text=_("Short descriptive slogan displayed near logo or headers."),
    )
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
    )
    favicon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Favicon"),
        help_text=_("Small icon used in browser tabs and bookmarks."),
    )

    # --- Language & Status ---
    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default="en",
        verbose_name=_("Language Code"),
        help_text=_("Language code for these settings (e.g., 'en', 'fr')."),
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_("Active"),
        help_text=_(
            "Designates whether these settings are active for this language. Only one active per language."
        ),
    )

    # --- SEO / META ---
    title_suffix = models.CharField(
        verbose_name=_("Title suffix"),
        max_length=255,
        help_text=_("Suffix for <title> tag, e.g. ' | Company Name'"),
        default=" | Xellent Hub",
    )
    meta_description = models.TextField(
        _("META description"),
        blank=True,
        default="Xellent Hub delivers innovative web, mobile, and cloud-based digital solutions for forward-thinking businesses.",
    )
    meta_keywords = models.TextField(
        _("META Keywords"),
        blank=True,
        default="Xellent, digital transformation, software, AI, technology, innovation",
    )
    meta_author = models.CharField(
        _("META Author"),
        max_length=255,
        blank=True,
        default="Xellent Hub Team",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("language"),
                        FieldPanel("active"),
                    ]
                ),
            ],
            heading=_("Language Configuration"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("site_name"),
                FieldPanel("tagline"),
                FieldPanel("logo"),
                FieldPanel("favicon"),
            ],
            heading=_("Brand Identity"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_suffix"),
                FieldPanel("meta_description"),
                FieldPanel("meta_keywords"),
                FieldPanel("meta_author"),
            ],
            heading=_("SEO & Meta Information"),
        ),
    ]

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")
        constraints = [
            models.UniqueConstraint(
                fields=["language"],
                condition=models.Q(active=True),
                name="unique_active_site_settings_per_language",
            ),
        ]

    def __str__(self):
        status = "✓" if self.active else "✗"
        return f"{self.site_name} Settings ({self.get_language_display()}) {status}"

    def clean(self):
        """Validate that only one active setting exists per language."""
        from django.core.exceptions import ValidationError

        super().clean()

        if self.active:
            # Check if another active setting exists for the same language
            existing_active = SiteSettings.objects.filter(
                language=self.language, active=True
            ).exclude(pk=self.pk)

            if existing_active.exists():
                raise ValidationError(
                    {
                        "active": f"Another active SiteSettings already exists for language {self.get_language_display()}."
                    }
                )

    def save(self, *args, **kwargs):
        # Ensure only one active setting per language
        if self.active:
            # Deactivate all other settings for this language
            SiteSettings.objects.filter(language=self.language, active=True).exclude(
                pk=self.pk
            ).update(active=False)

        super().save(*args, **kwargs)

    # --- Helpers ---
    def get_logo_image(self):
        """Return logo image instance."""
        return self.logo

    def get_brand_context(self):
        """Return key brand details for templates."""
        return {
            "name": self.site_name,
            "tagline": self.tagline,
            "logo": self.logo,
            "favicon": self.favicon,
            "language": self.language,
            "is_active": self.active,
        }

    @classmethod
    def get_active_for_language(cls, language_code):
        """
        Get active site settings for a specific language.

        Args:
            language_code: Language code (e.g., 'en', 'fr')

        Returns:
            SiteSettings instance or None
        """
        try:
            return cls.objects.get(language=language_code, active=True)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_active_for_request(cls, request=None):
        """
        Get active site settings for the current request with language fallback.

        Priority:
        1. Active settings for exact language code
        2. Active settings for language prefix (e.g., 'en' for 'en-us')
        3. First active settings found (as fallback)
        """
        # Get language from request
        language = getattr(request, "LANGUAGE_CODE", LANGUAGE_CODE)

        # Try exact language match
        settings = cls.get_active_for_language(language)
        if settings:
            return settings

        # Try language prefix if different from full language code
        if "-" in language:
            language_prefix = language.split("-")[0]
            settings = cls.get_active_for_language(language_prefix)
            if settings:
                return settings

        # Fallback to any active settings (first one)
        try:
            return cls.objects.filter(active=True).first()
        except cls.DoesNotExist:
            return cls.activate_language(language_prefix)

    @classmethod
    def get_default(cls):
        """Get the first active settings as default."""
        try:
            return cls.objects.filter(active=True).first()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all_active(cls):
        """Get all active settings, organized by language."""
        return {
            settings.language: settings
            for settings in cls.objects.filter(active=True).order_by("language")
        }

    @classmethod
    def get_available_languages(cls):
        """Get list of languages with active settings."""
        return list(cls.objects.filter(active=True).values_list("language", flat=True).distinct())

    @classmethod
    def activate_language(cls, language_code):
        """
        Activate settings for a specific language.
        If settings don't exist for that language, create default ones.
        """
        try:
            # Try to get existing settings for this language
            settings = cls.objects.get(language=language_code)
            settings.active = True
            settings.save()
            return settings
        except cls.DoesNotExist:
            # Create default settings for this language
            default_settings = cls.get_default()
            if default_settings:
                # Clone default settings for new language
                settings = cls.objects.create(
                    language=language_code,
                    active=True,
                    site_name=default_settings.site_name,
                    tagline=default_settings.tagline,
                    logo=default_settings.logo,
                    favicon=default_settings.favicon,
                    title_suffix=default_settings.title_suffix,
                    meta_description=default_settings.meta_description,
                    meta_keywords=default_settings.meta_keywords,
                    meta_author=default_settings.meta_author,
                )
                return settings
        return None


# =======================================
# SOCIAL & CONTACT SETTINGS
# =======================================
class SocialSettings(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    ClusterableModel,
    index.Indexed,
):
    """Site-wide contact details, social profiles, and communication channels."""

    # --- Contact Info ---
    description = models.TextField(
        blank=True,
        verbose_name=_("Footer Description"),
        default="We connect innovation with strategy — empowering brands to grow through technology.",
    )
    phone_number = models.CharField(
        max_length=24,
        blank=True,
        verbose_name=_("Phone number"),
        default="+1 800 123 4567",
    )
    whatsapp_number = models.CharField(
        max_length=24,
        blank=True,
        verbose_name=_("WhatsApp number"),
        help_text=_("Optional WhatsApp business contact."),
        default="+1 800 765 4321",
    )
    email = models.EmailField(
        blank=True,
        verbose_name=_("Email"),
        default="info@xellenthub.com",
    )
    support_email = models.EmailField(
        blank=True,
        verbose_name=_("Support Email"),
        default="support@xellenthub.com",
    )
    address = models.TextField(
        blank=True,
        verbose_name=_("Address"),
        default="123 Innovation Drive, San Francisco, CA 94105",
    )
    google_maps_link = models.URLField(
        blank=True,
        verbose_name=_("Google Maps Link"),
        help_text=_("Optional map link for location directions."),
    )
    organisation_url = models.URLField(
        verbose_name=_("Organisation URL"),
        blank=True,
        default="https://www.xellenthub.com",
    )
    additional_info = models.TextField(
        verbose_name=_("Additional Information"),
        blank=True,
        default="Open Monday – Friday, 9:00am – 6:00pm (PST).",
    )

    # --- Social Media ---
    social_links = StreamField(
        [("link", SocialLinkBlock())],
        use_json_field=True,
        verbose_name=_("Social links"),
        blank=True,
        help_text=_("Add links to your social media profiles"),
    )

    # --- Language & Status ---
    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default="en",
        verbose_name=_("Language Code"),
        help_text=_("Language code for these settings (e.g., 'en', 'fr')."),
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_("Active"),
        help_text=_(
            "Designates whether these settings are active for this language. Only one active per language."
        ),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("language"),
                        FieldPanel("active"),
                    ]
                ),
            ],
            heading=_("Language Configuration"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("description"),
                FieldRowPanel([FieldPanel("phone_number"), FieldPanel("whatsapp_number")]),
                FieldRowPanel([FieldPanel("email"), FieldPanel("support_email")]),
                FieldPanel("address"),
                FieldPanel("google_maps_link"),
                FieldPanel("organisation_url"),
                FieldPanel("additional_info"),
            ],
            heading=_("Contact & Organisation Info"),
        ),
        FieldPanel("social_links"),
    ]

    class Meta:
        verbose_name = _("Social & Contact Settings")
        verbose_name_plural = _("Social & Contact Settings")
        constraints = [
            models.UniqueConstraint(
                fields=["language"],
                condition=models.Q(active=True),
                name="unique_active_social_settings_per_language",
            ),
        ]

    def __str__(self):
        status = "✓" if self.active else "✗"
        return f"Social Settings ({self.get_language_display()}) {status}"

    def clean(self):
        """Validate that only one active setting exists per language."""
        from django.core.exceptions import ValidationError

        # logger.debug("side clean working...")
        super().clean()
        if self.active:
            # Check if another active setting exists for the same language
            existing_active = SocialSettings.objects.filter(
                language=self.language, active=True
            ).exclude(pk=self.pk)

            if existing_active.exists():
                raise ValidationError(
                    {
                        "active": f"Another active SocialSettings already exists for language {self.get_language_display()}."
                    }
                )

    def save(self, *args, **kwargs):
        # Ensure only one active setting per language
        if self.active:
            # Deactivate all other settings for this language
            SocialSettings.objects.filter(language=self.language, active=True).exclude(
                pk=self.pk
            ).update(active=False)

        super().save(*args, **kwargs)

    @classmethod
    def get_active_for_language(cls, language_code):
        """Get active social settings for a specific language."""
        try:
            return cls.objects.get(language=language_code, active=True)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_active_for_request(cls, request):
        """
        Get active social settings for the current request with language fallback.
        """
        # Get language from request
        language = getattr(request, "LANGUAGE_CODE", LANGUAGE_CODE)

        # Try exact language match
        settings = cls.get_active_for_language(language)
        if settings:
            return settings

        # Try language prefix if different from full language code
        if "-" in language:
            language_prefix = language.split("-")[0]
            settings = cls.get_active_for_language(language_prefix)
            if settings:
                return settings

        # Fallback to any active settings (first one)
        try:
            return cls.objects.filter(active=True).first()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_default(cls):
        """Get the first active settings as default."""
        try:
            return cls.objects.filter(active=True).first()
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all_active(cls):
        """Get all active social settings."""
        return {
            settings.language: settings
            for settings in cls.objects.filter(active=True).order_by("language")
        }

    # --- Helpers ---
    def get_social_links(self):
        """Return structured list of valid social links."""
        return [block.value for block in self.social_links if block.value.get("url")]

    def get_contact_info(self):
        """Return contact details for rendering."""
        return {
            "phone": self.phone_number,
            "whatsapp": self.whatsapp_number,
            "email": self.email,
            "support": self.support_email,
            "address": self.address,
            "maps_link": self.google_maps_link,
            "organisation": self.organisation_url,
            "additional_info": self.additional_info,
            "language": self.language,
        }


