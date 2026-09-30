import os
import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Post, Tag

# Image uploads accepted from the martor editor.
_ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/gif", "image/webp", "image/svg+xml"}
_MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


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


@staff_member_required
@require_POST
def martor_uploader(request):
    """Save an image dropped/uploaded in the martor editor into our own /media/
    and return its URL. Replaces martor's default Imgur uploader so post images
    live on this site. Restricted to staff (post authors)."""
    image = request.FILES.get("markdown-image-upload")
    if image is None:
        return JsonResponse({"status": 400, "error": "No file received."}, status=400)
    if image.size > _MAX_UPLOAD_BYTES:
        return JsonResponse({"status": 400, "error": "Image is larger than 10 MB."}, status=400)
    if image.content_type not in _ALLOWED_IMAGE_TYPES:
        return JsonResponse({"status": 400, "error": "Unsupported image type."}, status=400)

    # Namespace by date and give a unique prefix to avoid collisions/overwrites.
    base, ext = os.path.splitext(image.name)
    safe_name = f"{uuid.uuid4().hex[:8]}{ext.lower()}"
    path = f"posts/inline/{timezone.now():%Y/%m}/{safe_name}"
    saved_path = default_storage.save(path, ContentFile(image.read()))

    return JsonResponse(
        {"status": 200, "link": default_storage.url(saved_path), "name": base},
        status=200,
    )
