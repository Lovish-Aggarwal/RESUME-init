from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.secret_key = 'resumeBuilder'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:hr@localhost/resumeBuilder'
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



# App routes

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = userModel.query.filter_by(email=email).first()
        print(" ----------- ")
        if data:
            # print(data.name)
            if(data.password== password):
                session['loggedIn'] = True
                session['email'] = email
                session['id'] = data.id
                session['number'] = data.number
                session['name'] = data.name
                return redirect(url_for('home'))
            else:
                msg='Wrong Credentials'
                return render_template('login.html',msg=msg)
        else:
            msg='User Not Exist'
            return render_template('login.html',msg=msg)

        
    if request.method == 'GET':
        # print(session['loggedIn'])
        if session.get('loggedIn'):
            return redirect(url_for('home'))
        return render_template('login.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name=     request.form['name']
        email=    request.form['email']
        number=   request.form['number']
        password= request.form['password']
        print(name,email,number,type(number),password)
        newUser=userModel(name,email,number,password)
        try:
            db.session.add(newUser)
            db.session.commit()
            session['loggedIn'] = True
            session['email'] = email
            data = userModel.query.filter_by(email=email).first()
            session['id'] = data.id
            session['number'] = data.number
            session['name'] = data.name
            profile=profileModel(data.id,"","","","","","")
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('login'))

        except exc.IntegrityError as e:
            print(type(e),e.detail,e.statement,e.args)
            if "email" in str(e.args):
                return render_template('signup.html',msg="Email already Exists")
            if "number" in str(e.args):
                return render_template('signup.html',msg="Number already Exists")
            return str(e)
    else:
        return render_template('signup.html')

@app.route('/logout',methods=['GET','POST'])
def logOut():
    if request.method == 'POST':
        session.pop('loggedIn')
        session.pop('id')
        session.pop('email')
        session.pop('name')
        session.pop('number')
        return redirect(url_for('login'))

@app.route('/home',methods=['GET', 'POST'])
def home():
    edu=educationModel.query.filter_by(user_id=session['id']).all()
    skill=skillsModel.query.filter_by(user_id=session['id']).all()
    exp=experienceModel.query.filter_by(user_id=session['id']).all()
    profile=profileModel.query.filter_by(user_id=session['id']).first()
    print(profile)
    return render_template('home.html',edu=len(edu),skill=len(skill),exp=len(exp),profile=profile)

@app.route("/profileUpdate",methods=['POST'])
def profileUpdate():
    upProfile=profileModel.query.filter_by(user_id=session['id']).first()
    upProfile.location = request.form['loc']
    upProfile.currentPosition = request.form['cp']
    upProfile.profileTitle = request.form['pt']
    print(request.form['pt'],upProfile.profileTitle)
    upProfile.profileLink = request.form['pl']
    print(request.form['pl'],upProfile.profileLink)
    upProfile.languages = request.form['lang']
    upProfile.summary = request.form['summary']
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/resume')
def resume():
    edu=educationModel.query.filter_by(user_id=session['id']).all()
    skill=skillsModel.query.filter_by(user_id=session['id']).all()
    exp=experienceModel.query.filter_by(user_id=session['id']).all()
    return render_template('resume.html',edu=edu,skill=skill,exp=exp)

# Skills Route

@app.route('/skills/<pg>',methods=['GET', 'POST'])
def skills(pg):
    if request.method == 'GET':
        msg=request.args
        resp=""
        if msg.get('msg'):
            resp=msg['msg']
        data=skillsModel.query.filter_by(user_id=session['id']).paginate(page=int(pg), per_page=5)
        print(data.items)
        return render_template('skills.html',data=data,resp=resp)

@app.route('/skillsAdd',methods=['GET', 'POST'])
def skillsAdd():
    if request.method == 'POST':
            skill=request.form['skill']
            rating=request.form['rating']
            newSkill=skillsModel(session['id'],skill,rating)
            db.session.add(newSkill)
            db.session.commit()
            return redirect(url_for('skills',pg=1,msg="Skill Added "+str(skill)))



@app.route('/skillDelete/<id>',methods=['GET', 'POST'])
def skillDelete(id):
                skill=skillsModel.query.get(id)
                db.session.delete(skill)
                db.session.commit()
                return redirect(url_for('skills',pg=1,msg="Skill Deleted with id="+str(id)))

@app.route('/skillUpdate/<id>',methods=['GET', 'POST'])
def skillUpdate(id):
        upskill=skillsModel.query.get(id)
        print(upskill)
        upskill.skill= request.form['skill']        
        upskill.rating= request.form['rating']
        db.session.commit()        
        return redirect(url_for('skills',pg=1,msg="Skill Updated with id="+str(id)))

# Experience Section

@app.route('/workExperience/<pg>',methods=['GET','POST'])
def experiences(pg):
    if request.method == 'GET':
        msg=request.args
        resp=""
        if msg.get('msg'):
            resp=msg['msg']
        data=experienceModel.query.filter_by(user_id=session['id']).paginate(page=int(pg), per_page=5)
        print(data.items)
        return render_template('workExperience.html',data=data,resp=resp)

@app.route('/experienceAdd',methods=['GET', 'POST'])
def experienceAdd():
    if request.method == 'POST':
            title=request.form['title']
            organisation=request.form['organisation']
            duration=request.form['duration']
            discription=request.form['discription']
            newExperience=experienceModel(session['id'],title,organisation,duration,discription)
            db.session.add(newExperience)
            db.session.commit()
            # return str(newExperience)
            return redirect(url_for('experiences',pg=1,msg="Experience Added "+str(title)))

@app.route('/experienceDelete/<id>',methods=['GET', 'POST'])
def experienceDelete(id):
        experience=experienceModel.query.get(id)
        db.session.delete(experience)
        db.session.commit()
        return redirect(url_for('experiences',pg=1,msg="Work Experience Deleted with id="+str(id)))


@app.route('/experienceUpdate/<id>',methods=['GET', 'POST'])
def experienceUpdate(id):
        upexp=experienceModel.query.get(id)
        print(upexp)
        upexp.title=request.form['title']
        upexp.organisation=request.form['organisation']
        upexp.duration=request.form['duration']
        upexp.discription=request.form['discription']
        db.session.commit()        
        return redirect(url_for('experiences',pg=1,msg="Experience Updated with id="+str(id)))

# Education Section

@app.route('/education/<pg>',methods=['GET','POST'])
def education(pg):
    if request.method == 'GET':
        msg=request.args
        resp=""
        if msg.get('msg'):
            resp=msg['msg']
        data=educationModel.query.filter_by(user_id=session['id']).paginate(page=int(pg), per_page=5)
        print(data.items)
        return render_template('education.html',data=data,resp=resp)

@app.route('/educationAdd',methods=['GET', 'POST'])
def educationAdd():
    if request.method == 'POST':
            institute=request.form['institute']
            course=request.form['course']
            duration=request.form['duration']
            grades=request.form['grades']
            newEducation=educationModel(session['id'],institute,duration,course,grades)
            db.session.add(newEducation)
            db.session.commit()
            # return str(newExperience)
            return redirect(url_for('education',pg=1,msg="Education Added "+str(course)))

@app.route('/educationDelete/<id>',methods=['GET', 'POST'])
def educationDelete(id):
        education=educationModel.query.get(id)
        db.session.delete(education)
        db.session.commit()
        return redirect(url_for('education',pg=1,msg="Work Education Deleted with id="+str(id)))


@app.route('/educationUpdate/<id>',methods=['GET', 'POST'])
def educationUpdate(id):
        upedu=educationModel.query.get(id)
        print(upedu)
        upedu.institute=request.form['institute']
        upedu.course=request.form['course']
        upedu.duration=request.form['duration']
        upedu.grades=request.form['grades']
        db.session.commit()        
        return redirect(url_for('education',pg=1,msg="Education Updated with id="+str(id)))

if __name__ == '__main__':
   app.run(debug=True,port=5000)