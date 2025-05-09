from . import db

class User(db.Model):
    __tablename__ = 'users'     
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)

class Location(db.Model):
    __tablename__ = 'locations' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Product(db.Model):
    __tablename__ = 'products' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

class Order(db.Model):
    __tablename__ = 'orders' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

