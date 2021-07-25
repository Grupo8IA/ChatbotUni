import React, { Component } from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route} from "react-router-dom";
import Chat from './components/chat';
import Home from './components/home';

export default class App extends Component {
  render(){
    return (
      <Router>
        <div className="App">
              <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/:roomId" exact component={Chat}/>
              </Switch>
        </div>
      </Router>
    );
  }
}