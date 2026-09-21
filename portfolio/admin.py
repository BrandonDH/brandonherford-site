from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "featured", "published", "order")
    list_filter = ("featured", "published", "year")
    list_editable = ("featured", "published", "order")
    search_fields = ("title", "summary", "tech")
    prepopulated_fields = {"slug": ("title",)}
