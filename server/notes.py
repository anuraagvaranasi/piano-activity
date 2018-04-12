default_sequence = ['C#','A','D','E','F#','G','Ab']

class Notes:
    #given sequence defaults to above if not inputted
    def __init__(self,given_sequence=default_sequence):
        self.position = 0
        self.notes = given_sequence
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