from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()
def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)  
    return db

def insertInDb(self):
    db.session.add(self)
    db.session.commit()

def update(self):
    db.session.commit(self)

def delete(self):
    db.session.delete(self)
    db.session.commit()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.String, primary_key=True)
    question = db.Column(db.String)
    answerA = db.Column(db.String(120))
    answerB = db.Column(db.String(120))
    answerC = db.Column(db.String(120))
    answerD = db.Column(db.String(120))
    answerCorrect = db.Column(db.String(120))
    picture_path = db.Column(db.String(500))
    hint = db.Column(db.String(120))
    
    
    
class user(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.String, primary_key=True)
    token = db.Column(db.String, nullable=True)
    user_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean)

class score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.Date)
    user_score= db.Column(db.Integer)
    user_id = db.Column(db.String, ForeignKey('student.id'), nullable=False)
    
    