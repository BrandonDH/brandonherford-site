# Developer workflow

Quick reference for running the site locally and pushing changes to production
(PythonAnywhere). Full production setup lives in
[DEPLOY_PYTHONANYWHERE.md](DEPLOY_PYTHONANYWHERE.md); this doc is the day-to-day
commands.

## Local development

```bash
cd /Users/brandonherford/Desktop/projectB/brandonherford-site
source venv/bin/activate
python manage.py runserver
```

Open http://127.0.0.1:8000 (site) and http://127.0.0.1:8000/admin (content).

Other commands you'll reach for locally:

```bash
python manage.py migrate               # apply model changes to your local db.sqlite3
python manage.py makemigrations        # after changing a model
python manage.py createsuperuser       # first-time admin login
python manage.py seed_content          # optional sample profile/content
python manage.py collectstatic         # only needed to sanity-check static output; not required with DEBUG=True
```

Local uses SQLite and `DEBUG=True` automatically — no `.env` needed unless you
want to override something (copy `.env.example` to `.env` if so).

## Production (PythonAnywhere)

You don't run these day-to-day — only when deploying a change (see workflow
below). From a PythonAnywhere **Bash console**:

```bash
cd ~/brandonherford-site
git pull
workon brandonherford-venv
pip install -r requirements.txt        # only if requirements.txt changed
python manage.py migrate               # only if models changed
python manage.py collectstatic --noinput
```

Then click **Reload** on the **Web** tab. Production settings come from
`~/brandonherford-site/.env` (`DEBUG=False`, `ALLOWED_HOSTS`, etc.) — see
`DEPLOY_PYTHONANYWHERE.md` for the one-time setup of that file, the virtualenv,
and the web app config.

## Feature development workflow (local → production)

1. **Branch locally**
   ```bash
   git checkout main && git pull
   git checkout -b feature/short-description
   ```

2. **Build and verify locally**
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```
   - If you changed a model: `python manage.py makemigrations` and commit the
     generated migration file(s) along with the model change.
   - Click through the affected page(s) and `/admin` at
     http://127.0.0.1:8000 before moving on.

3. **Commit and push the branch**
   ```bash
   git add -A
   git commit -m "Short description of the change"
   git push -u origin feature/short-description
   ```

4. **Merge to `main`**
   Open a PR on GitHub (recommended, even solo — gives you a diff to review),
   or merge directly:
   ```bash
   git checkout main
   git merge feature/short-description
   git push origin main
   ```

5. **Deploy to production** — on PythonAnywhere, in a Bash console:
   ```bash
   cd ~/brandonherford-site
   git pull
   workon brandonherford-venv
   pip install -r requirements.txt        # only if requirements.txt changed
   python manage.py migrate               # only if you added migrations
   python manage.py collectstatic --noinput
   ```
   Then hit **Reload** on the **Web** tab.

6. **Verify in production** — visit `https://YOURNAME.pythonanywhere.com` and
   spot-check the change, plus `/admin` if it touched a model.

7. **Clean up**
   ```bash
   git branch -d feature/short-description
   git push origin --delete feature/short-description
   ```

### Notes

- There's no staging environment yet — `main` **is** what you deploy. Keep
  feature branches short-lived and verify locally before merging.
- Content edits (posts, profile, portfolio items) go through `/admin` directly
  on production and don't need a deploy.
- If Python version or dependency issues come up on PythonAnywhere, see the
  **Notes / gotchas** section at the bottom of `DEPLOY_PYTHONANYWHERE.md`.
