from flask import Blueprint, jsonify
from .models import Product, Location
from . import db
from flask import request
from .models import Order, User, Product
from datetime import datetime


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

@api.route('/debug_tables')
def debug_tables():
    inspector = inspect(db.engine)
    return jsonify(inspector.get_table_names())

@api.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    # Basic input validation
    if not user_id or not product_id:
        return jsonify({"error": "Missing user_id or product_id"}), 400

    # Fetch product
    product = Product.query.get(product_id)
    if not product or not product.available:
        return jsonify({"error": "Invalid or unavailable product"}), 404

    # Calculate total price
    total_price = product.price * quantity

    # Create new order
    new_order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        total_price=total_price,
        timestamp=datetime.now()
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "message": "Order created successfully",
        "order": {
            "id": new_order.id,
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "total_price": total_price,
            "timestamp": new_order.timestamp
        }
    }), 201

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin
        }
        for u in users
    ])


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")  # In real apps, hash this!
    email = data.get("email")
    is_admin = data.get("is_admin", False)

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = User(username=username, password=password, email=email, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created", "user_id": user.id}), 201

@api.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    location_id = data.get("location_id")
    available = data.get("available", True)

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    product = Product(name=name, description=description, price=price,
                      available=available, location_id=location_id)
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product created", "product_id": product.id}), 201


@api.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.available = data.get("available", product.available)
    product.location_id = data.get("location_id", product.location_id)

    db.session.commit()
    return jsonify({"message": "Product updated"})


@api.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})

@api.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([
        {
            "id": loc.id,
            "name": loc.name,
            "latitude": loc.latitude,
            "longitude": loc.longitude
        }
        for loc in locations
    ])

@api.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    name = data.get("name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not name or latitude is None or longitude is None:
        return jsonify({"error": "Missing name, latitude, or longitude"}), 400

    location = Location(name=name, latitude=latitude, longitude=longitude)
    db.session.add(location)
    db.session.commit()

    return jsonify({
        "message": "Location created",
        "location_id": location.id
    }), 201

