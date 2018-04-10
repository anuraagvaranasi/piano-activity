import os
from flask import Flask, request, render_template, send_from_directory, jsonify
app = Flask(__name__, static_folder=None)

CLIENT_FOLDER = os.path.abspath('../client/build')
default_sequence = ['Bb','A','D','E','F#','G','Ab']

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
        print(self.position)
        #result_position = self.position-1
        #self.results[result_position] = (self.notes[result_position] in note_played) 

test = Notes()

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/note', methods=['GET', 'POST'])
def note():
    result = None

    if request.method == 'POST':
        notes = request.get_json()

        test.record_result(notes)

    
    result = {'note': test.next_note()}
    print(test.results)
    print(result)

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
