import datetime

from app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    creator = db.Column(db.String(64))
    creation_date = db.Column(db.DateTime)

    def __repr__(self):
        return self.name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    creator = db.Column(db.String(64))
    creation_date = db.Column(db.DateTime)
    owner = db.Column(db.String(64))
    owned_date = db.Column(db.DateTime)
    completer = db.Column(db.String(64))
    complete_date = db.Column(db.DateTime)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('tasks', lazy='dynamic'))

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status', backref=db.backref('tasks', lazy='dynamic'))
    
    def __repr__(self):
        return '<Task {}>'.format(self.title)
    
    def days_active(self):
        delta = datetime.date.today() - self.creation_date.date()
        return delta.days


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return '<Status {}>'.format(self.name)


# user class
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    pw_hashed = db.Column(db.String(64))
    pw_salt = db.Column(db.String(8))
    pw_hash_type = db.Column(db.String(64))
    logged_in = db.Column(db.Boolean())
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
    
    def set_password(self, password):
        hashed_password = generate_password_hash(password)
        self.pw_hash_type = hashed_password.split("$")[0]
        self.pw_salt = hashed_password.split("$")[1]
        self.pw_hashed = hashed_password.split("$")[2]
    
    def check_password(self, password):
        hashed_password = self.pw_hash_type + "$"
        hashed_password += self.pw_salt + "$"
        hashed_password += self.pw_hashed
        if check_password_hash(hashed_password, password):
            self.logged_in = True
            return True
        else:
            self.logged_in = True
            return False

    def is_anonymous(self):
        '''only allow identified users'''
        return False
    
    def is_active(self):
        '''all users are active if they exist'''
        return True
    
    def get_id(self):
        return self.username
    
    def is_authenticated(self):
        return True

    def __repr__(self):
        return self.username