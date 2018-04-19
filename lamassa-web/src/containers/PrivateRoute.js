import React from 'react';
import { Route, Redirect, Switch } from 'react-router';
import { connect } from 'react-redux';

import * as reducers from '../reducers';
import DrawerBar from '../components/DrawerBar';
import ListScreen from './ListScreen';
import PreferScreen from './PreferScreen';
import CartScreen from './CartScreen';
import ProducteScreen from './ProducteScreen';
import UserProfileScreen from './UserProfileScreen';

const styles = {
  appFrame: {
    position: 'relative',
    display: 'flex',
    width: '-webkit-fill-available',
    minHeight: '-webkit-fill-available',
    // height: '100%',
  },
  appScreens: {
    paddingTop: 24,
    marginTop: 56,
    // paddingLeft: 54,
    // height: '100%',
  },
};

const PrivateRoute = ({ component: Component, isAuthenticated, ...rest }) => {
  if (true) {
    console.log(props);
    return (
      <div style={styles.appFrame}>
        <DrawerBar />
        <div className="container-screen">
          <Switch>
            <Route path="/cart" component={CartScreen} />
            <Route path="/preferits" component={PreferScreen} />
            <Route path="/userprofile" component={UserProfileScreen} />
            <Route path="/producte/:product" component={ProducteScreen} />
            <Route path="/" component={ListScreen} />
          </Switch>
        </div>
      </div>
    );
  }
  return (
    <Redirect
      to={{
        pathname: '/login',
        state: { from: rest.location.pathname },
      }}
    />
  );
};

const mapStateToProps = state => ({
  isAuthenticated: reducers.isAuthenticated(state),
});

export default connect(mapStateToProps, null)(PrivateRoute);
