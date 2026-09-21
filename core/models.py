from django.db import models


class SiteProfile(models.Model):
    """Site-wide identity and links. Intended as a single row (a singleton),
    editable from the admin so you never touch templates to change your bio."""

    name = models.CharField(max_length=120, default="Brandon Herford")
    tagline = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short one-liner shown under your name on the home page.",
    )
    bio = models.TextField(
        blank=True,
        help_text="Longer intro (Markdown supported) for the home page.",
    )
    location = models.CharField(max_length=120, blank=True)

    # Contact / social
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    dribbble_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True, help_text="Full URL to your X/Twitter profile.")

    # Files & media
    resume = models.FileField(upload_to="resume/", blank=True, help_text="PDF resume.")
    avatar = models.ImageField(upload_to="profile/", blank=True)
    og_image = models.ImageField(
        upload_to="og/",
        blank=True,
        help_text="Default social-share preview image (1200x630 recommended).",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return self.name

    @classmethod
    def get(cls):
        """Return the profile row, creating a default one if none exists."""
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj
