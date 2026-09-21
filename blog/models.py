from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True,
                            help_text="Leave blank to auto-generate from the title.")
    summary = models.CharField(
        max_length=300,
        blank=True,
        help_text="One or two sentences shown in the blog list and social previews.",
    )
    body = models.TextField(help_text="Post content in Markdown. Images/embeds welcome.")

    hero_image = models.ImageField(upload_to="posts/", blank=True,
                                   help_text="Optional banner image shown at the top of the post.")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(default=timezone.now,
                                        help_text="Used for ordering and the displayed date.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["-published_at"]), models.Index(fields=["status"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.slug])

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
