import React, { Component } from 'react';
import Piano from './Piano.js';

import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentNote: null,
      feedback: ""
    }

    this.props.fetchNextNote().then((data) => {
      this.setState({currentNote: data.note});
    }).catch((err) => {
      this.setState({error: 'Unable to connect to the server'});
    });
  }

  onPress = (octave, keyNames) => {
    this.props.checkAnswer(keyNames).then((data) => {
      if(data){
        this.setState({feedback: "Correct!"});
        this.props.fetchNextNote().then((data) => {
          this.setState({currentNote: data.note});  
        });
      }
      else{
        this.setState({feedback: "Try Again ):"});
      }
    });
  }

  getNote() {
    return this.state.currentNote.replace('#', '♯').replace('b', '♭');
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          {this.state.error ? `An error occurred: ${this.state.error}` : null}

          {
            this.state.currentNote ?
              <div className="App-note-name-display">{this.getNote()}</div>
            :
              <div className="App-note-loading">loading...</div>
          }
          When a note appears above, play the corresponding note on the piano keyboard.
        </header>
        <Piano
          numOctaves={3}
          onPress={this.onPress}
        />
        <h1>{this.state.feedback}</h1>
      </div>
    );
  }
}

export default App;
