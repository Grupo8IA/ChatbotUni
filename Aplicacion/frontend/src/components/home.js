import React from 'react';
import { Link } from "react-router-dom";
import uuid from 'react-uuid'

const Home = () => {
    return(
        <div className="Container">
            <h2 className="Title">Chatbot UNI</h2>
            <img src="https://image.flaticon.com/icons/png/512/1766/1766895.png" alt="Robot" width="80"></img>
            <Link to={`${uuid()}`}>
                <div className="Button">¡Comenzar!</div>
            </Link>
        </div>
    );
}
export default Home;