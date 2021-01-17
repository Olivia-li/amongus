import './App.css';
import React, { Component } from 'react';
import fire from './config';

class App extends Component {
  state = { "blue": {x:0, y:0}, "red": {x:0, y:0}, "yellow": {x:0, y:0}, "lime": {x:0, y:0} }

  colorDict = (red, green, blue) => {
    if (red > 130 && green < 60 && blue < 60) {
      return "red"
    } else if (green > 130 && red < 60 && blue < 60) {
      return "lime"
    } else if (blue > 130 && green < 60 && red < 60) {
      return "blue"
    } else if (red < 60 && green < 60 && blue < 60) {
      return "yellow"
    } else {
      return "yellow"
    }
  }

  componentDidMount = () => {
    let lobbyId = this.props.match.params.lobbyId
    console.log(lobbyId)

    const dotsRef = fire.database().ref(lobbyId).child('webapp');

    dotsRef.on('value', (snapshot) => {
      snapshot.forEach(data => {
        let theData = data.val()
        let color = this.colorDict(theData.color[0], theData.color[1], theData.color[2])
        console.log(color + " is at " + theData.x + "," + theData.y)
        var obj = {}
        obj[color] = color
        this.setState({[color]: {x: Math.round(theData.x/3), y: Math.round(theData.y/3)}})
      })
    })
  }

  dotPositions = (dots) => {
    const dict = {blue: "https://www.mikeball.com/wp-content/uploads/2016/03/blue-dot.png", red: "https://upload.wikimedia.org/wikipedia/commons/0/0e/Basic_red_dot.png", yellow: "https://img.pngio.com/filegaudit-yellowdotpng-wikimedia-commons-yellow-dot-png-460_460.png", lime: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Location_dot_lime.svg/1024px-Location_dot_lime.svg.png"};
    
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
          <img src="https://i.redd.it/ldfi6xzs56t51.png" width="1235px" height="691px" />
          {dotPos}
        </div>
    )
  }
}
 
export default App;
