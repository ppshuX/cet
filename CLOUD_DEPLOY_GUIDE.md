# Cloud Server Deployment Guide

## Current Issue
The cloud server is showing "Vue application not built" because the static files haven't been generated on the server yet.

## Solution Steps

### On Cloud Server (SSH to 47.121.137.60):

```bash
# 1. Connect to server
ssh acs@47.121.137.60

# 2. Navigate to project directory
cd ~/roamio

# 3. Pull latest code
git pull

# 4. Build Vue frontend
cd web
npm run build
cd ..

# 5. Collect static files (IMPORTANT!)
python manage.py collectstatic --noinput

# 6. Restart uWSGI
sudo pkill -f uwsgi
uwsgi --ini scripts/uwsgi.ini --daemonize uwsgi.log

# 7. Verify Nginx is running
sudo systemctl status nginx
# If not running: sudo systemctl start nginx
```

## Why This Is Needed?

1. **`npm run build`** - Compiles Vue source code into optimized static files
   - Output: `static/vue/` directory with compiled JS/CSS
   
2. **`collectstatic`** - Copies all static files to `staticfiles/` directory
   - Nginx serves files from `staticfiles/` NOT `static/`
   
3. **Restart uWSGI** - Reloads Django application with new code

## File Flow

```
web/src/ (Vue source)
    ↓ npm run build
static/vue/ (compiled files)
    ↓ collectstatic
staticfiles/vue/ (Nginx serves from here)
```

## Verification

After running these commands, visit:
- https://app7508.acapp.acwing.com.cn/

You should see the Vue application instead of "Vue application not built" message.

