"""Seed the site with Brandon's real profile plus a little starter content.

Idempotent: safe to run multiple times. Run with:  python manage.py seed_content
"""
from datetime import date

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import SiteProfile
from blog.models import Post, Tag
from portfolio.models import Project
from experience.models import Experience, Skill


class Command(BaseCommand):
    help = "Populate the database with an initial profile and sample content."

    def handle(self, *args, **options):
        profile = SiteProfile.get()
        profile.name = "Brandon Herford"
        profile.tagline = "Software developer building interfaces for the physical world."
        profile.bio = (
            "I build interfaces for monitoring **civil engineering** and the "
            "subsurface. I work in Python, JavaScript, and .NET Core, and I like "
            "the space where design, data, and the field meet.\n\n"
            "This is where I write about what I'm building and thinking about."
        )
        profile.location = "United States"
        profile.email = "brandonherford@gmail.com"
        profile.github_url = "https://github.com/BrandonDH"
        profile.dribbble_url = "https://dribbble.com/BrandonHerford"
        profile.save()
        self.stdout.write(self.style.SUCCESS("✓ Site profile"))

        # Skills
        skills = [
            ("Python", Skill.Category.LANGUAGE),
            ("JavaScript", Skill.Category.LANGUAGE),
            ("C# / .NET Core", Skill.Category.LANGUAGE),
            ("Django", Skill.Category.FRAMEWORK),
            ("React", Skill.Category.FRAMEWORK),
            ("p5.js", Skill.Category.FRAMEWORK),
            ("PostgreSQL", Skill.Category.TOOL),
            ("Git", Skill.Category.TOOL),
            ("Figma", Skill.Category.DESIGN),
        ]
        for i, (name, cat) in enumerate(skills):
            Skill.objects.get_or_create(name=name, defaults={"category": cat, "order": i})
        self.stdout.write(self.style.SUCCESS(f"✓ {len(skills)} skills"))

        # Experience (placeholder — edit in the admin)
        Experience.objects.get_or_create(
            role="Software Developer",
            company="GEO-Instruments",
            defaults={
                "company_url": "https://www.geo-instruments.com/",
                "start_date": date(2021, 1, 1),
                "end_date": None,
                "description": (
                    "Build and maintain interfaces for monitoring civil "
                    "engineering projects — turning subsurface sensor data into "
                    "tools people can act on."
                ),
                "order": 0,
            },
        )
        self.stdout.write(self.style.SUCCESS("✓ Experience entry"))

        # Sample project
        Project.objects.get_or_create(
            title="Flocking Study",
            defaults={
                "summary": "A p5.js iteration of Craig Reynolds' classic boids algorithm.",
                "description": "An interactive flocking simulation exploring emergent behavior.",
                "tech": "JavaScript, p5.js",
                "url": "https://brandonherford.com",
                "year": 2024,
                "featured": True,
                "order": 0,
            },
        )
        self.stdout.write(self.style.SUCCESS("✓ Sample project"))

        # Welcome post
        tag, _ = Tag.objects.get_or_create(name="Meta")
        post, created = Post.objects.get_or_create(
            slug="hello-world",
            defaults={
                "title": "Hello, world",
                "summary": "Why I built this site, and what I plan to write about here.",
                "body": (
                    "## A place to think out loud\n\n"
                    "I wanted a home for ideas that don't fit in a tweet — notes on "
                    "what I'm building, how I'm building it, and the odd tangent.\n\n"
                    "This site is a small **Django** app: server-rendered pages with "
                    "a sprinkle of React where it earns its keep. Simple to run, "
                    "simple to change.\n\n"
                    "> The best tools disappear into the work.\n\n"
                    "More soon."
                ),
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now(),
            },
        )
        if created:
            post.tags.add(tag)
        self.stdout.write(self.style.SUCCESS("✓ Welcome post"))

        self.stdout.write(self.style.SUCCESS("\nDone. Visit / to see the site."))
