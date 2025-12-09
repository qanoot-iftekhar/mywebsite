# PythonAnywhere Deployment Guide

## 📋 Pre-Deployment Checklist

✅ Code pushed to GitHub  
✅ `requirements.txt` fixed (no duplicates)  
✅ WSGI configuration ready  
✅ Static files configured  

---

## 🚀 Deployment Steps

### 1️⃣ Clone Repository on PythonAnywhere

```bash
# PythonAnywhere Console में
git clone https://github.com/YOUR_USERNAME/mywebsite.git
cd mywebsite
```

### 2️⃣ Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 mywebsite-env
pip install -r requirements.txt
```

### 3️⃣ Create .env File

```bash
nano .env
```

Add the following:
```bash
SECRET_KEY=your-super-secret-random-key-here
DEBUG=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=Footwear Store <noreply@footwearstore.com>
```

> **💡 Secret Key generate karne ke liye:**
> ```python
> from django.core.management.utils import get_random_secret_key
> print(get_random_secret_key())
> ```

### 4️⃣ Run Migrations & Collect Static Files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5️⃣ Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 6️⃣ Configure Web App on PythonAnywhere

**Web Tab → Add a new web app:**
- Framework: **Manual configuration**
- Python version: **3.10**

**WSGI Configuration File:**

Click on the WSGI configuration file link and replace content with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/mywebsite'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'mywebsite.settings'

# Load environment variables from .env file
from pathlib import Path
env_path = Path(path) / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Static Files Mapping:**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/mywebsite/static/` |
| `/media/` | `/home/YOUR_USERNAME/mywebsite/media/` |

**Virtualenv Path:**
```
/home/YOUR_USERNAME/.virtualenvs/mywebsite-env
```

### 7️⃣ Reload Web App

Click **Reload** button on Web tab

---

## ✅ Verification

Visit your site: `https://YOUR_USERNAME.pythonanywhere.com`

- ✅ Homepage loads
- ✅ Static files (CSS/JS) working
- ✅ Product images showing
- ✅ Admin panel accessible at `/admin`

---

## 🔧 Troubleshooting

### Static files not loading?
```bash
python manage.py collectstatic --noinput
# Then reload web app
```

### Server error?
Check error logs on PythonAnywhere:
- Web tab → Error log
- Server log

### Database issues?
```bash
python manage.py migrate
python manage.py check
```

### Update code after changes?
```bash
cd ~/mywebsite
git pull
python manage.py collectstatic --noinput
# Then click Reload on Web tab
```

---

## 📝 Important Notes

1. **DEBUG=False** in production (.env file)
2. **SECRET_KEY** must be different from development
3. **Media files** upload to `/media/` directory
4. **Database** is SQLite - file at `db.sqlite3`
5. **Free tier** limits: 100MB storage, one web app

---

## 🎯 Next Steps After Deployment

1. Add products via `/admin`
2. Test checkout process
3. Configure email (if needed)
4. Set up custom domain (optional, paid feature)

---

## 📧 Email Configuration (Optional)

For Gmail:
1. Enable 2-Step Verification
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Add to `.env`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   ```
