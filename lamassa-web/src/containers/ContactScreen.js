import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Typography } from 'material-ui/Typography';

class ContactScreen extends Component {
  render() {
    return (
      <div>
        weke
        <div> Contact form </div>
      </div>
    );
  }
}

const mapStateToProps = () => {};

export default connect(mapStateToProps, {})(ContactScreen);
