from models import *
from sqlalchemy import exc

# App routes

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    if session.get('loggedIn'):
            return redirect(url_for('home'))

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
        msg=request.args
        resp=""
        if msg.get('msg'):
            resp=msg['msg']
        msg=resp
        return render_template('login.html',msg=msg)

@app.route('/register',methods=['GET', 'POST'])
def register():
    if session.get('loggedIn'):
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name=     request.form['name'].strip()
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
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    if request.method == 'POST':
        session.pop('loggedIn')
        session.pop('id')
        session.pop('email')
        session.pop('name')
        session.pop('number')
        return redirect(url_for('login'))

@app.route('/home',methods=['GET', 'POST'])
def home():
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))
    edu=educationModel.query.filter_by(user_id=session['id']).all()
    skill=skillsModel.query.filter_by(user_id=session['id']).all()
    exp=experienceModel.query.filter_by(user_id=session['id']).all()
    profile=profileModel.query.filter_by(user_id=session['id']).first()
    print(profile)
    return render_template('home.html',edu=len(edu),skill=len(skill),exp=len(exp),profile=profile)

@app.route("/profileUpdate",methods=['GET', 'POST'])
def profileUpdate():
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))
    upProfile=profileModel.query.filter_by(user_id=session['id']).first()
    upProfile.location = request.form['loc'].strip()
    upProfile.currentPosition = request.form['cp'].strip()
    upProfile.profileTitle = request.form['pt'].strip()
    print(request.form['pt'],upProfile.profileTitle)
    upProfile.profileLink = request.form['pl'].strip()
    print(request.form['pl'],upProfile.profileLink)
    upProfile.languages = request.form['lang'].strip()
    upProfile.summary = request.form['summary'].strip()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/resume',methods=['GET', 'POST'])
def resume():
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    edu=educationModel.query.filter_by(user_id=session['id']).all()
    skill=skillsModel.query.filter_by(user_id=session['id']).all()
    exp=experienceModel.query.filter_by(user_id=session['id']).all()
    profile=profileModel.query.filter_by(user_id=session['id']).first()
    return render_template('resume.html',edu=edu,skill=skill,exp=exp,profile=profile)

# Public View Link
@app.route('/resumeView/<id>',methods=['GET', 'POST'])
def resumeView(id):
    data = userModel.query.filter_by(id=id).first()
    edu=educationModel.query.filter_by(user_id=id).all()
    skill=skillsModel.query.filter_by(user_id=id).all()
    exp=experienceModel.query.filter_by(user_id=id).all()
    profile=profileModel.query.filter_by(user_id=id).first()
    return render_template('viewresume.html',data=data,edu=edu,skill=skill,exp=exp,profile=profile)

# Skills Route

@app.route('/skills/<pg>',methods=['GET', 'POST'])
def skills(pg):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

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
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    if request.method == 'POST':
        skill=request.form['skill'].strip()
        rating=request.form['rating']
        newSkill=skillsModel(session['id'],skill,rating)
        db.session.add(newSkill)
        db.session.commit()
        return redirect(url_for('skills',pg=1,msg="Skill Added "+str(skill)))



@app.route('/skillDelete/<id>',methods=['GET', 'POST'])
def skillDelete(id):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    skill=skillsModel.query.get(id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for('skills',pg=1,msg="Skill Deleted with id="+str(id)))

@app.route('/skillUpdate/<id>',methods=['GET', 'POST'])
def skillUpdate(id):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    upskill=skillsModel.query.get(id)
    print(upskill)
    upskill.skill= request.form['skill'].strip()       
    upskill.rating= request.form['rating']
    db.session.commit()        
    return redirect(url_for('skills',pg=1,msg="Skill Updated with id="+str(id)))

# Experience Section

@app.route('/workExperience/<pg>',methods=['GET','POST'])
def experiences(pg):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

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
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    if request.method == 'POST':
            title=request.form['title'].strip()
            organisation=request.form['organisation'].strip()
            duration=request.form['duration'].strip()
            discription=request.form['discription'].strip()
            newExperience=experienceModel(session['id'],title,organisation,duration,discription)
            db.session.add(newExperience)
            db.session.commit()
            # return str(newExperience)
            return redirect(url_for('experiences',pg=1,msg="Experience Added "+str(title)))

@app.route('/experienceDelete/<id>',methods=['GET', 'POST'])
def experienceDelete(id):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))
    experience=experienceModel.query.get(id)
    db.session.delete(experience)
    db.session.commit()
    return redirect(url_for('experiences',pg=1,msg="Work Experience Deleted with id="+str(id)))


@app.route('/experienceUpdate/<id>',methods=['GET', 'POST'])
def experienceUpdate(id):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    upexp=experienceModel.query.get(id)
    print(upexp)
    upexp.title=request.form['title'].strip()
    upexp.organisation=request.form['organisation'].strip()
    upexp.duration=request.form['duration'].strip()
    upexp.discription=request.form['discription'].strip()
    db.session.commit()        
    return redirect(url_for('experiences',pg=1,msg="Experience Updated with id="+str(id)))

# Education Section

@app.route('/education/<pg>',methods=['GET','POST'])
def education(pg):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

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
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    if request.method == 'POST':
            institute=request.form['institute'].strip()
            course=request.form['course'].strip()
            duration=request.form['duration'].strip()
            grades=request.form['grades'].strip()
            newEducation=educationModel(session['id'],institute,duration,course,grades)
            db.session.add(newEducation)
            db.session.commit()
            # return str(newExperience)
            return redirect(url_for('education',pg=1,msg="Education Added "+str(course)))

@app.route('/educationDelete/<id>',methods=['GET', 'POST'])
def educationDelete(id):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    education=educationModel.query.get(id)
    db.session.delete(education)
    db.session.commit()
    return redirect(url_for('education',pg=1,msg="Work Education Deleted with id="+str(id)))


@app.route('/educationUpdate/<id>',methods=['GET', 'POST'])
def educationUpdate(id):
    if not session.get('loggedIn'):
        return redirect(url_for('login',msg="Please Login First"))

    upedu=educationModel.query.get(id)
    print(upedu)
    upedu.insitute=request.form['institute'].strip()
    upedu.course=request.form['course'].strip()
    upedu.duration=request.form['duration'].strip()
    upedu.grades=request.form['grades'].strip()
    db.session.commit()        
    return redirect(url_for('education',pg=1,msg="Education Updated with id="+str(id)))

if __name__ == '__main__':
   app.run(debug=True)