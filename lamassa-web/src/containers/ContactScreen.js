import React, { Component } from 'react';
import { connect } from 'react-redux';

class ContactScreen extends Component {
  render() {
    return <div>contactform</div>;
  }
}

const mapStateToProps = () => {};

export default connect(mapStateToProps, {})(ContactScreen);
