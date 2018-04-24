import React from 'react';
import { Route, Switch } from 'react-router';
import ListScreen from './containers/ListScreen';
import AppBarTitle from './components/AppBarTitle';
import PrivateRoute from './containers/PrivateRoute';
import LoginScreen from './containers/LoginScreen';
import FooterBar from './components/FooterBar';

const styles = {
  appFrame: {
    // position: 'relative',
    // display: 'flex',
    backgroundColor: '#e9ffaf',
    // minHeight: '-webkit-fill-available',
    // height: '-webkit-fill-available',
    overflow: 'hidden',
  },
};

const App = ({ ...children }) => {
  return (
    <div style={styles.appFrame}>
      <AppBarTitle />
      <Switch>
        <PrivateRoute path="/" component={ListScreen} />
      </Switch>
      <footer>
        <FooterBar />
      </footer>
    </div>
  );
};

export default App;
