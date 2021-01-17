import './App.css';
import React, { Component } from 'react';
import fire from './config';

class App extends Component {
  state = { "blue": {x:20, y:20}, "red": {x:0, y:0}, "yellow": {x:50, y:25}, "lime": {x:30, y:75} }

  componentDidMount = () => {
    this.updatePositions({"blue": {x: 200, y:0}})
    const dotsRef = fire.database().ref('None');
    dotsRef.on('value', (snapshot) => {
      snapshot.forEach(data => {
        console.log(data.val())
      })
    })
  }

  dotPositions = (dots) => {
    var dict = {blue: "https://www.mikeball.com/wp-content/uploads/2016/03/blue-dot.png", red: "https://upload.wikimedia.org/wikipedia/commons/0/0e/Basic_red_dot.png", yellow: "https://img.pngio.com/filegaudit-yellowdotpng-wikimedia-commons-yellow-dot-png-460_460.png", lime: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Location_dot_lime.svg/1024px-Location_dot_lime.svg.png"};
    
    var dotMap = []
    for (const [key, value] of Object.entries(dots)) {
      dotMap.push([key, value.x, value.y])
    }
    const paulmillsap = dotMap.map((dot) =>
      <img src={dict[dot[0]]} width="15px" height="15px" style={{position: "absolute", left: dot[1], top: dot[2]}}/>
    );
    return paulmillsap
  }

  // of form {blue: {x: 0, y:0}, red: {x:1, y:1}}
  updatePositions = (dotsToPositions) => {
    for (const [key, value] of Object.entries(dotsToPositions)) {
      var obj = {}
      obj[key] = key
      this.setState({[key]: {x: value.x, y: value.y}})
    }
  }

  render() { 
    const dotPos = this.dotPositions(this.state)
    return (
      <div>
        <img src="https://i.redd.it/ldfi6xzs56t51.png" width="80%" height="auto" />
        {dotPos}
      </div>
    )
  }
}
 
export default App;
