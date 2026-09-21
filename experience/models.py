from django.db import models


class Experience(models.Model):
    """A job / role for the Experience (resume) page."""

    role = models.CharField(max_length=160)
    company = models.CharField(max_length=160)
    company_url = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if this is your current role.")

    description = models.TextField(blank=True,
                                   help_text="What you did / achievements (Markdown supported).")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"

    @property
    def is_current(self):
        return self.end_date is None


class Skill(models.Model):
    class Category(models.TextChoices):
        LANGUAGE = "language", "Language"
        FRAMEWORK = "framework", "Framework / Library"
        TOOL = "tool", "Tool"
        DESIGN = "design", "Design"
        OTHER = "other", "Other"

    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name
