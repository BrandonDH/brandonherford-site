import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_MD_EXTENSIONS = ["extra", "fenced_code", "codehilite", "toc", "nl2br", "sane_lists"]


@register.filter(name="markdown")
def markdown_filter(text):
    """Render Markdown text to HTML.

    Content comes only from the admin (trusted authors), so we allow raw HTML
    for embeds (e.g. YouTube iframes, social share widgets) within posts.
    """
    if not text:
        return ""
    html = md.markdown(text, extensions=_MD_EXTENSIONS, output_format="html5")
    return mark_safe(html)
