from django.contrib import admin

from .models import Experience, Skill


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "order")
    list_editable = ("order",)
    search_fields = ("role", "company")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    list_editable = ("category", "order")
    search_fields = ("name",)
