import os
from flask import Flask, request, render_template, send_from_directory,\
 jsonify, make_response,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import hashlib

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

default_sequence = ['C#','A','D','E','F#','G','Ab']
#default_sequence = ['C#']

class Notes:
    def __init__(self):
        self.position = 0
        self.notes = default_sequence
        self.results = []

    def end(self):
        return self.position == len(self.notes)
    
    def next_note(self):
        return_note = self.notes[self.position]
        return return_note

    def record_result(self,note_played):
        if self.notes[self.position] in note_played:
            self.results.append(True)
            #move forward when correct note is played
            self.position += 1
            return True
        else:
            self.results.append(False)    
            return False

    def final_stats(self):
        return {'note':'Done!','correct':len(self.notes),'total':len(self.results)}

    def restart(self):
        self.position = 0
        self.results.clear()

    def last_element(self):
        return self.results[-1]

#where the state of the program will be stored
#for when users log in then log out
userDictionary = {}

#login to piano app, also stores state if logged in before and wasnt completed
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET': #GET = display login page
        return render_template('welcome.html')

    else: #POST, read login information
        print(request.form)
        user = request.form['username']
        pwd = request.form['password']

        if user_exists(user) and hash(pwd) == get_pass(user):
            resp = make_response(send_from_directory(CLIENT_FOLDER, 'index.html'))
            resp.set_cookie('username',user)
            #create a new class only if it doesnt exist already
            if user not in userDictionary:
                userDictionary[user] = Notes()
            return resp

        else:
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
            return render_template('register.html',incorrect=True)

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
        print("cannot register user " + user)
        return False

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

if __name__ == "__main__":
    app.debug = True
    app.run()
