"""
Django settings for Brandon Herford's site (blog + portfolio + resume).

Reads configuration from environment variables (see .env.example) so the same
codebase runs on SQLite in development and PostgreSQL in production by changing
a single DATABASE_URL value.
"""

from pathlib import Path

import dj_database_url
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from a .env file if present (optional in dev).
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in ("1", "true", "yes", "on")


# --- Core security -----------------------------------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-key-change-me-in-production-)g&h-y#r893=jq@4",
)
DEBUG = env_bool("DEBUG", True)
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]


# --- Applications ------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "martor",  # Markdown editor for the admin (toolbar, live preview, image upload)
    # Local apps (one per nav section, easy to reason about).
    "core",
    "blog",
    "portfolio",
    "experience",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Makes the site profile + nav available on every page.
                "core.context_processors.site_globals",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Database ----------------------------------------------------------------
# Defaults to SQLite (zero config, great for development/MVP). Set DATABASE_URL
# to a postgres:// URL in production, e.g.
#   DATABASE_URL=postgres://user:pass@localhost:5432/brandon
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}


# --- Password validation -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- I18N --------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "America/New_York")
USE_I18N = True
USE_TZ = True


# --- Static & media ----------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise: serve compressed static files without a separate web server.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Martor (Markdown editor) ------------------------------------------------
# Matches the markdown extensions used by core.templatetags.markdown_tags so the
# live preview looks like the published post.
MARTOR_THEME = "bootstrap"
MARTOR_ENABLE_CONFIGS = {
    "emoji": "true",       # enable :emoji: shortcodes
    "imgur": "true",       # show the image-upload toolbar button
    "mention": "false",
    "jquery": "true",      # martor bundles the jQuery it needs
    "living": "false",     # off = preview on demand (click), not on every keystroke
    "spellcheck": "false",
    "hljs": "true",        # syntax highlighting in code blocks
}
MARTOR_TOOLBAR_BUTTONS = [
    "bold", "italic", "horizontal", "heading", "pre-code", "blockquote",
    "unordered-list", "ordered-list", "link", "image-link", "image-upload",
    "emoji", "toggle-maximize", "help",
]
# Upload images to OUR /media/ instead of Imgur (see blog.views.martor_uploader).
MARTOR_UPLOAD_URL = "/blog/martor/uploader/"
MARTOR_MARKDOWN_BASE_MENTION_URL = ""
# Server-side markdown preview extensions (mirror the display filter).
MARTOR_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.fenced_code",
    "markdown.extensions.codehilite",
    "markdown.extensions.nl2br",
    "markdown.extensions.sane_lists",
]

# --- Email -------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
