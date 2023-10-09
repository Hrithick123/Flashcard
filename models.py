from datetime import datetime
from sqlalchemy.sql import func
from flask_login import UserMixin
from main import app, login_manager
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
db.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False, unique=True)
    uids = db.relationship('Deck', backref='id', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password_correction(self, attempted_password):
        if self.password == attempted_password:
            return True

    def __repr__(self):
        return f'{self.name}'


class Deck(db.Model):
    __tablename__ = 'deck'
    deck_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    deck_rate = db.Column(db.String(), nullable=False, default="Medium")

    def __repr__(self):
        return f'{self.name}'


class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer(), primary_key=True)
    front = db.Column(db.String(), nullable=False, unique=True)
    deck_id = db.Column(db.Integer(), db.ForeignKey("deck.deck_id"))
    card_rate = db.Column(db.String(), nullable=False, default="Medium")
    card_date = db.Column(db.Timestamp(), onupdate=func.now(), default=datetime(2021, 11, 28, 00, 00, 00))
    back = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'{self.name}'
