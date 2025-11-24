from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user
from ..extensions import db
from ..models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_url = request.args.get('next') or url_for('applicant.apply')
            return redirect(next_url)
        flash('Invalid credentials', 'danger')
    return render_template('login.html', t=g.t)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('auth.register'))
        user = User(email=email, mobile=mobile, role='applicant')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registration successful', 'success')
        return redirect(url_for('applicant.apply'))
    return render_template('register.html', t=g.t)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
