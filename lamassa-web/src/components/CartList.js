import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import ExpansionPanel, {
  ExpansionPanelDetails,
  ExpansionPanelSummary,
  ExpansionPanelActions,
} from 'material-ui/ExpansionPanel';
import Typography from 'material-ui/Typography';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import Button from 'material-ui/Button';
import Divider from 'material-ui/Divider';
import DeleteIcon from 'material-ui-icons/Delete';
import TextField from 'material-ui/TextField';
import Chip from 'material-ui/Chip';
import Card, { CardActions, CardContent, CardHeader } from 'material-ui/Card';

import { removeFromCart } from '../actions/userActions';
import DialogConfirm from './DialogConfirm';

const styles = theme => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
  icon: {
    verticalAlign: 'bottom',
    height: 20,
    width: 20,
  },
  details: {
    alignItems: 'center',
  },
  firstColumn: {
    flexBasis: '10%',
  },
  column: {
    flexBasis: '20%',
  },
  helper: {
    borderLeft: `2px solid ${theme.palette.text.lightDivider}`,
    padding: `${theme.spacing.unit}px ${theme.spacing.unit * 2}px`,
  },
  link: {
    color: theme.palette.primary.main,
    textDecoration: 'none',
    '&:hover': {
      textDecoration: 'underline',
    },
  },
  img: {
    maxHeight: 150,
    marginRight: 30,
  },
  divider: {},
  text: {},
});

class CartList extends React.Component {
  state = {
    expanded: null,
    tipus: '',
    quantitat: 0,
    open: false,
  };

  handleChange = panel => (event, expanded) => {
    this.setState({
      expanded: expanded ? panel : false,
    });
  };
  handleChangeSelection = name => event => {
    this.setState({ [name]: event.target.value });
  };

  handleDelete = () => {
    this.props.removeFromCart(this.state.selectedItem);
    this.handleCloseConfirm();
  };

  render() {
    const { classes, cart } = this.props;
    let preuTotal = 0;

    return (
      <Card className="card-review-product ">
        <CardHeader title={<div className="cards-title">{this.props.title}</div>} />
        <CardContent>
          <ExpansionPanel expanded={false}>
            <ExpansionPanelSummary>
              <div className={classes.firstColumn} style={{ display: 'flex' }}>
                .
              </div>
              <div className="cart-details">
                <div className={classes.column}>Producte:</div>
                <div className={classes.column}>Format:</div>
                <div className={classes.column}>Entrega:</div>
                <div className={classes.column}>Preu Unitat:</div>
                <div className={classes.column}>Quantitat:</div>
                <div className={classes.column}>Total:</div>
              </div>
            </ExpansionPanelSummary>
            <Divider />
          </ExpansionPanel>
          {cart.map((value, index) => {
            preuTotal = preuTotal + value.preu;
            return (
              <ExpansionPanel key={value.pk}>
                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                  <div className={classes.firstColumn} style={{ display: 'flex' }}>
                    {this.props.edit ? (
                      <DeleteIcon onClick={() => this.handleClickOpenConfirm(value.pk)} style={{ marginRight: 20 }} />
                    ) : null}
                  </div>

                  <div className="cart-details">
                    <div className={classes.column}>{value.producte}</div>
                    <div className={classes.column}>
                      <Chip label={value.format.nom} className="cart-chips" />
                    </div>
                    <div className={classes.column}>
                      <Chip
                        label={new Date(value.entregas[0].dia_entrega.date).toLocaleDateString()}
                        className="cart-chips"
                      />
                    </div>
                    <div className={classes.column}>
                      <Chip label={`(${value.format.preu} €)`} className="cart-chips" />
                    </div>
                    <div className={classes.column}>
                      <Chip label={value.cantitat} className="cart-chips" />
                    </div>
                    <div className={classes.column}>
                      <Chip label={value.preu + ' €'} className="cart-chips" />
                    </div>
                  </div>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails className={classes.details}>
                  <div className={classes.column}>
                    <img className={classes.img} alt="" src={'https://lamassa.org' + value.format.producte.thumb} />
                    <Typography className={classes.secondaryHeading}>{value.format.producte.text_curt}</Typography>
                  </div>
                  <div className={classes.column}>
                    <TextField
                      autoFocus
                      margin="dense"
                      id="dia"
                      label="Dia d'entrega:"
                      type="dia"
                      value={'value.data_entrega'}
                    />
                    <TextField
                      autoFocus
                      margin="dense"
                      id="hora"
                      label="Franja Horària:"
                      type="hora"
                      value={'value.franja_horaria'}
                    />
                    <TextField
                      autoFocus
                      margin="dense"
                      id="frequencia"
                      label="Freqüència:"
                      type="frequencia"
                      value={'value.frequencia'}
                    />
                  </div>
                  <div className={classNames(classes.column, classes.helper)}>
                    <TextField
                      autoFocus
                      margin="dense"
                      id="quantitat"
                      label="Quantitat: "
                      type="quantitat"
                      value={value.cantitat}
                    />
                    <TextField
                      autoFocus
                      margin="dense"
                      id="tipus"
                      label="Format: "
                      type="tipus"
                      value={value.format.nom + ` (${value.format.preu} €)`}
                    />
                    <TextField autoFocus margin="dense" id="hora" label="Preu Total:" type="hora" value={value.preu} />
                  </div>
                </ExpansionPanelDetails>
                <Divider />
                <ExpansionPanelActions>
                  <Button dense>Cancel·la</Button>
                </ExpansionPanelActions>
              </ExpansionPanel>
            );
          })}
        </CardContent>
        {this.props.edit ? (
          <CardActions>
            <div className="card-cart-total">
              <div className="cards-text">Total: </div>
              <Chip label={preuTotal + ' €'} className={classes.chip} />
            </div>
          </CardActions>
        ) : null}
        <DialogConfirm open={this.state.open} handleConfirm={this.handleDelete} handleClose={this.handleCloseConfirm} />
      </Card>
    );
  }

  handleClickOpenConfirm = itemPk => {
    this.setState({
      open: true,
      selectedItem: itemPk,
    });
  };

  handleCloseConfirm = () => {
    this.setState({ open: false });
  };
}

CartList.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles, {
  name: 'CartList',
})(CartList);
