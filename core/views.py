from django.shortcuts import render

from blog.models import Post
from portfolio.models import Project


def home(request):
    context = {
        "recent_posts": Post.objects.filter(status=Post.Status.PUBLISHED)[:3],
        "featured_projects": Project.objects.filter(published=True, featured=True)[:3],
    }
    return render(request, "core/home.html", context)
