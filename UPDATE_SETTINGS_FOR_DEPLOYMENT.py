"""
Instructions for updating netproinfotech/settings.py for deployment

COPY THE FOLLOWING CODE AND ADD IT TO YOUR settings.py FILE
"""

# ============================================================================
# ADD THIS AT THE TOP OF settings.py (AFTER IMPORTS)
# ============================================================================

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# MODIFY THESE SETTINGS IN YOUR settings.py
# ============================================================================

# DEBUG - Change to False in production
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# SECRET_KEY - Use environment variable
SECRET_KEY = os.getenv('SECRET_KEY', 'your-insecure-secret-key-change-this')

# ALLOWED_HOSTS - Add your domain
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ============================================================================
# STATIC FILES CONFIGURATION (For Production)
# ============================================================================

# Add this section
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================================
# MIDDLEWARE (Add whitenoise for static files in production)
# ============================================================================

# Add this at the top of MIDDLEWARE list (after SecurityMiddleware):
# 'whitenoise.middleware.WhiteNoiseMiddleware',

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ADD THIS LINE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================================
# DATABASE (Optional: Use PostgreSQL in production)
# ============================================================================

# Current (SQLite):
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For production with PostgreSQL (uncomment and update):
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.config(
#         default='sqlite:///db.sqlite3',
#         conn_max_age=600
#     )
# }

# ============================================================================
# SECURITY SETTINGS (For Production)
# ============================================================================

# Uncomment these for production:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'

# ============================================================================
# DEPLOYMENTS CHECKLIST
# ============================================================================

"""
Before deploying, ensure you have:

1. ✓ Created .env file with production values
2. ✓ Updated DEBUG = False
3. ✓ Set a strong SECRET_KEY
4. ✓ Added your domain to ALLOWED_HOSTS
5. ✓ Run migrations: python manage.py migrate
6. ✓ Collect static files: python manage.py collectstatic --noinput
7. ✓ Run checks: python manage.py check --deploy
8. ✓ Install gunicorn: pip install gunicorn
9. ✓ Install whitenoise: pip install whitenoise

Then deploy using Procfile and your chosen platform.
"""
