from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Post, Tag


def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).prefetch_related("tags")

    # Optional server-side filtering (no-JS fallback for the React island).
    query = request.GET.get("q", "").strip()
    tag_slug = request.GET.get("tag", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(body__icontains=query))
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    tags = Tag.objects.filter(posts__status=Post.Status.PUBLISHED).distinct()

    # Serialized data for the client-side Preact island (full, unfiltered set so
    # filtering happens instantly in the browser).
    all_posts = Post.objects.filter(status=Post.Status.PUBLISHED).prefetch_related("tags")
    posts_json = [
        {
            "title": p.title,
            "url": p.get_absolute_url(),
            "summary": p.summary,
            "date": p.published_at.strftime("%b %-d, %Y"),
            "iso_date": p.published_at.strftime("%Y-%m-%d"),
            "tags": [t.slug for t in p.tags.all()],
        }
        for p in all_posts
    ]
    tags_json = [{"slug": t.slug, "name": t.name} for t in tags]

    context = {
        "posts": posts,
        "tags": tags,
        "active_tag": tag_slug,
        "query": query,
        "posts_json": posts_json,
        "tags_json": tags_json,
    }
    return render(request, "blog/list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.prefetch_related("tags"),
        slug=slug,
        status=Post.Status.PUBLISHED,
    )
    return render(request, "blog/detail.html", {"post": post})
