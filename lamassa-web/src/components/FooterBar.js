import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';

const styles = {
  root: {},
};

function FooterBar(props) {
  return (
    <div>
      <AppBar className="footer-bar" position="static">
        <div className="footer-text">www.lamassa.org - 2018</div>
      </AppBar>
    </div>
  );
}

FooterBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(FooterBar);
