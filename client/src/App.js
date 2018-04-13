import React, { Component } from 'react';
import Piano from './Piano.js';
import Results from './Results.js';

import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentNote: null,
      feedback: "",
      correct: null,
      total: null
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
          if(data.note == "Done!"){
            this.setState({correct: data.correct});
            this.setState({total: data.total});
          }
          this.setState({currentNote: data.note});  
        });
      }
      else{
        this.setState({feedback: "Try Again ):"});
      }
    });
  }

  sendOwnSequence(event){
    var seq = prompt("Enter Your own sequence, seperated by spaces");
    this.props.sendSeq(seq).then((data) => {
      if(data != "error"){
        this.setState({currentNote: data});
        this.setState({feedback: ""});
      }
      else{
        alert("Sequence wasn't in correct format");
      }
    });
  }

  getNote() {
    return this.state.currentNote.replace('#', '♯').replace('b', '♭');
  }

  reset(event){
    this.setState({feedback: ""});
    window.location.reload();
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
        {
          this.state.currentNote != "Done!" ? 
            <div>
              <Piano
                numOctaves={3}
                onPress={this.onPress}
              />
              <h1>{this.state.feedback}</h1>
            </div>
          :
            <div>
              <Results
                correct={this.state.correct}
                total={this.state.total}
              />
              <button type="button" className = "button" onClick={this.reset.bind(this)}>Reset</button>
              
            </div>
        }
        <br/><button type="button" className = "button" onClick={this.sendOwnSequence.bind(this)}>Play Own Notes</button>
        </div>
    );
  }
}

export default App;
