from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bootstrap5 import Bootstrap    # ← fixed import

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder="templates",
                static_folder="static")

    # ── DB config ───────────────────────────
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../honestybox.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # ── CORS for Vue front‑end ──────────────
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ── Bootstrap 5 init ────────────────────
    Bootstrap(app)                         # ← fixed

    # ── Blueprints ─────────────────────────
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    from .html_routes import html
    app.register_blueprint(html)           # root (“/”)

    # Optional: auto‑create tables
    with app.app_context():
        db.create_all()

    return app

