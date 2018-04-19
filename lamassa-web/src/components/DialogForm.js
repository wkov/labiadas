import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle, // eslint-disable-next-line
  withMobileDialog,
} from 'material-ui/Dialog';

import DialogCalendar from './DialogCalendar';
import StepperCart from './StepperCart';

const frequencies = {
  1: 'Una sola vegada',
  2: 'Cada Setmana',
  3: 'Cada 2 Setmanes',
  4: 'Cada 4 Setmanes',
};

const styles = {
  containerTextImg: {
    display: 'flex',
  },
  img: {
    maxHeight: 200,
    padding: 30,
  },
};

class DialogForm extends Component {
  state = {
    open: false,
    entrega: '',
    openDialogCalendar: false,
    frequencia: '',
  };

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  render() {
    const { fullScreen, handleClose, open, item, selected } = this.props;
    const entrega = {
      dia: ['Dilluns 17', 'Dilluns 23', 'Dilluns 29'],
      hora: ['13:00-14:00', '19:00-20:00'],
      frequencia: ['una sola vegada', 'cada 2 setmanes', 'cada 4 setmanes'],
    };

    return (
      <Dialog
        fullScreen={fullScreen}
        open={open ? open : false}
        onClose={handleClose}
        aria-labelledby="responsive-dialog-title"
      >
        <DialogTitle id="responsive-dialog-title">{'Nova Comanda: '}</DialogTitle>
        <DialogContent>
          <DialogContentText />
          <div style={styles.containerTextImg}>
            <div>
              <TextField
                autoFocus
                margin="dense"
                id="producte"
                label="Producte:"
                type="producte"
                fullWidth
                value={item.nom}
              />
              <TextField
                autoFocus
                margin="dense"
                id="tipus"
                label="Format:"
                type="tipus"
                value={selected.tipus ? selected.tipus.nom + ` (${selected.tipus.preu} €)` : null}
              />
              <TextField
                autoFocus
                margin="dense"
                id="quantitat"
                label="Quantitat:"
                type="quantitat"
                fullWidth
                value={selected.quantitat}
              />
              <TextField
                autoFocus
                margin="dense"
                id="preu"
                label="Preu Total:"
                type="preu"
                fullWidth
                value={selected.tipus ? selected.tipus.preu * selected.quantitat : null}
              />
            </div>
            <img alt="" src="/item_espelta.jpg" style={styles.img} />
          </div>
          <StepperCart
            data={selected}
            submit={this.addCart.bind(this)}
            onChangeFrequencia={value => this.setState({ frequencia: frequencies[value] })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel·la
          </Button>
        </DialogActions>
        <DialogCalendar
          dies={selected.tipus.dies_stocks_futurs}
          frequencia={this.state.frequencia}
          open={this.state.openDialogCalendar}
          handleClose={this.handleDialogCalendar}
        />
      </Dialog>
    );
  }
  handleDialogCalendar = () => {
    this.setState({ openDialogCalendar: false });
  };
  addCart(entrega) {
    const { item, selected } = this.props;
    const comanda = { ...selected, ...entrega, preuTotal: selected.tipus.preu * selected.quantitat };
    if (comanda.frequencia === 1) {
      this.props.submitForm(item, comanda);
      this.props.handleClose();
    } else {
      this.setState({ openDialogCalendar: true });
    }
  }
}

DialogForm.propTypes = {
  fullScreen: PropTypes.bool.isRequired,
};

export default withMobileDialog()(DialogForm);
