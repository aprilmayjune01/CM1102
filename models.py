
from datetime import datetime
from shop import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Florist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    flowers = db.relationship('Flower', backref='florist', lazy=True)

    def __repr__(self):
        return f"Florist('{self.first_name}', '{self.last_name}')"

class Flower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(300), nullable=False)
    #publication_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Numeric(10,2), nullable=False)
    image_file = db.Column(db.String(10), nullable=False, default='default.jpg')
    stock_level = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('florist.id'), nullable=False)

    def __repr__(self):
        return f"Flower('{self.title}', '{self.description}', '{self.price}', '{self.stock_level}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    flower_id = db.Column(db.Integer, db.ForeignKey('flower.id'), nullable=False)


