import React from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Fab from '@material-ui/core/Fab';
import SendIcon from '@material-ui/icons/Send';

const Sender = (props) => {
    return(
        <Grid container style={{padding: '20px'}}>
            <Grid item xs={10}>
                <TextField id="outlined-basic-email" label="Escribe un mensaje aquí." fullWidth value={props.message} onChange={(e) => {props.setMessage(e.target.value)}}/>
            </Grid>
            <Grid xs={1} align="right">
                <Fab color="#6d3878" aria-label="add" onClick={e => props.sendMessage(e)}><SendIcon /></Fab>
            </Grid>
        </Grid>
    )
} 
export default Sender;