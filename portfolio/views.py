from django.shortcuts import render

from .models import Project


def project_list(request):
    projects = Project.objects.filter(published=True)
    return render(request, "portfolio/list.html", {"projects": projects})
