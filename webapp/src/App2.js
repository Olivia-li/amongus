import './App.css';
import React, { useEffect, useState } from 'react';
import fire from './config';
import styled from 'styled-components'
import { useParams } from "react-router-dom";


export const App = () => {
  const { lobbyId } = useParams();
  const dbRef = fire.database().ref(lobbyId).child('webapp');
  const [count, setCount] = useState(0)
  const [users, setUsers] = useState([])

  useEffect(() => {
    const interval = setInterval(() => {
      getColors()
    }, 1000);
    return () => clearInterval(interval);
  }, []);



  const getColors = () => {
    setUsers([])
    setCount(0)
    dbRef.on('value', (snapshot) => {
      snapshot.forEach(data => {
        let theData = data.val()
        let user_id = data.key
        let color = `rgb(${theData.color[0]}, ${theData.color[1]}. ${theData.color[2]})`
        console.log(color + " is at " + theData.x + "," + theData.y)
        setCount(count + 1)
        setUsers(oldArray => [...oldArray, { [user_id]: { "color": color, "x": theData.x, "y": theData.y } }])
      })
    })
  }
  const divStyle = {
    color: 'blue',
    height: "100vh"
  };

  
  return (
    <>
      {Array(count).fill(<div style={divStyle}/>)}
      <img src="https://i.redd.it/ldfi6xzs56t51.png" width="1235px" height="691px" />
    </>

  )

}

export default App;