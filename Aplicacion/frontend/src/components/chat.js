import React, {useEffect, useState } from 'react';
import { useParams } from "react-router-dom";
import { makeStyles, Paper, Container } from '@material-ui/core';
import io from 'socket.io-client';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import ChatBox from '../elements/chatBox';
import Sender from '../elements/sender';
import moment from "moment";
import FaceCat from "./faceCat";

const useStyles = makeStyles((theme) => ({
    root: {
      display: 'flex',
      flexDirection: 'column',
      '& > *': {
        margin: theme.spacing(2),
      },
    },
    Muicontainer: {
      display: 'flex',
      flexDirection: 'column',
      width: '500px',
      padding: '0px'
    },
    chatSection: {
      width: '100%',
      height: '85vh'
    },
    catFace: {
      padding: "auto",
    }
  }));

let socket;
const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const [mRecibido, setMRecibido] = useState("");
    const [mood, setMood] =  useState("");
    const classes = useStyles();
    const {roomId} = useParams();
    const ENDPOINT = 'localhost:5000';

    useEffect(() => {
      console.log("roomID")
        socket = io.connect(ENDPOINT, {
          withCredentials: true,
        });
        setInterval(()=>{
          socket.volatile.emit('keep_alive');
          //console.log('Keeping alive');
        },30000);
        socket.emit('join_room', roomId);
        //console.log(socket);
        return () => {
            socket.emit('leave_room');
            socket.off();
        }
    }, [roomId])

    const sendMessage = (e) => {
        e.preventDefault();
        const data = {
          message: message,
          roomId: roomId,
          sender: 0,
          createdAt: moment().format("DD-MM-YYYY hh:mm:ss"),
        }
        if(message !== "" && message ){
          socket.emit('send_message', data);
          setMessages([...messages, data]);
        }
        setMessage("");
        setMood(message)
        console.log("-------",message);
    }

    useEffect(() => {
      console.log("mensaje recibido")
        socket.on('receive_message', (msjRecibido) => {
          if(messages !== null){
            setMessages([...messages, msjRecibido]);
            setMRecibido(msjRecibido);
            //setMood(msjRecibido);
          }
        })
    },[messages])
    
    return (
      <Container classes={{ root: classes.Muicontainer }}>
      <div>
        {console.log("componente principal renderizado")}
        <FaceCat sentence={mood}></FaceCat>
        <Grid container component={ Paper } className={ classes.chatSection }>
            <Grid item xs={12} item={true}>
            {messages && (
              <ChatBox messages={ messages }/>
              )}
            <Divider />
              <Sender message={ message } setMessage={ setMessage } sendMessage={ sendMessage }/>
            </Grid>
        </Grid>
      </div>
      </Container>  
    );
}
export default Chat;