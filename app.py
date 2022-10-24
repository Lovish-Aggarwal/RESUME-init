from flask import Flask, render_template, request, session
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
        return f"{self.name}:{self.email}"

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
    if(session.get('loggedIn')==None):
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

if __name__ == '__main__':
   app.run(debug=True,port=5000)