import os
from datetime import datetime
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    mobile = db.Column(db.String(15))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), default='applicant')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ApplicantProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200))
    father = db.Column(db.String(200))
    mother = db.Column(db.String(200))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    nationality = db.Column(db.String(100))
    category = db.Column(db.String(20))
    pwbd = db.Column(db.String(20))
    exsm = db.Column(db.String(10))
    addr1 = db.Column(db.String(250))
    addr2 = db.Column(db.String(250))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    pin = db.Column(db.String(6))
    photo_path = db.Column(db.String(300))
    sign_path = db.Column(db.String(300))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_code = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(32), default='Submitted')
    shortlist_tag = db.Column(db.String(64))
    reviewer_notes = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    degree_level = db.Column(db.String(32))
    discipline = db.Column(db.String(200))
    institute = db.Column(db.String(200))
    year = db.Column(db.Integer)
    marks = db.Column(db.String(32))

class Employment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    org = db.Column(db.String(200))
    designation = db.Column(db.String(200))
    dt_from = db.Column(db.Date)
    dt_to = db.Column(db.Date)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    doc_type = db.Column(db.String(50))
    storage_path = db.Column(db.String(400))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    applicable = db.Column(db.Boolean, default=True)
    utr = db.Column(db.String(64))
    utr_date = db.Column(db.Date)
    amount = db.Column(db.Integer)
    receipt_path = db.Column(db.String(300))
    verified = db.Column(db.Boolean, default=False)
    verified_at = db.Column(db.DateTime)
    verified_by = db.Column(db.String(255))

class BulkEmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subject = db.Column(db.String(300))
    body_preview = db.Column(db.Text)
    filter_status = db.Column(db.String(32))
    filter_post_code = db.Column(db.String(16))
    count_sent = db.Column(db.Integer)

# Seeder
from .config import Config

def seed_admin_if_needed():
    email = os.getenv('ADMIN_EMAIL','admin@serc.res.in')
    pwd = os.getenv('ADMIN_PASSWORD','Admin@123')
    admin = User.query.filter_by(email=email).first()
    if not admin:
        admin = User(email=email, mobile='9999999999', role='admin')
        admin.set_password(pwd)
        db.session.add(admin)
        db.session.commit()
