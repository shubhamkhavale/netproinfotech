# NetPro Infotech - Deployment Guide

## Quick Start - Deploy to PythonAnywhere (Recommended for Beginners)

### Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com/
2. Click "Create a Beginner account" (Free)
3. Sign up with email

### Step 2: Upload Your Code
1. In PythonAnywhere Dashboard → Files
2. Create a new folder: `netproinfotech`
3. Upload your project files OR use Git:

```bash
# Via Git (Recommended)
git clone https://github.com/YOUR-USERNAME/netproinfotech.git
```

### Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.11 netproinfotech
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Configure Web App
1. Go to "Web" tab → Add a new web app
2. Choose "Manual configuration" → Python 3.11
3. Set source code folder: `/home/your-username/netproinfotech`
4. Set virtualenv: `/home/your-username/.virtualenvs/netproinfotech`

### Step 5: Configure WSGI File
Edit the WSGI file at `/var/www/your_username_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

path = '/home/your-username/netproinfotech'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'netproinfotech.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Run Migrations
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 7: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 8: Update Django Settings
Edit `netproinfotech/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-username.pythonanywhere.com', 'localhost']
```

### Step 9: Reload Web App
- Go to "Web" tab
- Click the green "Reload" button

✅ Your site is now live at: `https://your-username.pythonanywhere.com/`

---

## Alternative: Deploy to Render.com

### Step 1: Prepare Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Push to GitHub
1. Create GitHub repo
2. Push your code:
```bash
git remote add origin https://github.com/YOUR-USERNAME/netproinfotech.git
git branch -M main
git push -u origin main
```

### Step 3: Connect to Render
1. Go to https://render.com/
2. Sign up with GitHub
3. Click "Create +" → "Web Service"
4. Connect your GitHub repo
5. Fill in settings:
   - **Name**: netproinfotech
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn netproinfotech.wsgi:application`

### Step 4: Set Environment Variables
In Render dashboard → Environment:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-app.onrender.com
```

✅ Your site will be live at: `https://your-app.onrender.com/`

---

## Easy Code Changes from Anywhere

### Option 1: Via PythonAnywhere Web Editor
1. Login to PythonAnywhere
2. Files → Click on any file to edit
3. Edit directly in browser
4. Click "Save"
5. Reload web app

### Option 2: Via Git + GitHub (Best Practice)
```bash
# On your local machine or any computer
git clone https://github.com/YOUR-USERNAME/netproinfotech.git
cd netproinfotech

# Make changes
# Edit files as needed

# Push changes
git add .
git commit -m "Description of changes"
git push origin main

# On PythonAnywhere/Render
git pull origin main
python manage.py collectstatic --noinput
# Reload web app
```

### Option 3: Direct SSH Access
```bash
# Connect via SSH (PythonAnywhere)
ssh your-username@ssh.pythonanywhere.com

# Navigate to project
cd ~/netproinfotech

# Make edits and restart
```

---

## Database Options

### SQLite (Current - File-based)
- ✅ Good for small projects
- ✅ No setup required
- ❌ Limited for multiple users
- Location: `db.sqlite3`

### PostgreSQL (Recommended for Production)
1. Create PostgreSQL database on Heroku/Render
2. Update `requirements.txt`:
```
psycopg2-binary==2.9.9
```

3. Update settings.py:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='postgresql://...')
}
```

---

## Security Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Use strong `SECRET_KEY` (at least 50 characters)
- [ ] Set `ALLOWED_HOSTS` correctly
- [ ] Use HTTPS only
- [ ] Store `.env` file securely (never commit to Git)
- [ ] Use environment variables for sensitive data
- [ ] Keep dependencies updated: `pip list --outdated`
- [ ] Run `python manage.py check --deploy`

---

## Troubleshooting

### 502 Bad Gateway Error
- Check error log in PythonAnywhere
- Ensure all dependencies installed
- Check WSGI configuration
- Reload web app

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Locked
```bash
# Remove old db file and migrate fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Permission Denied
```bash
# Ensure correct permissions
chmod -R 755 ~/netproinfotech
```

---

## Updating Your Code from Anywhere

### Via Browser (Easiest)
1. PythonAnywhere Dashboard
2. Files → Edit in browser
3. Make changes, Save
4. Web → Reload

### Via Git from Any Device
1. Make changes on laptop/phone browser/tablet
2. Push to GitHub: `git push`
3. Pull on server: `git pull`
4. Reload app

### Via Email/Cloud
1. Edit file locally
2. Upload to Google Drive/Dropbox
3. Download on server
4. Replace and reload

---

## Performance Tips

1. **Enable Caching**:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Compress Static Files**:
```bash
python manage.py compress
```

3. **Monitor Logs**:
- PythonAnywhere: Web tab → View logs
- Render: Logs section in dashboard

---

## Support & Resources

- PythonAnywhere Docs: https://help.pythonanywhere.com/
- Render Docs: https://render.com/docs/
- Django Docs: https://docs.djangoproject.com/
- Heroku Docs: https://devcenter.heroku.com/

---

**Your app is production-ready!** 🚀
