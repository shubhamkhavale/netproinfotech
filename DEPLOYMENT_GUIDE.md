# Deployment and Incident Guide

This guide focuses on recovery for auth/login incidents and on safe Render deployments.

## Production recovery checklist

1. Reproduce and capture the traceback in Render logs.
2. Open Render Shell and run:

```bash
python --version
python manage.py check
python manage.py showmigrations accounts auth sessions
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'], settings.DATABASES['default']['NAME'])"
python manage.py migrate --noinput
python manage.py shell -c "from django.contrib.auth import authenticate; print(authenticate(username='probe_user', password='probe_pass'))"
python manage.py shell -c "from apps.accounts.models import User; print(User.objects.count())"
```

3. If logs show missing table/relation drift (for example `accounts_user` missing), backup first, then use:

```bash
python manage.py migrate accounts zero --fake
python manage.py migrate accounts --fake-initial
python manage.py migrate --noinput
```

4. If logs show DB connection/auth issues, verify `DATABASE_URL` is bound to `netproinfotech-db`, restart DB if needed, and re-run migrations.

## Deploy behavior

- Build phase:
  - install dependencies
  - collect static files
- Runtime startup:
  - run `python manage.py migrate --noinput`
  - start Gunicorn

This ensures migration failure blocks startup instead of serving a partially-ready app.

## Smoke test (internal)

Run after deploy or restart:

```bash
python tools/smoke_auth.py --base-url https://netproinfotech.onrender.com
```

Pass criteria:
- `GET /accounts/login/` is `200`
- `POST /accounts/login/` with invalid credentials is non-500

## Notes

- No public health endpoint is added.
- Use Render logs for root-cause detail and this runbook for safe, repeatable recovery.
