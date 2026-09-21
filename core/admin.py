from django.contrib import admin

from .models import SiteProfile


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("name", "tagline", "bio", "location", "avatar")}),
        ("Contact & social", {"fields": ("email", "github_url", "dribbble_url", "linkedin_url", "twitter_url")}),
        ("Files & sharing", {"fields": ("resume", "og_image")}),
    )

    def has_add_permission(self, request):
        # Only one profile row should exist.
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
