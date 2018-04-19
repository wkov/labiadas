import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { connect } from 'react-redux';
import compose from 'recompose/compose';

import { Link } from 'react-router-dom';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import Menu, { MenuItem } from 'material-ui/Menu';
import AccountCircle from 'material-ui-icons/AccountCircle';

import * as reducers from '../reducers';
import { userLogout } from '../actions/authActions';
import { handleDrawer } from '../actions/userActions';
import './AppBarTitle.css';

const drawerWidth = 240;

const styles = theme => ({
  appFrame: {
    overflow: 'hidden',
  },
  appBar: {
    position: 'fixed',
    width: drawerWidth,
    backgroundColor: 'transparent',
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 15,
  },
  hide: {
    display: 'none',
  },
});

class AppBarTitle extends Component {
  state = {
    open: false,
    anchorEl: null,
  };

  handleMenu = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  handleClose = () => {
    this.setState({ anchorEl: null });
  };

  handleDrawerOpen = () => {
    this.props.handleDrawer({ open: true });
  };

  handleDrawerClose = () => {
    this.props.handleDrawer({ open: false });
  };

  handleLogout() {
    this.props.userLogout();
  }

  render() {
    const { classes, isAuthenticated, userInfo } = this.props;
    const { anchorEl } = this.state;
    const openProfileMenu = Boolean(anchorEl);

    return (
      <div className="appbar-menu-button">
        <IconButton
          color="contrast"
          aria-label="open drawer"
          onClick={this.handleDrawerOpen}
          className={classNames(classes.menuButton, this.props.open && classes.hide)}
        >
          <MenuIcon />
        </IconButton>
      </div>
    );
  }
}

AppBarTitle.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

const mapStateToProps = state => ({
  isAuthenticated: reducers.isAuthenticated(state),
  open: state.user.open,
  userInfo: state.user.user,
});

export default compose(
  withStyles(styles, { name: 'AppBarTitle', withTheme: true }),
  connect(mapStateToProps, { userLogout, handleDrawer })
)(AppBarTitle);
