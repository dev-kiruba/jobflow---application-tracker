# Job Application Tracker

A full-stack web app to track job applications — company, role, status,
dates, and notes — with a dashboard showing upcoming deadlines. Built with
Django (handles frontend, backend, and database together), MySQL, and
deployed as a single live app on Railway.

## Why this exists

Tracking job applications in a spreadsheet gets messy fast. This gives each
application a status (Applied → Interviewing → Offer / Rejected /
Withdrawn), a next-action date, and a dashboard that surfaces what needs
attention in the next two weeks.

## Tech stack

- **Django** — handles routing, business logic, and renders the HTML pages
  directly (no separate frontend framework)
- **MySQL** — stores users and applications
- **PyMySQL** — pure-Python MySQL driver (avoids native build tools some
  Windows setups struggle with)
- **Whitenoise** — serves CSS/static files in production without a separate
  file host
- **Gunicorn** — production web server (used when deployed; `runserver` is
  used locally)

## Project structure

```
job_tracker/
├── manage.py
├── job_tracker/            # project settings & routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/                 # the actual app
│   ├── models.py               # Application model
│   ├── forms.py                 # ModelForm + registration form
│   ├── views.py                  # dashboard, CRUD views
│   ├── urls.py
│   ├── admin.py
│   ├── templates/tracker/        # all HTML pages
│   └── static/tracker/style.css
├── requirements.txt
├── .env.example
└── Procfile                  # tells Railway/Render how to run this in production
```

## Local setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Create the database:
```sql
mysql -u root -p
CREATE DATABASE job_tracker_db;
EXIT;
```

Configure environment:
```bash
copy .env.example .env
```
Edit `.env` and set `DB_PASSWORD` to your MySQL password, and generate a
real `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Create the database tables (Django's equivalent of `Base.metadata.create_all`,
but versioned — this is what Alembic does for SQLAlchemy):
```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin account (optional, lets you use `/admin`):
```bash
python manage.py createsuperuser
```

Run it:
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** — sign up, log in, and start adding
applications.

## Deploying live (Railway)

1. Push this project to GitHub (same process as the expense tracker).
2. Create a Railway account at railway.app and start a **New Project**.
3. Choose **Deploy from GitHub repo** and select this repository.
4. Add a **MySQL** database plugin from Railway's marketplace inside the
   same project — it will generate its own connection details.
5. In your web service's **Variables** tab, set the same variables as your
   `.env` file (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS` set to your
   Railway domain, and the `DB_*` variables copied from the MySQL plugin's
   connection info).
6. Railway automatically detects the `Procfile` and runs `gunicorn`, plus
   the migration on each deploy.
7. Once deployed, Railway gives you a public URL like
   `job-tracker-production.up.railway.app` — this is the link you can send
   to anyone, including an interviewer.

## Features

- Register / login / logout (Django's built-in auth system)
- Add, edit, delete job applications
- Filter applications by status
- Dashboard with per-status counts and a 14-day upcoming deadlines view
- Per-user data isolation — every query is scoped to `request.user`
