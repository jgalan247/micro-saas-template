"""
backend/app/routes.py
JSON API endpoints only (Blueprint: api)
"""
from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import inspect

from . import db
from .models import Product, Location, Order, User

api = Blueprint('api', __name__)

# ───────────────────────────── Products ────────────────────────────
@api.route('/products')
def get_products():
    location_id = request.args.get('location_id')
    query = Product.query
    if location_id:
        query = query.filter_by(location_id=location_id)

    products = query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "available": p.available,
            "location_id": p.location_id
        } for p in products
    ])


@api.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name  = data.get("name")
    price = data.get("price")
    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    product = Product(
        name        = name,
        description = data.get("description", ""),
        price       = price,
        available   = data.get("available", True),
        location_id = data.get("location_id")
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created", "product_id": product.id}), 201


@api.route('/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name        = data.get("name",        product.name)
    product.description = data.get("description", product.description)
    product.price       = data.get("price",       product.price)
    product.available   = data.get("available",   product.available)
    product.location_id = data.get("location_id", product.location_id)
    db.session.commit()
    return jsonify({"message": "Product updated"})


@api.route('/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


# ───────────────────────────── Locations ───────────────────────────
@api.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([
        {
            "id": loc.id,
            "name": loc.name,
            "latitude": loc.latitude,
            "longitude": loc.longitude
        } for loc in locations
    ])


@api.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    if not all(k in data for k in ("name", "latitude", "longitude")):
        return jsonify({"error": "Missing name, latitude or longitude"}), 400

    loc = Location(name=data["name"],
                   latitude=data["latitude"],
                   longitude=data["longitude"])
    db.session.add(loc)
    db.session.commit()
    return jsonify({"message": "Location created", "location_id": loc.id}), 201


# ───────────────────────────── Orders ──────────────────────────────
@api.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id    = data.get("user_id")
    product_id = data.get("product_id")
    quantity   = data.get("quantity", 1)

    if not user_id or not product_id:
        return jsonify({"error": "Missing user_id or product_id"}), 400

    product = Product.query.get(product_id)
    if not product or not product.available:
        return jsonify({"error": "Invalid or unavailable product"}), 404

    total_price = product.price * quantity
    order = Order(user_id=user_id, product_id=product_id,
                  quantity=quantity, total_price=total_price,
                  timestamp=datetime.now())
    db.session.add(order)
    db.session.commit()

    return jsonify({
        "message": "Order created",
        "order": {
            "id": order.id,
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "total_price": total_price,
            "timestamp": order.timestamp
        }
    }), 201


# ───────────────────────────── Users / Auth ────────────────────────
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "confirmed": bool(u.confirmed)
        } for u in users
    ])


@api.route('/users/unconfirmed')
def unconfirmed_users():
    unconfirmed = User.query.filter_by(confirmed=False).all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email} for u in unconfirmed
    ])


@api.route('/users/confirm/<int:user_id>', methods=['PUT'])
def confirm_user(user_id):
    user = User.query.get_or_404(user_id)
    user.confirmed = True
    db.session.commit()
    return jsonify({"message": "User confirmed"})


@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required = ('username', 'password', 'email')
    if not all(k in data for k in required):
        return jsonify({"error": "Missing signup fields"}), 400

    user = User(username=data['username'],
                password=data['password'],   # TODO: hash
                email=data['email'],
                role='farmer',
                confirmed=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Signup received – awaiting confirmation"}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or user.password != data['password']:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"user": {
        "id":        user.id,
        "username":  user.username,
        "role":      user.role,
        "confirmed": bool(user.confirmed)
    }})


# ─────────────────────── Debug helper (optional) ───────────────────
@api.route('/debug_tables')
def debug_tables():
    inspector = inspect(db.engine)
    return jsonify(inspector.get_table_names())

