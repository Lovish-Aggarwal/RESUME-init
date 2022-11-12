from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'resumeBuilder'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:hr@localhost/resumeBuilder'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://ugkdax2p8yl3qcva:ZnIBCamnvqvbTiKkfg7M@b7ar3u2nbjahvczxcllc-mysql.services.clever-cloud.com:3306/b7ar3u2nbjahvczxcllc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_table():
    db.create_all()
 
# Data Models

class userModel(db.Model):
    __tablename__ = "user_credentials"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(35),unique=True)
    number = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(80))

    def __init__(self,name,email,number,password) -> None:
        self.name=name
        self.email=email
        self.number=number
        self.password=password

    def __repr__(self):
        return f"{self.name}:{self.email}:{self.number}:{self.password}"

class profileModel(db.Model):
    __tablename__="profile"
    user_id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(40))
    currentPosition = db.Column(db.String(40))
    profileTitle = db.Column(db.String(40))
    profileLink = db.Column(db.String(200))
    languages = db.Column(db.String(80))
    summary = db.Column(db.String(400))
    

    def __init__(self,id,loc,currPos,pl,pt,lan,sum) -> None:
        self.user_id=id
        self.location = loc
        self.currentPosition = currPos
        self.profileTitle = pl
        self.profileLink = pt
        self.languages = lan
        self.summary = sum

    def __repr__(self) -> str:
        return self.summary

class skillsModel(db.Model):
    __tablename__="skills"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    skill = db.Column(db.String(40))
    rating = db.Column(db.Integer)

    def __init__(self,id,skill,rating) -> None:
        self.user_id=id
        self.skill=skill
        self.rating=rating
    
    def __repr__(self) -> str:
        return self.skill

class experienceModel(db.Model):
    __tablename__="experiencess"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(80))
    organisation = db.Column(db.String(80))
    duration = db.Column(db.String(80))
    discription = db.Column(db.String(500))

    def __init__(self,id,title,organisation,duration,discription) -> None:
        self.user_id=id
        self.discription=discription
        self.title=title
        self.organisation=organisation
        self.duration=duration
    
    def __repr__(self) -> str:
        return self.title


class educationModel(db.Model):
    __tablename__="educations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    insitute = db.Column(db.String(80))
    course = db.Column(db.String(80))
    duration = db.Column(db.String(80))
    grades= db.Column(db.String(20))

    def __init__(self,id,insitute,duration,course,grades) -> None:
        self.user_id=id
        self.grades=grades
        self.insitute=insitute
        self.course=course
        self.duration=duration
    
    def __repr__(self) -> str:
        return self.course
