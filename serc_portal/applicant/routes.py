import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file, g
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models import ApplicantProfile, Application, Education, Employment, Document, Payment, User
from ..rules import validate_eligibility
from ..mailer import Mailer

ALLOWED_IMG = {'jpg','jpeg','png'}
ALLOWED_PDF = {'pdf'}

applicant_bp = Blueprint('applicant', __name__)

@applicant_bp.route('/')
@login_required
def apply():
    return render_template('applicant/portal.html', t=g.t)

def check_size(stream, max_bytes):
    stream.seek(0, os.SEEK_END)
    size = stream.tell()
    stream.seek(0)
    return size <= max_bytes

@applicant_bp.route('/submit', methods=['POST'])
@login_required
def submit():
    profile = ApplicantProfile.query.filter_by(user_id=current_user.id).first() or ApplicantProfile(user_id=current_user.id)
    for field in ['name','father','mother','gender','nationality','category','pwbd','exsm','addr1','addr2','city','state','pin']:
        setattr(profile, field, request.form.get(field))
    dob_str = request.form.get('dob')
    try:
        profile.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    except Exception:
        flash('Invalid Date of Birth', 'danger'); return redirect(url_for('applicant.apply'))

    upload_dir = current_app.config['UPLOAD_FOLDER']; os.makedirs(upload_dir, exist_ok=True)
    def save_file(field, allowed, max_bytes=None):
        f = request.files.get(field)
        if f and f.filename:
            ext = f.filename.rsplit('.',1)[-1].lower()
            if ext not in allowed:
                flash(f'Invalid file type for {field}', 'danger'); return None
            if max_bytes and not check_size(f.stream, max_bytes):
                flash(f'{field} exceeds allowed size', 'danger'); return None
            fname = secure_filename(f"{current_user.id}_{field}_{int(datetime.utcnow().timestamp())}.{ext}")
            path = os.path.join(upload_dir, fname)
            f.stream.seek(0); f.save(path)
            return path
        return None
    photo_path = save_file('photo', ALLOWED_IMG, current_app.config['MAX_PHOTO_SIZE'])
    sign_path = save_file('sign', ALLOWED_IMG, current_app.config['MAX_SIGN_SIZE'])
    if not photo_path or not sign_path:
        flash('Photo/Signature missing or invalid.', 'danger'); return redirect(url_for('applicant.apply'))
    profile.photo_path = photo_path; profile.sign_path = sign_path
    db.session.add(profile); db.session.commit()

    post_code = request.form.get('postcode')
    degrees = [{'level':'Bachelor','discipline':request.form.get('bdisc') or ''},{'level':'Master','discipline':request.form.get('mdisc') or ''}]
    ok, msg = validate_eligibility(post_code, profile.category, dob_str, degrees, current_app.config['CLOSING_DATE'])
    if not ok:
        flash(msg, 'danger'); return redirect(url_for('applicant.apply'))

    app = Application(user_id=current_user.id, post_code=post_code, status='Submitted')
    db.session.add(app); db.session.commit()

    edu_entries = [
        ('Bachelor', request.form.get('bdisc'), request.form.get('buni'), request.form.get('byear'), request.form.get('bmarks')),
        ('Master', request.form.get('mdisc'), request.form.get('muni'), request.form.get('myear'), request.form.get('mmarks')),
    ]
    for level, disc, inst, year, marks in edu_entries:
        if disc and inst:
            e = Education(application_id=app.id, degree_level=level, discipline=disc, institute=inst,
                          year=int(year) if year else None, marks=marks)
            db.session.add(e)
    phd_area = request.form.get('phd_area'); phd_status = request.form.get('phd_status'); phd_date = request.form.get('phd_date')
    if phd_area or phd_status:
        e = Education(application_id=app.id, degree_level='PhD', discipline=phd_area or '', institute='',
                      year=int(phd_date.split('-')[0]) if (phd_date and '-' in phd_date) else None, marks=phd_status or '')
        db.session.add(e)
    db.session.commit()

    pdf_fields = ['phd_synopsis','phd_proof','cat_cert','pwbd_cert','equivalence','exp_cert','other_docs','noc','fee_receipt','exempt_proof']
    for field in pdf_fields:
        files = request.files.getlist(field)
        for f in files:
            if f and f.filename:
                ext = f.filename.rsplit('.',1)[-1].lower()
                if ext != 'pdf':
                    flash(f'Invalid file type for {field}', 'danger'); continue
                if not check_size(f.stream, current_app.config['MAX_PDF_SIZE']):
                    flash(f'{field} PDF too large', 'danger'); continue
                fname = secure_filename(f"{current_user.id}_{field}_{int(datetime.utcnow().timestamp())}.pdf")
                path = os.path.join(upload_dir, fname)
                f.stream.seek(0); f.save(path)
                doc = Document(application_id=app.id, doc_type=field, storage_path=path)
                db.session.add(doc)
    db.session.commit()

    fee_applicable = request.form.get('fee_applicable') == 'Yes'
    pay = Payment(application_id=app.id, applicable=fee_applicable, utr=request.form.get('utr'),
                  utr_date=datetime.strptime(request.form.get('utr_date'), '%Y-%m-%d').date() if request.form.get('utr_date') else None,
                  amount=500 if fee_applicable else 0)
    db.session.add(pay); db.session.commit()

    mailer = Mailer(current_app.config['SMTP_HOST'], current_app.config['SMTP_PORT'], current_app.config['SMTP_USER'], current_app.config['SMTP_PASS'], current_app.config['FROM_EMAIL'])
    try:
        mailer.send(current_user.email, 'CSIR-SERC — Application Submitted', f'Thank you. Your application #{app.id} for {post_code} has been submitted.')
    except Exception: pass
    try:
        admin_email = os.getenv('ADMIN_EMAIL','admin@serc.res.in')
        mailer.send(admin_email, 'New Application Submitted', f'Application #{app.id} submitted by {current_user.email} for {post_code}.')
    except Exception: pass

    flash('Application submitted successfully.', 'success')
    return redirect(url_for('applicant.view_application', app_id=app.id))

@applicant_bp.route('/application/<int:app_id>')
@login_required
def view_application(app_id):
    app = Application.query.get_or_404(app_id)
    if app.user_id != current_user.id and current_user.role not in ['admin','reviewer']:
        flash('Unauthorized', 'danger'); return redirect(url_for('applicant.apply'))
    profile = ApplicantProfile.query.filter_by(user_id=app.user_id).first()
    edus = Education.query.filter_by(application_id=app.id).all()
    emps = Employment.query.filter_by(application_id=app.id).all()
    docs = Document.query.filter_by(application_id=app.id).all()
    pay = Payment.query.filter_by(application_id=app.id).first()
    return render_template('applicant/view_application.html', app=app, profile=profile, edus=edus, emps=emps, docs=docs, pay=pay, t=g.t)

@applicant_bp.route('/application/<int:app_id>/pdf')
@login_required
def application_pdf(app_id):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from io import BytesIO
    app = Application.query.get_or_404(app_id)
    profile = ApplicantProfile.query.filter_by(user_id=app.user_id).first()
    edus = Education.query.filter_by(application_id=app.id).all()
    pay = Payment.query.filter_by(application_id=app.id).first()
    buffer = BytesIO(); c = canvas.Canvas(buffer, pagesize=A4)
    w,h = A4; y = h-50
    c.setFont('Helvetica-Bold', 14); c.drawString(50,y, f"CSIR-SERC Scientist Application — {app.post_code}"); y-=30
    # Photo on right
    if profile and profile.photo_path and os.path.exists(profile.photo_path):
        try:
            img = ImageReader(profile.photo_path)
            c.drawImage(img, w-150, h-150, width=96, height=96, preserveAspectRatio=True, mask='auto')
        except Exception: pass
    c.setFont('Helvetica', 10); c.drawString(50,y, f"Applicant: {profile.name if profile else ''} | Email: {app.user_id}"); y-=20
    c.drawString(50,y, f"Status: {app.status} | Submitted: {app.submitted_at.strftime('%Y-%m-%d %H:%M')}"); y-=30
    c.setFont('Helvetica-Bold', 12); c.drawString(50,y, 'Education:'); y-=20; c.setFont('Helvetica',10)
    for e in edus:
        c.drawString(50,y, f"{e.degree_level} — {e.discipline} — {e.institute} — {e.year} — {e.marks}"); y-=16
        if y<100: c.showPage(); y=h-50; c.setFont('Helvetica',10)
    y-=10; c.setFont('Helvetica-Bold',12); c.drawString(50,y,'Payment:'); y-=20; c.setFont('Helvetica',10)
    if pay: c.drawString(50,y, f"Applicable: {pay.applicable} | UTR: {pay.utr} | Amount: {pay.amount} | Verified: {pay.verified}")
    else: c.drawString(50,y, 'No payment record')
    c.showPage(); c.save(); buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f'application_{app.id}.pdf')
