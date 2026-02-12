# Render.com Deployment Guide

This guide explains how to deploy the netproinfotech Django project to Render.com.

## Prerequisites
- GitHub account with this repository pushed
- Render.com account (sign up at https://render.com)

## Deployment Steps

### Step 1: Push to GitHub
Ensure your project is pushed to a GitHub repository:
```bash
git add .
git commit -m "Prepare for Render.com deployment"
git push origin main
```

### Step 2: Connect to Render.com

1. Go to https://dashboard.render.com
2. Click "New +" and select "Blueprint"
3. Select your GitHub repository
4. Name your service (e.g., "netproinfotech")
5. Click "Deploy"

Render will automatically read the `render.yaml` file and:
- Create a PostgreSQL database
- Deploy the Django web service
- Run migrations automatically
- Collect static files

### Step 3: Generate a Secret Key

The deployment needs a secure SECRET_KEY. Generate one:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use an online generator: https://djecrety.ir/

### Step 4: Set Environment Variables

In the Render Dashboard:
1. Go to your web service
2. Click "Environment" in the left sidebar
3. Add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | [Generated key from Step 3] | Keep this secret! |
| `DEBUG` | `False` | Production mode |
| `ALLOWED_HOSTS` | Your Render domain | e.g., `myapp.onrender.com` |
| `DATABASE_URL` | Automatically set | From PostgreSQL service |

The database connection is automatically set up by Render.

### Step 5: Create a Superuser

Connect to your deployed instance and create a superuser:

1. Go to your service dashboard
2. Click "Shell" tab
3. Run:
```bash
python manage.py createsuperuser
```
4. Follow the prompts to create an admin account

### Step 6: Access Your Application

- **App URL**: `https://yourapp.onrender.com`
- **Admin URL**: `https://yourapp.onrender.com/admin`

## File Structure

```
netproinfotech/
├── render.yaml              # Blueprint configuration
├── build.sh                 # Build commands
├── requirements.txt         # Updated with production dependencies
├── .env.example             # Environment variables reference
└── netproinfotech/
    └── settings.py          # Updated for production
```

## What Changed

### Dependencies Added
- `psycopg2-binary` - PostgreSQL adapter
- `gunicorn` - Production WSGI server
- `dj-database-url` - Database URL parsing

### Settings Updated
- Environment variable support for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- PostgreSQL support via `DATABASE_URL`
- WhiteNoise middleware for static files
- Secure static file handling

## Troubleshooting

### Database Connection Issues
- Ensure DATABASE_URL is set correctly in environment variables
- Check that the PostgreSQL service is running
- Verify migrations have run: Check logs for "Applied X migration(s)"

### Static Files Not Loading
- Run `python manage.py collectstatic` locally to test
- Check that `STATICFILES_STORAGE` is set correctly
- Verify static files are being served by WhiteNoise

### Superuser Login Issues
- Use the Shell in Render Dashboard to reset password:
```bash
python manage.py changepassword admin
```

### SSH/Shell Access
Click the "Shell" button on your service dashboard for direct access

## Production Checklist

- [ ] SECRET_KEY is set and unique
- [ ] DEBUG is set to False
- [ ] ALLOWED_HOSTS includes your Render domain
- [ ] DATABASE_URL is automatically set
- [ ] Admin user created
- [ ] Static files collecting successfully
- [ ] Database migrations applied
- [ ] Email configuration (if needed)

## Rolling Updates

To redeploy after code changes:
1. Push to GitHub
2. Render automatically detects changes and rebuilds

Or manually trigger:
1. Go to your service dashboard
2. Click "Manual Deploy" → "Latest Commit"

## Scaling

For production:
- Upgrade from free to paid plan
- Increase instance size if needed
- Enable auto-scaling

## Support

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
