import React from 'react';
import './Piano.css';

const Key = (props) => 
  <div
    className={`Key-container ${props.color}`}
    onClick={props.onPress.bind(null, props.keyNames)}
  ></div>

const Octave = (props) =>
  <div className="Octave-container">
    <Key {...props} color='white' keyNames={['C','B#']} />
    <Key {...props} color='black' keyNames={['C#', 'Db']} />
    <Key {...props} color='white' keyNames={['D']} />
    <Key {...props} color='black' keyNames={['D#', 'Eb']} />
    <Key {...props} color='white' keyNames={['E','Fb']} />
    <Key {...props} color='white' keyNames={['F','E#']} />
    <Key {...props} color='black' keyNames={['F#', 'Gb']} />
    <Key {...props} color='white' keyNames={['G']} />
    <Key {...props} color='black' keyNames={['G#', 'Ab']} />
    <Key {...props} color='white' keyNames={['A']} />
    <Key {...props} color='black' keyNames={['A#', 'Bb']} />
    <Key {...props} color='white' keyNames={['B','Cb']} />
  </div>

const Piano = (props) => 
  <div className="Piano-container">
    {Array(props.numOctaves).fill().map((element, octave) => 
      <Octave
        key={`Octave-${octave}`}
        onPress={props.onPress.bind(null, octave)}
      />
    )}
  </div>

export default Piano;
