import React from 'react';

const Results = (props) =>
    <div className = "Results-container">
        <h1 style={{color:'#0F0'}}>{props.correct} note(s) played correctly!</h1>
        <h1>Out of {props.total} attempts</h1>
        <h1>{(props.correct/props.total * 100).toFixed(2)}% Overall!</h1>
    </div>

export default Results;