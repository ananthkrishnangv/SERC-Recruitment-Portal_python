from flask import Blueprint, render_template, request, send_file, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Application, ApplicantProfile, Payment
import io
import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage

reports_bp = Blueprint('reports', __name__, url_prefix='/admin/reports')

@reports_bp.before_request
def restrict_to_admin():
    if not current_user.is_authenticated:
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    if current_user.role not in ['admin','reviewer']:
        from flask import flash, redirect, url_for
        flash('Admins/Reviewers only', 'danger')
        return redirect(url_for('applicant.apply'))

@reports_bp.route('/')
@login_required
def reports_home():
    return render_template('reports/reports.html')

@reports_bp.route('/export')
@login_required
def export():
    fmt = request.args.get('format','csv')
    include_photo = request.args.get('include_photo','0') == '1'
    status = request.args.get('status')
    post_code = request.args.get('post_code')

    q = Application.query
    if status: q = q.filter_by(status=status)
    if post_code: q = q.filter_by(post_code=post_code)
    apps = q.order_by(Application.id).all()

    rows = []
    for a in apps:
        prof = ApplicantProfile.query.filter_by(user_id=a.user_id).first()
        pay = Payment.query.filter_by(application_id=a.id).first()
        rows.append({
            'ApplicationID': a.id,
            'Name': prof.name if prof else '',
            'Category': prof.category if prof else '',
            'PwBD': prof.pwbd if prof else '',
            'PostCode': a.post_code,
            'Status': a.status,
            'SubmittedAt': a.submitted_at,
            'PhotoFile': prof.photo_path if prof else '',
            'UTR': pay.utr if pay else '',
            'Amount': pay.amount if pay else 0,
            'PaymentVerified': pay.verified if pay else False,
        })

    if fmt == 'csv':
        df = pd.DataFrame(rows)
        buf = io.StringIO(); df.to_csv(buf, index=False)
        return send_file(io.BytesIO(buf.getvalue().encode('utf-8')), as_attachment=True, download_name='applications.csv', mimetype='text/csv')
    elif fmt == 'xlsx':
        wb = Workbook(); ws = wb.active; ws.title = 'Applications'
        headers = list(rows[0].keys()) if rows else ['ApplicationID']
        ws.append(headers)
        # write rows first
        for r in rows:
            ws.append([r.get(h,'') for h in headers])
        if include_photo:
            # Embed photos in a dedicated column named 'Photo'
            if 'Photo' not in headers:
                ws.cell(row=1, column=len(headers)+1, value='Photo')
                photo_col = len(headers)+1
            else:
                photo_col = headers.index('Photo')+1
            for idx, r in enumerate(rows, start=2):
                path = r.get('PhotoFile')
                try:
                    if path and os.path.exists(path):
                        # Load & downscale to thumbnail
                        img = PILImage.open(path)
                        img.thumbnail((96,96))
                        tmp = io.BytesIO()
                        img.save(tmp, format='PNG'); tmp.seek(0)
                        xlimg = XLImage(tmp)
                        xlimg.width = 96; xlimg.height = 96
                        ws.add_image(xlimg, f'{chr(64+photo_col)}{idx}')
                except Exception:
                    continue
        buf = io.BytesIO(); wb.save(buf); buf.seek(0)
        return send_file(buf, as_attachment=True, download_name='applications.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        flash('Unsupported format', 'danger')
        return render_template('reports/reports.html')
