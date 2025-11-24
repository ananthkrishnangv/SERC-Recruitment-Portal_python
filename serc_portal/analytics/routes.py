from flask import Blueprint, render_template, jsonify, g
from flask_login import login_required, current_user
from ..models import Application, ApplicantProfile
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, url_prefix='/admin/analytics')

@analytics_bp.before_request
def restrict_to_admin():
    if not current_user.is_authenticated:
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    if current_user.role not in ['admin','reviewer']:
        from flask import flash, redirect, url_for
        flash('Admins/Reviewers only', 'danger')
        return redirect(url_for('applicant.apply'))

@analytics_bp.route('/')
@login_required
def analytics_home():
    return render_template('analytics/analytics.html', t=g.t)

@analytics_bp.route('/data')
@login_required
def analytics_data():
    by_post = dict((pc, cnt) for pc, cnt in Application.query.with_entities(Application.post_code, func.count('*')).group_by(Application.post_code).all())
    by_status = dict((st, cnt) for st, cnt in Application.query.with_entities(Application.status, func.count('*')).group_by(Application.status).all())
    by_category = dict((cat, cnt) for cat, cnt in ApplicantProfile.query.with_entities(ApplicantProfile.category, func.count('*')).group_by(ApplicantProfile.category).all())
    return jsonify({'by_post': by_post,'by_status': by_status,'by_category': by_category})
