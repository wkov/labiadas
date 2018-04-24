import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Drawer from 'material-ui/Drawer';
import List from 'material-ui/List';
import IconButton from 'material-ui/IconButton';
import ChevronLeftIcon from 'material-ui-icons/ChevronLeft';
import ChevronRightIcon from 'material-ui-icons/ChevronRight';
import Hidden from 'material-ui/Hidden';

import { handleDrawer } from '../actions/userActions';
import DrawerIcons from './utils/DrawerIcons';

const drawerWidth = 240;

const styles = theme => ({
  drawerPaper: {
    top: 50,
    position: 'fixed',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    backgroundColor: '#90ae68',
  },
  drawerPaperClose: {
    width: 60,
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    backgroundColor: '#90ae68',
  },
  drawerInner: {
    // Make the items inside not wrap when transitioning:
    width: drawerWidth,
  },
  drawerHeader: {
    height: 30,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
    minHeight: '30px !important',
  },
});

class DrawerBar extends Component {
  handleDrawerClose() {
    this.props.handleDrawer({ open: false });
  }

  render() {
    const { open, classes, theme } = this.props;
    return (
      <div>
        <Hidden smDown>
          <Drawer
            type="permanent"
            classes={{
              paper: classNames(classes.drawerPaper, !open && classes.drawerPaperClose),
            }}
            open={open}
          >
            <div className={classes.drawerInner}>
              <div className={classes.drawerHeader}>
                <IconButton onClick={this.handleDrawerClose.bind(this)}>
                  {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
                </IconButton>
              </div>
              <List>
                <DrawerIcons />
              </List>
            </div>
          </Drawer>
        </Hidden>
        <Hidden mdUp>
          <Drawer
            type="persistent"
            classes={{
              paper: classNames(classes.drawerPaper),
            }}
            open={open}
          >
            <div className={classes.drawerInner}>
              <div className={classes.drawerHeader}>
                <IconButton onClick={this.handleDrawerClose.bind(this)}>
                  {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
                </IconButton>
              </div>
              <List>
                <DrawerIcons />
              </List>
            </div>
          </Drawer>
        </Hidden>
      </div>
    );
  }
}

DrawerBar.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

const mapStateToProps = ({ user }) => {
  return { open: user.open };
};

export default compose(withStyles(styles, { withTheme: true }), connect(mapStateToProps, { handleDrawer }))(DrawerBar);
