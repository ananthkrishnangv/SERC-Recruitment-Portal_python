# SERC Recruitment Portal — Application Features (v1 → v3)

This document catalogs **application-related features** implemented in the SERC Recruitment Portal up to **version v3**. It is organized by release version and functional area to help product, engineering, QA, and operations teams align on scope.

> **Note:** Where specifics depend on the repository’s exact implementation, please validate and adjust wording to match the codebase (models, views, APIs, templates). This file is designed to be comprehensive and future-proof.

---

## v1 — Core Portal (Initial Release)

### 1) User & Access Management
- **Roles**: Admin, Recruiter, Applicant
- **Authentication**: Login/logout, password reset (email-based)
- **Profile Management**:
  - Applicants: personal details, education, skills, resume upload
  - Recruiters: organization, department, contact info
- **Authorization (RBAC)**: Role-scoped menus and permissions

### 2) Job & Position Management
- Create, edit, publish, archive job postings
- Job attributes: title, category, project/section, grade/level, location, openings, application deadline
- Attachments: JD/PDF uploads, annexures
- Visibility controls: internal/external posting, publish/unpublish

### 3) Application Workflow
- Applicant submission: forms + file uploads (resume, certificates)
- Draft vs final submission; edit until deadline
- Auto-generated application ID and acknowledgment
- Status lifecycle: `Submitted → Under Review → Shortlisted/Rejected → Final` (basic)

### 4) Search & Filters
- Recruiter panel: filter by job, status, qualification, experience, category
- Applicant panel: search open jobs by keyword, location, department

### 5) Notifications & Communication
- Email confirmations on registration and application submission
- Deadline reminders (simple scheduled emails)

### 6) Data & Export
- Recruiter exports (CSV/Excel) for applicants of a job
- Printable application form (PDF/HTML)

### 7) Content & Pages
- Static pages: Instructions, FAQs, Privacy, Terms
- Contact/Support form

### 8) Accessibility & UX
- Mobile-friendly pages (basic responsive design)
- Form validation (client/server)

### 9) Admin Utilities
- Manage users (create/disable)
- Manage lookups (qualification, categories, reservation types)
- Basic dashboard: counts of jobs, applications

---

## v2 — Enhancements & Integrations

### 1) Advanced RBAC & Workflows
- Granular permissions for Admin sub-roles (HR, Screening, Panel Coordinator)
- Multi-stage review: **Screening → Technical evaluation → HR review → Final panel**
- Bulk actions (shortlist/reject) with reason codes

### 2) Interview & Scheduling
- Interview rounds configuration per job
- Slot management (date/time, panel, capacity)
- Invite emails to shortlisted applicants
- Attendance tracking; panel feedback capture

### 3) Documents & Attachments
- Multiple file uploads per applicant: resume, publications, experience letters, caste/disability certificates
- File-type & size validation; secure storage paths

### 4) Reports & Analytics
- Job funnel metrics: views, starts, submissions, shortlists, offers
- Applicant demographics: qualification, experience bands
- Downloadable reports (CSV/XLSX)

### 5) Search & Matching Improvements
- Full-text search across applicant profiles and resumes (metadata)
- Faceted filters (department, grade, experience, reservation category)

### 6) Communications & Templates
- Email templates per lifecycle event (customizable)
- Batch email to cohorts (shortlisted / waitlisted)

### 7) Data Policies & Retention
- Configurable retention windows (e.g., archive applications after N months)
- Soft-delete with restore for records

### 8) API (Internal Integrations)
- Read endpoints: jobs, applicants, application status
- Write endpoints: status update, interview scheduling
- Token/JWT-based access (internal systems)

### 9) Usability & Accessibility
- Improved responsive layouts and keyboard navigation
- Form progress indicators and autosave for multi-step forms

### 10) Admin & Ops
- Admin dashboard: per-job KPIs, overdue actions
- Audit summary (who changed what, when) — initial logging

---

## v3 — Production Readiness & Scale

### 1) Security & Compliance
- TLS hardening with existing certificate and key in Nginx
- Security headers: HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- CSRF protection for forms; input sanitization
- Role-based data access controls; PII masking in exports (as configured)

### 2) Audit & Traceability
- Detailed audit logging for user actions (create/update/delete)
- Status change history with actor and timestamp
- Download/view logs for admins with role-based access

### 3) Performance & Scalability
- Gunicorn worker tuning (workers, timeouts)
- Static asset offload via Nginx with cache headers
- Optional caching layer (per-page/per-query) — configuration-driven

### 4) Observability & Health
- `/healthz` endpoint (app/service health)
- Structured logs (JSON) for app events and errors
- Log rotation policies

### 5) Reliability & Operations
- Systemd service for app with automatic restart
- Graceful reloads for rolling updates
- Backup procedures: DB dumps; file storage backups (documented)

### 6) Data & Reporting Extensions
- Advanced exports with anonymization options
- Longitudinal reports (applications over time; department trends)

### 7) Internationalization & Localization (Optional)
- i18n-ready templates and messages
- Date/time localization and Indian formats

### 8) Admin & Configuration
- Feature flags (enable/disable modules per release)
- Email/SMS gateway abstraction; SMTP profiles per environment
- Retention & purge tools with dry-run mode

---

## Cross-Cutting Features (All Versions)

### Validation & Integrity
- Server-side validation for required fields and file types
- Referential integrity between jobs and applications

### Error Handling & UX
- Clear error messages and recovery paths
- Accessibility hints (labels, aria attributes)

### Documentation & Help
- User guides for applicants and recruiters
- Admin handbook for workflows and compliance

---

## Version Mapping (Quick Reference)

| Area | v1 | v2 | v3 |
|---|---|---|---|
| Roles & Auth | Core | Granular RBAC | Compliance-focused access |
| Jobs | Create/Publish | Multi-stage workflows | Advanced reporting |
| Applications | Submit/Status | Bulk actions, attachments | Audit trails |
| Interviews | — | Scheduling & invites | Panel logs & reliability |
| Search/Filters | Basic | Faceted + full-text | Performance tuned |
| Notifications | Basic email | Templates & batches | Gateway abstraction |
| API | — | Internal API | Observability endpoints |
| Security | Basic | Improved validation | TLS/headers/CSRF |
| Audit | — | Summary | Detailed logs & history |
| Ops | Basic dashboards | Admin KPIs | Health, backups, log rotation |

---

## Notes & Next Steps
- Validate feature names and lifecycle states against actual models/routes/templates.
- Align file upload limits, accepted formats, and retention policies with institutional guidelines.
- If you provide repo access (or export the directory trees), I can auto‑link each feature to the exact modules and templates.
