from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Модель категории
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

# Промежуточная таблица для связи многие-ко-многим между работами и категориями
work_category = db.Table('work_category',
    db.Column('work_id', db.Integer, db.ForeignKey('work.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(80))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Work(db.Model):
    __tablename__ = 'work'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories = db.relationship('Category', secondary=work_category,
                               backref='works', lazy='dynamic')

    def can_edit(self, user):
        return user.id == self.user_id or user.id == 1

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    chief = db.Column(db.Integer, db.ForeignKey('user.id'))
    members = db.Column(db.String, nullable=True)
    chief_user = db.relationship('User', foreign_keys=[chief])