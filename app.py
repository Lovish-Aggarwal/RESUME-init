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
                return redirect(url_for('home'))
            else:
                msg='Wrong Credentials'
                return render_template('login.html',msg=msg)
        else:
            msg='User Not Exist'
            return render_template('login.html',msg=msg)

        
    if request.method == 'GET':
        print(session['loggedIn'])
        if session['loggedIn']==True:
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
            return "Registed"
        except exc.IntegrityError as e:
            print(type(e),e.detail,e.statement,e.args)
            if "email" in str(e.args):
                return render_template('signup.html',msg="Email already Exists")
            if "number" in str(e.args):
                return render_template('signup.html',msg="Number already Exists")
            return str(e)
    else:
        return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/resume')
def resume():
    pdfkit.from_file('resume.html', 'out.pdf')
    return render_template('resume.html')

if __name__ == '__main__':
   app.run(debug=True,port=5000)