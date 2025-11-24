# CSIR-SERC Scientist Recruitment Portal — v3 (Bulk Email + Reports)

This version adds:
- **Bulk Email Tool** for interview scheduling (filters, placeholders, dry-run).
- **Reports & Export**: CSV and Excel (.xlsx). Excel can **embed photo thumbnails**.
- **Individual Application PDF** now includes applicant **photo**.
- Existing admin analytics charts and CSV export remain.

## Usage
- Bulk Email: `/admin/bulk-email` → filter by Status/Post Code → compose subject & body → use placeholders `{name}`, `{post_code}`, `{app_id}`, `{interview_dt}`, `{venue}` → dry run preview or send.
- Reports: `/admin/reports` → export CSV or Excel; check **Include Photo** to embed thumbnails in Excel. CSV includes photo file path.
- Individual PDF: open the application and click **Download PDF**.

## Configuration
See `.env.example` for SMTP, sizes, DB, and closing date.

## Notes
- Ensure SMTP settings are valid before sending bulk emails.
- For large exports, consider pagination or filters.
- Excel photo embedding uses **openpyxl** and **Pillow**.

## Security
CSP, HSTS (on HTTPS), XFO, XCTO, Referrer-Policy enabled; CSRF protection on forms.

## References
- Official Advertisement (**SE-2/2025**) for post codes, categories, disciplines, age & requirements.
- Steps for Online Application PDF for fee and flow (UTR capture, exemptions).
