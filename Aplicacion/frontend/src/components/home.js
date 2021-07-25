import React from 'react';
import { Link } from "react-router-dom";
import uuid from 'react-uuid'

const Home = () => {
    return(
        <div>
            <Link to={`${uuid()}`}>About</Link>
        </div>
    );
}
export default Home;