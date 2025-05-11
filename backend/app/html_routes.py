"""
backend/app/html_routes.py
Server‑rendered Bootstrap pages (Blueprint: html)
"""
from flask import Blueprint, render_template

html = Blueprint('html', __name__)

@html.route('/')
def root():
    return render_template('base.html')

@html.route('/admin-page')
def admin_page():
    return render_template('admin_page.html')

