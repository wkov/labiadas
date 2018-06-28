import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import IconButton from '@material-ui/core/IconButton';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import Hidden from '@material-ui/core/Hidden';

import { handleDrawer } from '../actions/userActions';
import DrawerIcons from './utils/DrawerIcons';

const drawerWidth = 240;

const styles = theme => ({
  drawerPaper: {
    zIndex: 1200,
    top: 0,
    position: 'fixed',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    backgroundColor: '#90ae68',
  },
  drawerPaperClose: {
    zIndex: 10,
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing.unit * 7,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing.unit * 9,
    },
    backgroundColor: '#90ae68',
  },
  drawerInner: {
    // Make the items inside not wrap when transitioning:
    width: drawerWidth,
  },
  drawerHeader: {
    height: 70,
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
    console.log('Drawer;', open, theme);
    return (
      <div>
        <Hidden smDown>
          <Drawer
            variant="permanent"
            classes={{
              paper: classNames(classes.drawerPaper, !(open ? open : false) && classes.drawerPaperClose),
            }}
            open={open ? open : false}
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
            variant="persistent"
            classes={{
              paper: classNames(classes.drawerPaper),
            }}
            open={open ? open : false}
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
