# swe1-app

A Django polls app for NYU SWE coursework, following tutorial Parts 1–4. Visitors can choose a poll, vote, and view results. Polls and choices are managed through Django admin.

Built with Python 3.14 and Django 5.2.

## Run locally

From the project folder on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On a fresh checkout, create a private local key once:

```bash
python -c "from pathlib import Path; import secrets; Path('.django-secret-key').open('x').write(secrets.token_urlsafe(50))"
chmod 600 .django-secret-key
```

Then create the database and admin account, and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [the polls page](http://127.0.0.1:8000/polls/) or [Django admin](http://127.0.0.1:8000/admin/). Add questions and their choices through admin; the local database and sample polls are not included in Git.

## Deployment

AWS deployment uses the configuration in `.ebextensions/`. Supply a separate `DJANGO_SECRET_KEY` and set `DJANGO_ALLOWED_HOSTS` to the AWS hostname. Debug mode is disabled on AWS. Deployment creates the database, adds three example polls only when no polls exist, and collects static files.

The single-server SQLite database lives outside the deployed code so ordinary deployments preserve votes. Replacing the server requires a database backup to keep its data. Secrets and local databases are excluded from Git.
