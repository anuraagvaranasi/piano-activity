import os
from flask import Flask, request, render_template, send_from_directory,\
 jsonify, make_response,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from notes import Notes
import hashlib
import re

app = Flask(__name__, static_folder=None)
CLIENT_FOLDER = os.path.abspath('../client/build')

#database stuff
dbPath = os.path.abspath('piano.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbPath
#disable event system, reduces overhead 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    password = db.Column(db.String(256),unique=False,nullable=False)

    def __repr__(self):
        return self.username

#where the state of the program will be stored
#for when users log in then log out
userDictionary = {}


#----First we have the login and register pages
#----Since they are the first thing the user sees
#login to piano app
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET': #GET = display login page
        #if user is already logged in, send directly to app
        if 'username' in request.cookies:
            add_object(request.cookies['username'])
            return send_from_directory(CLIENT_FOLDER, 'index.html')
        #go to login page if not
        else:
            return render_template('welcome.html')

    else: #POST, read login information
        user = request.form['username']
        pwd = request.form['password']

        if user_exists(user) and hash(pwd) == get_pass(user):
            resp = make_response(send_from_directory(CLIENT_FOLDER, 'index.html'))
            resp.set_cookie('username',user)
            #create a new class only if it doesnt exist already
            add_object(user)
            return resp
        else:
            #login failed, return login page but with an error for user
            return render_template('welcome.html',incorrect=True)

#register a new user
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else: #read register information and store in database
        if register_user(request.form['username'],request.form['password']):
            #succesfully registered, redirect to login page
            return redirect(url_for('login'))
        else:
            #redirect to same page but with an error for user
            return render_template('register.html',incorrect=True)

#add object to userDict if not already there
def add_object(user):
    if user not in userDictionary:
                userDictionary[user] = Notes()


#----Database and related functions under here, can change backend as  
#----long as it does the same thing and returns the same results

#get sha256 hash of a string to store/compare password
#since we should never store password in plaintext
def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

#check if a user exists in database
def user_exists(user):
    if User.query.filter_by(username=user).first() is None:
        return False
    else:
        return True

#get password from database (which is sha256(pass))
def get_pass(user):
    return db.session.query(User.password).filter(User.username == user).scalar()

#register user in database, or return false if username already exists
def register_user(user,pwd):
    if user_exists(user) == False:
        new_user = User(username=user,password=hash(pwd))
        db.session.add(new_user)
        db.session.commit()
        return True
    else:
        return False

#----Actual routes related to react app here

#allows user to send in own sequence of notes to play
@app.route('/newSeq',methods=['POST'])
def newSeq():
    seq = request.get_json()
    #if sequence is correct format, change state of userDict class
    if match(seq):
        user = request.cookies['username']
        userDictionary[user] = Notes(str.split(seq))
        curState = userDictionary[user]
        return jsonify(curState.next_note())
    #tell app that it wasnt correct format
    else:
        return jsonify("error")

#check if a sequence is in correct format(spaces between notes doesnt matter)
def match(seq):
    #make sure it has some elements in it
    if seq.replace(" ","") == "":
        return False
        
    split_str = str.split(seq)
    regex = r"^[ABCDEFG][#b]?$"
    #check if each element in it is in the correct format
    for x in split_str:
        match = re.search(regex,x)
        if match is None:
            return False
    
    return True


@app.route('/note', methods=['GET', 'POST'])
def note():
    currentUser = userDictionary[request.cookies.get('username')]
    result = None

    #if req method = post, it wants to check if note clicked is correct
    if request.method == 'POST':
        notes = request.get_json()
        result = currentUser.record_result(notes)

    else: 
        #req method = GET therefore wants next note
        #but first check if there are still notes to get
        #return end string if complete
        if (currentUser.end()):
            results = currentUser.final_stats()
            currentUser.restart()
            return jsonify(results)

        #else send next note
        result = {'note': currentUser.next_note()}

    return jsonify(result)



@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    print(path)
    return send_from_directory(CLIENT_FOLDER, path)

#to run the actual flask app
if __name__ == "__main__":
    app.debug = True
    app.run()
