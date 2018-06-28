import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelActions from '@material-ui/core/ExpansionPanelActions';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';
import DeleteIcon from '@material-ui/icons/Delete';
import TextField from '@material-ui/core/TextField';
import Chip from '@material-ui/core/Chip';

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
  column: {
    flexBasis: '33.3%',
  },
  chip: {
    marginLeft: 5,
    marginRight: 10,
    height: '24px',
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

class ExpansionList extends React.Component {
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
    this.props.removeFromCart(this.props.cart, this.state.selectedItem);
    this.handleCloseConfirm();
  };

  render() {
    const { classes, cart } = this.props;

    return (
      <div className={classes.root}>
        {cart.map((value, index) => (
          <ExpansionPanel style={{ width: '80%' }} key={value.pk}>
            <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
              <div className={classes.column} style={{ display: 'flex' }}>
                <DeleteIcon onClick={() => this.handleClickOpenConfirm(value.pk)} style={{ marginRight: 20 }} />
                <Typography className={classes.heading}>{value.nom}</Typography>
              </div>
              <div className={classes.column} style={{ display: 'flex' }}>
                <Typography className={classes.secondaryHeading}>Quantitat: </Typography>
                <Chip label={value.cantitat} className={classes.chip} />
                <Typography className={classes.secondaryHeading}>Tipus: </Typography>
                <Chip label={value.format.nom + ` (${value.format.preu} €)`} className={classes.chip} />
                <Typography className={classes.secondaryHeading}>Total: </Typography>
                <Chip label={value.preu + ' €'} className={classes.chip} />
              </div>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails className={classes.details}>
              <div className={classes.column}>
                <img className={classes.img} alt="" src={'https://lamassa.org' + value.thumb} />
                <Typography className={classes.secondaryHeading}>{value.item.text_curt}</Typography>
              </div>
              <div className={classes.column}>
                <TextField
                  autoFocus
                  margin="dense"
                  id="dia"
                  label="Dia d'entrega:"
                  type="dia"
                  value={value.comanda.dia}
                />
                <TextField
                  autoFocus
                  margin="dense"
                  id="hora"
                  label="Franja Horària:"
                  type="hora"
                  value={value.comanda.hora}
                />
                <TextField
                  autoFocus
                  margin="dense"
                  id="frequencia"
                  label="Freqüència:"
                  type="frequencia"
                  value={value.comanda.frequencia}
                />
              </div>
              <div className={classNames(classes.column, classes.helper)}>
                <TextField
                  autoFocus
                  margin="dense"
                  id="quantitat"
                  label="Quantitat: "
                  type="quantitat"
                  value={value.comanda.quantitat}
                />
                <TextField
                  autoFocus
                  margin="dense"
                  id="tipus"
                  label="Format: "
                  type="tipus"
                  value={value.comanda.tipus.nom + ` (${value.comanda.tipus.preu} €)`}
                />
                <TextField
                  autoFocus
                  margin="dense"
                  id="hora"
                  label="Preu Total:"
                  type="hora"
                  value={value.comanda.preuTotal}
                />
              </div>
            </ExpansionPanelDetails>
            <Divider />
            <ExpansionPanelActions>
              <Button dense>Cancel·la</Button>
            </ExpansionPanelActions>
          </ExpansionPanel>
        ))}
        <DialogConfirm open={this.state.open} handleConfirm={this.handleDelete} handleClose={this.handleCloseConfirm} />
      </div>
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

ExpansionList.propTypes = {
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = state => {
  const { cart } = state.user;
  console.log(cart);
  return { cart };
};

export default compose(
  withStyles(styles, {
    name: 'ExpansionList',
  }),
  connect(mapStateToProps, { removeFromCart })
)(ExpansionList);
