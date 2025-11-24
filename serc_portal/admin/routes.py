from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Application, ApplicantProfile, Education, Employment, Document, Payment, BulkEmailLog, User
from ..mailer import Mailer
from ..config import Config
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def restrict_to_admin():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.role not in ['admin','reviewer']:
        flash('Admins/Reviewers only', 'danger')
        return redirect(url_for('applicant.apply'))

@admin_bp.route('/')
@login_required
def dashboard():
    q = Application.query
    status = request.args.get('status'); post_code = request.args.get('post_code')
    if status: q = q.filter_by(status=status)
    if post_code: q = q.filter_by(post_code=post_code)
    apps = q.order_by(Application.submitted_at.desc()).limit(500).all()
    counts = {s: Application.query.filter_by(status=s).count() for s in ['Submitted','Under Review','Shortlisted','Rejected']}
    return render_template('admin/dashboard.html', apps=apps, counts=counts, t=g.t)

@admin_bp.route('/application/<int:app_id>')
@login_required
def review_application(app_id):
    app = Application.query.get_or_404(app_id)
    profile = ApplicantProfile.query.filter_by(user_id=app.user_id).first()
    edus = Education.query.filter_by(application_id=app.id).all()
    emps = Employment.query.filter_by(application_id=app.id).all()
    docs = Document.query.filter_by(application_id=app.id).all()
    pay = Payment.query.filter_by(application_id=app.id).first()
    return render_template('admin/review.html', app=app, profile=profile, edus=edus, emps=emps, docs=docs, pay=pay, t=g.t)

@admin_bp.route('/application/<int:app_id>/status', methods=['POST'])
@login_required
def update_status(app_id):
    app = Application.query.get_or_404(app_id)
    new_status = request.form.get('status')
    tag = request.form.get('shortlist_tag')
    notes = request.form.get('reviewer_notes')
    if new_status not in ['Submitted','Under Review','Shortlisted','Rejected']:
        flash('Invalid status', 'danger'); return redirect(url_for('admin.review_application', app_id=app.id))
    app.status = new_status; app.shortlist_tag = tag; app.reviewer_notes = notes
    db.session.commit()

    mailer = Mailer(Config.SMTP_HOST, Config.SMTP_PORT, Config.SMTP_USER, Config.SMTP_PASS, Config.FROM_EMAIL)
    try:
        u = User.query.get(app.user_id)
        if u:
            mailer.send(u.email, 'CSIR-SERC — Application Status Updated', f'Your application #{app.id} status is now: {new_status}.')
    except Exception:
        pass

    flash('Status updated', 'success')
    return redirect(url_for('admin.review_application', app_id=app.id))

@admin_bp.route('/payment/verify', methods=['POST'])
@login_required
def payment_verify():
    pay_id = request.form.get('payment_id'); verified = request.form.get('verified') == 'true'
    pay = Payment.query.get_or_404(int(pay_id))
    pay.verified = verified; pay.verified_at = datetime.utcnow(); pay.verified_by = current_user.email
    db.session.commit()
    flash('Payment verification updated', 'success')
    return redirect(url_for('admin.review_application', app_id=pay.application_id))

# Bulk email tool
@admin_bp.route('/bulk-email', methods=['GET','POST'])
@login_required
def bulk_email():
    if request.method == 'POST':
        filter_status = request.form.get('filter_status')
        filter_post_code = request.form.get('filter_post_code')
        subject = request.form.get('subject')
        body = request.form.get('body')
        interview_dt = request.form.get('interview_dt') or ''
        venue = request.form.get('venue') or ''
        dry_run = request.form.get('dry_run') == 'on'

        q = Application.query
        if filter_status: q = q.filter_by(status=filter_status)
        if filter_post_code: q = q.filter_by(post_code=filter_post_code)
        apps = q.all()

        sent = 0
        mailer = Mailer(Config.SMTP_HOST, Config.SMTP_PORT, Config.SMTP_USER, Config.SMTP_PASS, Config.FROM_EMAIL)
        previews = []
        for a in apps:
            u = User.query.get(a.user_id)
            prof = ApplicantProfile.query.filter_by(user_id=a.user_id).first()
            if not u or not u.email: continue
            placeholders = {
                'name': (prof.name if prof else ''),
                'post_code': a.post_code,
                'app_id': a.id,
                'interview_dt': interview_dt,
                'venue': venue
            }
            body_filled = body.format(**placeholders)
            if dry_run:
                previews.append({'to': u.email, 'subject': subject, 'body': body_filled})
            else:
                try:
                    mailer.send(u.email, subject, body_filled)
                    sent += 1
                except Exception:
                    continue
        if dry_run:
            flash(f'Dry run generated {len(previews)} previews. No emails sent.', 'info')
            return render_template('admin/bulk_email.html', previews=previews, t=g.t)
        log = BulkEmailLog(subject=subject, body_preview=(body[:500]+'...' if len(body)>500 else body), filter_status=filter_status, filter_post_code=filter_post_code, count_sent=sent)
        db.session.add(log); db.session.commit()
        flash(f'Bulk email sent to {sent} applicants.', 'success')
        return redirect(url_for('admin.bulk_email'))
    return render_template('admin/bulk_email.html', previews=None, t=g.t)
