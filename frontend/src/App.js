import './App.css';
import ButtonAppBar from './components/ButtonAppBar'

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import FastRewindIcon from '@material-ui/icons/FastRewind';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';

const useStyles = makeStyles((theme) => ({
  layout: {
    display: 'flex',
    margin: 'auto',
    maxWidth: 'fit-content',
    marginTop: '10rem'
  },

  menu: {
    padding: 10,

    '& > *': {
      margin: theme.spacing(1),
    },
  }
}));

function App() {
  
  const classes = useStyles();

  return (
    <div className="App">
      <ButtonAppBar></ButtonAppBar>
      <div className={classes.layout}>
        <Paper className={classes.menu} variant="outlined"> 
          <Button variant="contained" className={classes.button} startIcon={<FastRewindIcon />}>
            Backtest
          </Button>
          <Button variant="contained" className={classes.button} startIcon={<CloudUploadIcon />}>
            Scanner
          </Button>
        </Paper>
      </div>
    </div>
}

export default App;