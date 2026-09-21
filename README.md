# brandonherford.com

Personal site — landing page, blog, portfolio, and experience — built with
**Django** (server-rendered templates) and a light sprinkle of **Preact** (a
~4KB, no-build-step React) for interactive bits. Content is managed entirely
from the Django admin.

## Stack

- **Backend:** Django 6, Python 3.14
- **Frontend:** Django templates + vanilla CSS/JS, with Preact "islands" loaded
  from a CDN where interactivity helps (e.g. live blog search/filter). No npm,
  no build step.
- **Database:** SQLite in development (zero config); PostgreSQL in production
  (set `DATABASE_URL`).
- **Static files:** served by WhiteNoise, so no separate web server is needed.

## Project layout

```
config/        Django project settings & root URLs
core/          Home page + SiteProfile (your name, bio, links, resume)
blog/          Posts + tags (Markdown body, hero image, social sharing)
portfolio/     Projects
experience/    Jobs + skills (the resume page)
templates/     All page templates (base.html is the shared shell)
static/        css/, js/ (flocking animation, nav, share, blog-filter island)
media/         Uploaded images & files (git-ignored)
```

Apps map 1:1 to the nav (Home, Blog, Portfolio, Experience) so it's easy to
find where anything lives.

## Run it locally

```bash
source venv/bin/activate
python manage.py migrate
python manage.py seed_content      # optional: loads your profile + sample content
python manage.py createsuperuser   # create your admin login
python manage.py runserver
```

Then open http://127.0.0.1:8000 — and http://127.0.0.1:8000/admin to manage content.

## Writing a post

1. Go to `/admin`, log in.
2. **Blog → Posts → Add.** Write the body in Markdown, add a hero image and
   tags, set status to **Published**, save.
3. It appears on `/blog` and links share cleanly to social media (Open Graph +
   Twitter Card tags are generated automatically; the hero image becomes the
   preview image).

Edit your name, bio, social links, and resume PDF under **Core → Site profile**.

## Deploying (production notes)

1. Set env vars (see `.env.example`): `SECRET_KEY`, `DEBUG=False`,
   `ALLOWED_HOSTS`, `DATABASE_URL` (PostgreSQL), `CSRF_TRUSTED_ORIGINS`.
2. `pip install -r requirements.txt && pip install psycopg[binary] gunicorn`
3. `python manage.py collectstatic && python manage.py migrate`
4. Serve with `gunicorn config.wsgi`.

> Note: the previous static site lives in `brandon-productDesignManagement/`.
> This Django app supersedes it but needs a Python host (Railway, Render,
> Fly.io, a VPS) — GitHub Pages can't run Django.
