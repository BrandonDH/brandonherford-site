from .models import SiteProfile


def site_globals(request):
    """Expose the site profile and primary nav to every template."""
    return {
        "site": SiteProfile.get(),
        "main_nav": [
            {"label": "Home", "url_name": "core:home"},
            {"label": "Blog", "url_name": "blog:list"},
            {"label": "Portfolio", "url_name": "portfolio:list"},
            {"label": "Experience", "url_name": "experience:list"},
        ],
    }
