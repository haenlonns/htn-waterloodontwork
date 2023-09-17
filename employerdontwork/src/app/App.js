import logo from './logo.svg';
import './App.css';
import Card from './Card'; 
import React, {useState} from 'react';
import AnimatedText from './Title';
import Button from './Button';

function App() {
  const handleClick = () => {
    
    alert('Button clicked!');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1><AnimatedText/></h1>
        <br/>
        <br/>
      </header>

      <main className="main-content">
        <Card title="Register Your Company" 
                content={
                <div className="form-container">
                <br/>
                <label> Company: <input type="text" style={{ width: '290px', height:'20px'}}/>
                <br/>
                <br/>
                Verification Email: <input type="text" style={{ width: '234px', height:'20px'}}/>
                <br/>
                <br/>
                Website: <input type="text" style={{ width: '300px', height:'20px'}}/>
                <br/>
                <br/>
                Socials: <input type="text" style={{ width: '310px', height:'20px'}}/>
                <br/>
                <br/>
                Description: <br/><br/> <input type="text" style={{ width: '400px', height: '150px'}}/>
         </label>
         <br/>
         <br/>
         <Button label="Click Me" onClick={handleClick} />
         </div>
         } 
         />

        <Card title="Job Postings" 
        content= {
          <div className="form-container">
          <br/>
          <br/>
          <Button label="Click Me" onClick={handleClick} />
          </div>
        }/>
      </main>
      
    </div>
  );
}

export default App;
