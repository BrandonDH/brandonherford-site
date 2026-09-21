from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    summary = models.CharField(max_length=280, blank=True,
                               help_text="Short description shown on the portfolio card.")
    description = models.TextField(blank=True, help_text="Full write-up (Markdown supported).")

    image = models.ImageField(upload_to="portfolio/", blank=True)
    url = models.URLField(blank=True, help_text="Live site / demo link.")
    source_url = models.URLField(blank=True, help_text="Source code link (e.g. GitHub).")

    tech = models.CharField(max_length=240, blank=True,
                            help_text="Comma-separated tech, e.g. 'Django, p5.js, PostgreSQL'.")
    year = models.PositiveIntegerField(blank=True, null=True)

    featured = models.BooleanField(default=False, help_text="Featured projects surface on the home page.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-year", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:180]
        super().save(*args, **kwargs)

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech.split(",") if t.strip()]
