from itertools import groupby

from django.shortcuts import render

from .models import Experience, Skill


def experience_list(request):
    skills = list(Skill.objects.all())
    skills_by_category = [
        (Skill.Category(cat).label, list(items))
        for cat, items in groupby(skills, key=lambda s: s.category)
    ]
    context = {
        "experiences": Experience.objects.all(),
        "skills_by_category": skills_by_category,
    }
    return render(request, "experience/list.html", context)
