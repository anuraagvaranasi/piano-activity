import os
from flask import Flask, request, render_template, send_from_directory, jsonify, make_response
from uuid import uuid4
app = Flask(__name__, static_folder=None)

CLIENT_FOLDER = os.path.abspath('../client/build')
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
        self.position += 1
        return return_note

    def record_result(self,note_played):
        #position is 1 further than result table
        #as we move the position in the next_note method
        if self.notes[self.position-1] in note_played:
            self.results.append(True)
            return True
        else:
            self.results.append(False)    
            return False
    def final_stats(self):
        return {'note':'Done!','correct':len(self.notes),'total':len(self.results)}

#where the data for notes will be stored  
test = Notes()
userDictionary = {}

@app.route('/')
def welcome():
    sessionID = str
    resp = make_response(render_template('welcome.html'))
    resp.set_cookie('sessionID',sessionID)
    resp.set_cookie('username','anuraag')
    userDictionary[sessionID] = Notes()
    return resp




@app.route('/note', methods=['GET', 'POST'])
def note():

    id = request.cookies.get('sessionID')
    print(request.cookies.get('username'))
    print(id)
    print(request.cookies)
    print("VVCONFUSED???")
    currentUser = test
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
            return jsonify(currentUser.final_stats())

        #else send next note
        result = {'note': currentUser.next_note()}

    return jsonify(result)


@app.route('/piano/', methods=['GET'])
def serve_app():
    return send_from_directory(CLIENT_FOLDER, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    print(path)
    return send_from_directory(CLIENT_FOLDER, path)

if __name__ == "__main__":
    app.debug = True
    app.run()
