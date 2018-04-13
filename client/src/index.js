import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { unregister } from './registerServiceWorker';


const SEQ_URL = 'http://localhost:5000/newSeq';
const NOTE_URL = 'http://localhost:5000/note';

const fetchNextNote = () => 
  fetch(NOTE_URL,{
    credentials: 'same-origin',
  }).then(response => response.json());

const checkAnswer = (answer) => 
  fetch(NOTE_URL, {
    credentials: 'same-origin',
    body: JSON.stringify(answer),
    cache: 'no-cache',
    headers: {
      'content-type': 'application/json'
    },
    method: 'POST'
  }).then(response => response.json());

const sendSeq = (sequence) => 
  fetch(SEQ_URL, {
    credentials: 'same-origin',
    body: JSON.stringify(sequence),
    cache: 'no-cache',
    headers: {
      'content-type': 'application/json'
    },
    method: 'POST'
  }).then(response => response.json());

ReactDOM.render(
  <App
    fetchNextNote={fetchNextNote}
    checkAnswer={checkAnswer}
    sendSeq={sendSeq}
  />,
  document.getElementById('root')
);
unregister();
