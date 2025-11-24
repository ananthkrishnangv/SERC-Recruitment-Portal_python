# SERC Recruitment Portal Deployment Guide

## Overview
This document provides a step-by-step guide to deploy the **SERC Recruitment Portal** on an **Ubuntu 24.04** on-premises server using an existing SSL certificate and key.

---

## 1. Prerequisites
- Ubuntu 24.04 server
- Domain: `eos.serc.res.in`
- Existing SSL certificate and key files
- Git installed
- Python 3.12 (default on Ubuntu 24.04)
- Root or sudo access
- SSH access (port 2022)

Ensure DNS A record points `eos.serc.res.in` to your server IP.

---

## 2. Connect to Server
```bash
ssh -p 2022 root@14.139.176.60
```

---

## 3. System Update and Install Dependencies
```bash
apt update && apt -y upgrade
apt -y install git python3-venv python3-dev build-essential nginx logrotate
```

(Optional) Install DB packages if needed:
```bash
apt -y install postgresql postgresql-contrib libpq-dev
# or
apt -y install mysql-server default-libmysqlclient-dev
```

---

## 4. Create App User and Directory
```bash
adduser --system --group --home /var/www/sercapp sercapp
```

---

## 5. Clone Application Repository
```bash
sudo -u sercapp -H bash -c '
cd /var/www/sercapp
git clone https://github.com/ananthkrishnangv/SERC-Recruitment-Portal_python.git app
'
```

---

## 6. Setup Python Virtual Environment
```bash
sudo -u sercapp -H bash -c '
cd /var/www/sercapp/app
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
# or manually install gunicorn and other dependencies
# pip install gunicorn django psycopg2-binary
'
```

---

## 7. Configure Environment Variables
Create `/etc/sercapp.env`:
```bash
cat >/etc/sercapp.env <<'EOF'
DJANGO_SETTINGS_MODULE=project.settings.production
SECRET_KEY=change_me
DEBUG=False
ALLOWED_HOSTS=eos.serc.res.in,14.139.176.60
DATABASE_URL=postgres://dbuser:dbpass@localhost:5432/sercdb
EOF
chmod 640 /etc/sercapp.env
chown root:sercapp /etc/sercapp.env
```

---

## 8. Collect Static Files (Django)
```bash
sudo -u sercapp -H bash -c '
cd /var/www/sercapp/app
source .venv/bin/activate
python manage.py collectstatic --noinput
'
```

---

## 9. Configure Gunicorn with systemd
Create `/etc/systemd/system/sercapp.service`:
```ini
[Unit]
Description=SERC Recruitment Portal (Gunicorn)
After=network.target

[Service]
Type=simple
User=sercapp
Group=sercapp
EnvironmentFile=/etc/sercapp.env
WorkingDirectory=/var/www/sercapp/app
ExecStart=/var/www/sercapp/app/.venv/bin/gunicorn --workers 3 --bind unix:/run/sercapp.sock project.wsgi:application
Restart=always
RestartSec=5
RuntimeDirectory=sercapp
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
```
Enable and start service:
```bash
systemctl daemon-reload
systemctl enable --now sercapp
systemctl status sercapp
```

---

## 10. Configure Nginx with SSL
Place SSL files:
```bash
mkdir -p /etc/ssl/eos
cp /path/to/certificate.crt /etc/ssl/eos/eos.serc.res.in.crt
cp /path/to/private.key /etc/ssl/eos/eos.serc.res.in.key
chmod 600 /etc/ssl/eos/eos.serc.res.in.key
```

Create Nginx site `/etc/nginx/sites-available/eos.serc.res.in`:
```nginx
server {
    listen 80;
    server_name eos.serc.res.in;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name eos.serc.res.in;

    ssl_certificate     /etc/ssl/eos/eos.serc.res.in.crt;
    ssl_certificate_key /etc/ssl/eos/eos.serc.res.in.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location /static/ {
        alias /var/www/sercapp/app/static/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/sercapp.sock;
    }

    client_max_body_size 20M;
}
```
Enable site and reload:
```bash
ln -s /etc/nginx/sites-available/eos.serc.res.in /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## 11. Verify Deployment
```bash
curl -vk https://eos.serc.res.in
```
Check logs:
```bash
journalctl -u sercapp -f
```

---

## 12. Log Rotation
Create `/etc/logrotate.d/sercapp`:
```bash
/var/log/sercapp/*.log {
    weekly
    rotate 12
    missingok
    compress
    delaycompress
    notifempty
    create 0640 sercapp sercapp
    postrotate
        systemctl reload sercapp >/dev/null 2>&1 || true
    endscript
}
```

---

## 13. Update Application
```bash
sudo -u sercapp -H bash -c '
cd /var/www/sercapp/app
git pull
source .venv/bin/activate
pip install -r requirements.txt
'
systemctl restart sercapp
```

---

## Notes
- Replace paths for SSL files with actual locations.
- Adjust WSGI entry point if not Django.
- Ensure DNS and firewall allow ports 80 and 443.
