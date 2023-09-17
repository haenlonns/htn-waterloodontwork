import React from 'react';
import './App.css';

function Button({ label, onClick }) {
    return (
      <div className="button-container">
        <button className="custom-button" onClick={onClick}>
          {label}
        </button>
      </div>
    );
  }
  
  export default Button;