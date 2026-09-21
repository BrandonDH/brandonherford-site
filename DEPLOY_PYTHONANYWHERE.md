# Deploying to PythonAnywhere (free tier)

A step-by-step for getting this Django site live at
`https://YOURNAME.pythonanywhere.com`. The free tier is always-on, has a
persistent filesystem (so SQLite + uploaded images just work), and includes
free HTTPS. Custom domains (e.g. brandonherford.com) require a paid plan.

> Replace **YOURNAME** everywhere below with your PythonAnywhere username.
> Use **Python 3.13** — Django 6.1 needs Python 3.12+.

---

## 1. Get the code onto PythonAnywhere

The cleanest way is via GitHub. Locally, from the project root:

```bash
cd /Users/brandonherford/Desktop/projectB/brandonherford-site
git init
git add .
git commit -m "Initial Django site"
# create an empty repo on github.com first, then:
git remote add origin https://github.com/BrandonDH/brandonherford-site.git
git branch -M main
git push -u origin main
```

The whole repo is just this `brandonherford-site/` folder — nothing else from
projectB is included. `.gitignore` also excludes `venv/`, `db.sqlite3`, `.env`,
`media/`, and `.claude/`.

Then on PythonAnywhere, open a **Bash console** (Consoles tab) and clone it:

```bash
git clone https://github.com/BrandonDH/brandonherford-site.git
```

(No GitHub? You can instead zip the project — minus `venv/` — and upload it via
the **Files** tab, then unzip in a Bash console.)

---

## 2. Create the virtualenv and install dependencies

In the Bash console:

```bash
cd ~/brandonherford-site
mkvirtualenv --python=/usr/bin/python3.13 brandonherford-venv
pip install -r requirements.txt
```

`mkvirtualenv` leaves the env **activated** (prompt shows `(brandonherford-venv)`).
Note the path it created: `/home/YOURNAME/.virtualenvs/brandonherford-venv` — you'll
need it in step 4.

---

## 3. Create your production `.env`

Generate a secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Create `~/brandonherford-site/.env` (via the Files tab or `nano .env`) with:

```
SECRET_KEY=paste-the-generated-key-here
DEBUG=False
ALLOWED_HOSTS=YOURNAME.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://YOURNAME.pythonanywhere.com
TIME_ZONE=America/New_York
```

(No `DATABASE_URL` needed — it falls back to SQLite, which persists here.)

---

## 4. Set up the web app

1. Go to the **Web** tab → **Add a new web app**.
2. Choose **Manual configuration** (NOT "Django") → **Python 3.13**.
3. Back on the Web tab, fill in:
   - **Source code:** `/home/YOURNAME/brandonherford-site`
   - **Working directory:** `/home/YOURNAME/brandonherford-site`
   - **Virtualenv:** `/home/YOURNAME/.virtualenvs/brandonherford-venv`

4. Click the **WSGI configuration file** link and **replace its entire
   contents** with:

   ```python
   import os
   import sys

   path = "/home/YOURNAME/brandonherford-site"
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

   Save it. (Settings reads your `.env` automatically, so no env vars needed here.)

---

## 5. Migrate, seed, collect static, create your login

Back in the Bash console (with the venv active):

```bash
cd ~/brandonherford-site
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser        # your real admin login
python manage.py seed_content           # optional: loads profile + sample content
```

---

## 6. Map static & media URLs (Web tab → "Static files")

Add these two mappings so images and CSS are served correctly (required because
`DEBUG=False`):

| URL        | Directory                              |
|------------|----------------------------------------|
| `/static/` | `/home/YOURNAME/brandonherford-site/staticfiles`  |
| `/media/`  | `/home/YOURNAME/brandonherford-site/media`         |

The `/media/` mapping is what serves the images you upload through the admin.

---

## 7. Reload

Click the big green **Reload** button on the Web tab, then visit
`https://YOURNAME.pythonanywhere.com`. Admin is at `/admin/`.

---

## Updating the site later

```bash
cd ~/brandonherford-site
git pull
workon brandonherford-venv
pip install -r requirements.txt        # only if deps changed
python manage.py migrate               # only if models changed
python manage.py collectstatic --noinput
```

Then hit **Reload** on the Web tab. That's it.

---

## Notes / gotchas

- **Python version:** must be 3.12+ for Django 6.1. If PythonAnywhere doesn't
  offer 3.12/3.13 on your account, tell me and I'll pin the project to Django
  5.2 LTS, which supports Python 3.10+.
- **CDN assets** (Preact, p5.js, Google Fonts) load in the visitor's browser,
  not on the server, so the free tier's outbound-traffic whitelist doesn't
  affect them.
- **Static files** are also handled by WhiteNoise as a fallback, but the Web-tab
  mapping above is faster and is what serves `/media/` uploads.
