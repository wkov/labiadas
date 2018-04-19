import React from 'react';
import PropTypes from 'prop-types';
import Button from 'material-ui/Button';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  withMobileDialog,
} from 'material-ui/Dialog';

class DialogConfirm extends React.Component {
  state = {
    open: false,
  };

  render() {
    const { open, handleClose, handleConfirm, fullScreen } = this.props;
    return (
      <div>
        <Dialog
          fullScreen={fullScreen}
          open={open}
          onClose={handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{'Vols treure de la cistella aquesta comanda?'}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              Vols treure de la cistella aquesta comanda?
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} color="primary">
              Cancel·lar
            </Button>
            <Button onClick={handleConfirm} color="primary" autoFocus>
              Confirmar
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

DialogConfirm.propTypes = {
  fullScreen: PropTypes.bool.isRequired,
};

export default withMobileDialog()(DialogConfirm);
