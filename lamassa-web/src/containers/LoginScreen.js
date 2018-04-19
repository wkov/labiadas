import React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router';

import LoginForm from '../components/LoginForm';
import { login } from '../actions/authActions';
import { authErrors, isAuthenticated } from '../reducers';

const LoginScreen = props => {
  if (props.isAuthenticated) {
    return <Redirect to={props.location.state.from} />;
  }
  return (
    <div className="container-screen">
      <LoginForm {...props} />
    </div>
  );
};

const mapStateToProps = state => ({
  errors: authErrors(state),
  isAuthenticated: isAuthenticated(state),
});

const mapDispatchToProps = dispatch => ({
  onSubmit: (username, password) => {
    dispatch(login(username, password));
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(LoginScreen);
