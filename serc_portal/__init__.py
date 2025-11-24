import json, os
from flask import Flask, request, g
from .extensions import db, login_manager
from .config import Config
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def load_locale(app, lang_code='en'):
    path = os.path.join(app.root_path, 'i18n', f'{lang_code}.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        with open(os.path.join(app.root_path,'i18n','en.json'),'r',encoding='utf-8') as f:
            return json.load(f)

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    @app.before_request
    def inject_locale():
        lang = request.cookies.get('lang') or request.args.get('lang') or 'en'
        g.t = load_locale(app, lang)

    @app.after_request
    def add_security_headers(resp):
        csp = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' https://cdn.jsdelivr.net; img-src 'self' data:; font-src 'self' data:; connect-src 'self';"
        resp.headers['Content-Security-Policy'] = csp
        resp.headers['X-Content-Type-Options'] = 'nosniff'
        resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        resp.headers['X-Frame-Options'] = 'DENY'
        resp.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
        return resp

    from .auth.routes import auth_bp
    from .applicant.routes import applicant_bp
    from .admin.routes import admin_bp
    from .payment.routes import payment_bp
    from .analytics.routes import analytics_bp
    from .reports.routes import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(applicant_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(reports_bp)

    with app.app_context():
        from .models import seed_admin_if_needed
        db.create_all()
        seed_admin_if_needed()
    return app
