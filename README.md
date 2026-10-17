# Project Attachments Management System

A small Django + PostgreSQL + Bootstrap application with staff registration, email verification, admin approval, project attachments, and a permission-aware worldwide Leaflet map.

## Features

- Staff registration and signed email-verification links (24-hour expiry)
- Administrator approval of accounts via Django Admin
- Projects with optional latitude/longitude
- Project list, search, status/department filters
- Leaflet worldwide map with authorized project markers and live project counts
- Project membership roles: manager, contributor, viewer
- Attachment upload and permission-checked downloads
- PostgreSQL support and optional S3-compatible storage

## Local development

1. Install Python 3.11+.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and set environment variables in your shell. Django does not automatically read `.env` files in this starter.
5. For local development, leave `DEBUG=True` and use SQLite by default.
6. Run:

   ```bash
   python manage.py makemigrations accounts projects attachments
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/`.

For local email testing, set `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` in `config/settings.py`; verification links will print in the runserver terminal. For real verification emails, configure SMTP variables.

## Important first setup

- Create a superuser with `python manage.py createsuperuser`.
- Log into `/admin/`.
- Approve a registered user in **User profiles** after their email is verified.
- Add project members in the Project Membership admin section. Staff users see only projects where they are members; staff/superusers can see all projects.
- Project owners and project managers can edit project metadata. Contributors can upload files. Viewers can view and download files.

## Production deployment

1. Push this source code to the institution's existing GitHub repository.
2. Create a hosted Django web service and managed PostgreSQL database (the included `render.yaml` is a starting point).
3. Configure `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `SITE_URL`, and SMTP credentials as environment variables.
4. Configure persistent S3-compatible object storage for uploaded files by setting `USE_S3=True` and the AWS-compatible storage environment variables. Do not rely on a host's temporary filesystem for production uploads.
5. Run migrations and create a superuser using the host's shell or one-off command.
6. Update the `render.yaml` hostname placeholders to the real service hostname.
7. Use HTTPS and test account verification, approval, project permissions, and downloads before inviting staff.

## Security and production checklist

This is a starter scaffold and should be reviewed before handling confidential institutional data. In particular:

- Configure SMTP and test verification links end-to-end.
- Use private object storage; do not make the storage bucket public.
- Set `DEBUG=False`, strong secrets, allowed hosts, HTTPS, and trusted origins.
- Configure backup and restoration for PostgreSQL and object storage.
- Add malware scanning and stricter MIME/content validation if the institution will accept untrusted uploads.
- Review institutional email-domain restrictions and account approval policies.
- Review privacy, retention, and audit requirements.
- For public-facing use, consider rate limiting registration/login and adding an audit log.

## Notes

- Map markers are returned only for projects visible to the logged-in user.
- Coordinates are validated: latitude from -90 to 90; longitude from -180 to 180.
- Counts reflect projects visible to the current user, not hidden projects belonging to others.
- The app uses a simple project-membership access model. The institution can adjust it to its exact policy.
