
# SERC Recruitment Portal — README

> **Project**: SERC-Recruitment-Portal (Python)
> **Domain**: `eos.serc.res.in`
> **Target Platform**: Ubuntu 24.04 (Noble)

This README consolidates **features** and **detailed files & folder structures** across **versions v1 → v3** of the SERC Recruitment Portal. It is intended to serve as a single source of truth for developers, DevOps, QA, and stakeholders.

> **Note:** This document is a structured template. Please replace all `TODO` placeholders with the exact details from your repository (or provide access so we can auto-populate). Sections are organized to make future updates simple and auditable.

---

## Table of Contents
1. [Overview](#overview)
2. [Architecture & Tech Stack](#architecture--tech-stack)
3. [Version-by-Version Summary](#version-by-version-summary)
4. [Detailed Feature Lists](#detailed-feature-lists)
    - [v1 Features](#v1-features)
    - [v2 Features](#v2-features)
    - [v3 Features](#v3-features)
5. [Files & Folder Structure](#files--folder-structure)
    - [v1 Structure](#v1-structure)
    - [v2 Structure](#v2-structure)
    - [v3 Structure](#v3-structure)
6. [Configuration & Environment](#configuration--environment)
7. [Database & Migrations](#database--migrations)
8. [API Endpoints](#api-endpoints)
9. [Build & Release](#build--release)
10. [Operations (Runbook)](#operations-runbook)
11. [Security & Compliance](#security--compliance)
12. [Testing & Quality](#testing--quality)
13. [Contributing](#contributing)
14. [Changelog](#changelog)

---

## Overview
**SERC Recruitment Portal** is a paperless recruitment system supporting end‑to‑end workflows for job postings, applications, screening, shortlisting, scheduling, and finalization. It is built in **Python** (framework: **TODO: Django/Flask/FastAPI**), served via **Gunicorn** behind **Nginx**, and secured with an **existing SSL certificate**.

Key objectives:
- Centralized applicant tracking & evaluation
- Secure data handling aligned with institutional policies
- Role‑based access control (RBAC) for Admin/Recruiter/Applicant
- Reliable deployments and auditability

---

## Architecture & Tech Stack
- **Language**: Python 3.12
- **Framework**: **TODO** (Django/Flask/FastAPI)
- **WSGI/ASGI**: **TODO** (Gunicorn/Uvicorn) — systemd managed
- **Web Server**: Nginx (reverse proxy)
- **Database**: **TODO** (PostgreSQL/MySQL/SQLite)
- **Caching/Queue**: **TODO** (Redis/Celery if applicable)
- **Frontend**: **TODO** (HTML/CSS/JS/Tailwind/Bootstrap)
- **ORM**: **TODO** (Django ORM/SQLAlchemy)
- **Auth**: **TODO** (session/JWT/2FA)
- **Email/SMS**: **TODO** (SMTP gateway/Twilio/etc.)

> See `INSTALLATION.md` for deployment steps and production configuration.

---

## Version-by-Version Summary

### v1 — Initial Release
- **Release Date**: **TODO**
- **Focus**: Baseline portal with core recruitment workflows.
- **Highlights**: **TODO**

### v2 — Enhancements & Integrations
- **Release Date**: **TODO**
- **Focus**: Performance, RBAC enhancements, reporting.
- **Highlights**: **TODO**

### v3 — Production Readiness & Scaling
- **Release Date**: **TODO**
- **Focus**: Ops hardening, scalability, audit & compliance.
- **Highlights**: **TODO**

---

## Detailed Feature Lists

### v1 Features
- **User Roles**: Admin, Recruiter, Applicant — **TODO** detail permissions
- **Job Postings**: Create/update/list jobs — **TODO** fields
- **Applications**: Submit application, resume upload — **TODO** accepted formats, max size
- **Applicant Dashboard**: View status, edit profile — **TODO**
- **Recruiter Dashboard**: View applicants, shortlist — **TODO**
- **Search & Filters**: Basic filtering by role/location — **TODO**
- **Email Notifications**: Confirmation/Status updates — **TODO** SMTP config
- **Data Export**: CSV/Excel for applications — **TODO**

### v2 Features
- **Advanced RBAC**: Granular privileges — **TODO**
- **Bulk Actions**: Batch shortlist/reject — **TODO**
- **Interview Scheduling**: Calendar invites — **TODO**
- **Reports**: Application funnel, conversion metrics — **TODO**
- **Attachments**: Multiple docs per applicant — **TODO**
- **Improved Search**: Multi‑facet filters and keywords — **TODO**
- **Data Retention**: Archival policy — **TODO**
- **API**: Read/Write endpoints for integration — **TODO**

### v3 Features
- **Ops Hardening**: Health checks, structured logs — **TODO**
- **Scalability**: Worker tuning, caching — **TODO**
- **Security**: TLS hardening, headers, CSRF/XSS — **TODO**
- **Audit Trails**: Admin actions & data changes — **TODO**
- **Compliance**: Backups, encryption at rest — **TODO**
- **Observability**: Metrics & alerts — **TODO**
- **CI/CD**: Automated tests, build pipeline — **TODO**

---

## Files & Folder Structure
> **Tip**: For each version, list the full tree including apps/modules, templates, static assets, migrations, configs, and tests. If Git tags exist (`v1`, `v2`, `v3`), you can generate these with `git checkout tags/<version>` and `tree -a -I '.venv|__pycache__|.git'`.

### v1 Structure
```text
SERC-Recruitment-Portal_python/            # root (v1)
├─ README.md                               # this file
├─ INSTALLATION.md                         # deployment guide
├─ requirements.txt                        # Python deps (v1)
├─ manage.py / app.py                      # Django/Flask entry (TODO)
├─ project/ or src/                        # main package (TODO)
│  ├─ settings/                            # env-specific settings (TODO)
│  ├─ wsgi.py / asgi.py                    # server entrypoint (TODO)
│  ├─ urls.py                              # routes (Django) (TODO)
│  └─ __init__.py
├─ apps/                                   # domain apps (TODO)
│  ├─ recruitment/                         # jobs/apps models, views, forms
│  ├─ accounts/                            # auth, profiles
│  └─ notifications/                       # email tasks
├─ templates/                              # HTML templates (TODO)
├─ static/                                 # CSS/JS/images (TODO)
├─ migrations/                             # DB migrations per app (TODO)
├─ scripts/                                # maintenance scripts (TODO)
└─ tests/                                  # unit/integration tests (TODO)
```

### v2 Structure
```text
SERC-Recruitment-Portal_python/            # root (v2)
├─ README.md
├─ INSTALLATION.md
├─ requirements.txt / pyproject.toml       # deps (updated v2)
├─ manage.py / app.py
├─ project/ or src/
│  ├─ settings/
│  ├─ wsgi.py / asgi.py
│  ├─ urls.py
│  └─ __init__.py
├─ apps/
│  ├─ recruitment/
│  ├─ accounts/
│  ├─ scheduling/                          # interviews (NEW in v2)
│  ├─ reports/                             # reporting (NEW in v2)
│  └─ api/                                 # REST API (NEW in v2)
├─ templates/
├─ static/
├─ migrations/
├─ scripts/
└─ tests/
```

### v3 Structure
```text
SERC-Recruitment-Portal_python/            # root (v3)
├─ README.md
├─ INSTALLATION.md
├─ requirements.txt / pyproject.toml
├─ manage.py / app.py
├─ project/ or src/
│  ├─ settings/
│  ├─ wsgi.py / asgi.py
│  ├─ urls.py
│  └─ __init__.py
├─ apps/
│  ├─ recruitment/
│  ├─ accounts/
│  ├─ scheduling/
│  ├─ reports/
│  ├─ api/
│  ├─ audit/                               # audit logging (NEW in v3)
│  └─ ops/                                 # health checks, metrics (NEW in v3)
├─ templates/
├─ static/
├─ migrations/
├─ scripts/
├─ .github/workflows/                      # CI/CD (NEW in v3)
├─ docker/                                 # optional containerization (if used)
└─ tests/
```

---

## Configuration & Environment
- **Env file**: `/etc/sercapp.env` (production)
- **App config**: `project/settings/` (Django) or `config.py` (Flask)
- **Secrets**: Use environment variables; avoid committing secrets.
- **TLS**: Existing certificate & key (Nginx):
  - `/etc/ssl/eos/eos.serc.res.in.crt`
  - `/etc/ssl/eos/eos.serc.res.in.key`

---

## Database & Migrations
- **Engine**: **TODO** (PostgreSQL/MySQL/SQLite)
- **Migrations**: `python manage.py makemigrations && migrate` (Django) or Alembic (Flask/SQLAlchemy) — **TODO**
- **Seed Data**: `scripts/seed.py` — **TODO**

---

## API Endpoints
Document the key endpoints per version:
- **v1**: Auth, Jobs (list/create), Applications (submit) — **TODO**
- **v2**: Reports, Scheduling, API tokens/JWT — **TODO**
- **v3**: Audit endpoints, Ops health (`/healthz`), Metrics — **TODO**

---

## Build & Release
- **Packaging**: `requirements.txt` / `pyproject.toml`
- **Build**: Virtualenv, `pip install -r requirements.txt`
- **Release**: Git tags `v1`, `v2`, `v3` — **TODO provide exact tags**
- **Artifacts**: Docker images / wheels — **TODO**

---

## Operations (Runbook)
- **Start/Stop**: `systemctl [start|stop|restart|status] sercapp`
- **Logs**: `/var/log/sercapp/*.log`, `journalctl -u sercapp -f`
- **Nginx**: `nginx -t && systemctl reload nginx`
- **Static Assets**: `manage.py collectstatic` (Django)
- **Backup**: DB dumps, file storage — **TODO schedule**

---

## Security & Compliance
- **TLS**: Nginx with existing cert/key
- **Headers**: HSTS, X-Content-Type-Options, X-Frame-Options — **TODO**
- **RBAC**: Role definitions & least privilege — **TODO**
- **PII**: Encryption at rest; retention policy — **TODO**
- **Audit**: Admin actions, data changes — **TODO**

---

## Testing & Quality
- **Unit/Integration Tests**: `pytest`/`unittest` — **TODO coverage**
- **Linting**: `flake8`/`black` — **TODO rules**
- **CI/CD**: GitHub Actions workflow — **TODO pipeline steps**

---

## Contributing
1. Fork & branch naming conventions — **TODO**
2. Code style — **TODO**
3. Test requirements — **TODO**
4. Commit message format — **TODO**
5. PR review checklist — **TODO**

---

## Changelog
- **v1** — Initial release: **TODO summary**
- **v2** — Enhancements: **TODO summary**
- **v3** — Production readiness: **TODO summary**

---

## How to Populate This README Automatically (Optional)
If your repository has Git tags for `v1`, `v2`, `v3`, you can auto-generate structures:
```bash
# Example (run from repo root)
for tag in v1 v2 v3; do
  git checkout tags/$tag
  echo "\n## ${tag^^} Structure" >> README.md
  tree -a -I '.venv|__pycache__|.git' >> README.md
done
```

Or use a Python script to list files and write to README with path filtering.

---

**Maintainers**: Information & Communication Technology Division (ICTD), CSIR‑SERC.

**Contact**: ictd@serc.res.in (or official channel)
