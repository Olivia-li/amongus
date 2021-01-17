import React, { Component } from 'react';
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route } from "react-router-dom";
import App from './App'

class Source extends Component {
    state = {  }
    render() { 
        return ( 
            <Router>
                <Route path="/:lobbyId" component={App} />
            </Router>
        );
    }
}
 
export default Source;