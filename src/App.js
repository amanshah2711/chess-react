// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";
import ChessHome from "./ChessHome"
import 'bootstrap/dist/css/bootstrap.min.css';
import {io} from 'socket.io-client';

function App() {
  
    var socket = io();
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    return (
        <div className="container justify-content-center margin-md p-5">
            <ChessHome socket={socket}/>
        </div>
    );
}
  
export default App;