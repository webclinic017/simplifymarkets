import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import mainLogo from '../images/logo.png'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    marginBottom: '5rem',
  },

  appBar: {
    background: '#F8F8F8'
  },

  menuButton: {
    marginRight: theme.spacing(2),
  },

  logoContainer: {
    flexGrow: 1,
  },

  logo: {
    height: '2.1rem'
  }

}));

export default function ButtonAppBar() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar>
          <IconButton edge="start" className={classes.menuButton} aria-label="menu">
            <MenuIcon />
          </IconButton>
          <div className={classes.logoContainer}>
            <img className={classes.logo} src={mainLogo} alt="Simplify Markets" ></img>
          </div>
          <Button>Login</Button>
        </Toolbar>
      </AppBar>
    </div>
  );
}
