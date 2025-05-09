from flask import Blueprint, jsonify
from .models import Product, Location
from . import db

from sqlalchemy import inspect
api = Blueprint('api', __name__)

@api.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "available": p.available,
            "location_id": p.location_id
        }
        for p in products
    ])

@api.route('/locations')
def get_locations():
    locations = Location.query.all()
    return jsonify([
        {
            "id": l.id,
            "name": l.name,
            "latitude": l.latitude,
            "longitude": l.longitude
        }
        for l in locations
    ])

@api.route('/debug_tables')
def debug_tables():
    inspector = inspect(db.engine)
    return jsonify(inspector.get_table_names())
