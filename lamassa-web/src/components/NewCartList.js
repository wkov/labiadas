import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import classNames from 'classnames';
import classnames from 'classnames';
import _ from 'lodash';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelActions from '@material-ui/core/ExpansionPanelActions';
import TableRow from '@material-ui/core/TableRow';
import TableHead from '@material-ui/core/TableHead';
import TableCell from '@material-ui/core/TableCell';
import TableBody from '@material-ui/core/TableBody';
import Table from '@material-ui/core/Table';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Button from '@material-ui/core/Button';
import Divider from '@material-ui/core/Divider';
import DeleteIcon from '@material-ui/icons/Delete';
import TextField from '@material-ui/core/TextField';
import Chip from '@material-ui/core/Chip';
import Paper from '@material-ui/core/Paper';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardHeader from '@material-ui/core/CardHeader';
import Collapse from '@material-ui/core/Collapse';
import IconButton from '@material-ui/core/IconButton';

import { removeFromCart } from '../actions/userActions';
import DialogConfirm from './DialogConfirm';

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
  expand: {
    transform: 'rotate(0deg)',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
    marginLeft: 'auto',
  },
  expandOpen: {
    transform: 'rotate(180deg)',
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
    flexBasis: '30%',
  },
  column: {
    flexBasis: '30%',
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

let id = 0;

function createData(name, calories, fat, carbs, protein) {
  id += 1;
  return { id, name, calories, fat, carbs, protein };
}

const data = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9),
];

class CartList extends React.Component {
  state = {
    expanded: [[false, false], [false, false], [false, false], [false, false], [false, false]],
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

  handleExpandClick = (pk, key) => {
    const { expanded } = this.state;
    expanded[pk][key] = !expanded[pk][key];
    this.setState(state => ({ expanded }));
  };

  render() {
    console.log(this.state.expanded);
    if (!this.state.expanded.length) {
      console.log('expanded');
    }
    const { classes, cart, newCart } = this.props;
    let preuTotal = 0;
    const newCom = _.map(newCart, (obj, key) => ({
      pk: key,
      comandes: _.map(obj, (obj2, key2) => ({ pk: key2, ...obj2 })),
    }));
    console.log(newCom);
    return (
      <div>
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <TableCell>Dessert (100g serving)</TableCell>
                <TableCell numeric>Calories</TableCell>
                <TableCell numeric>Fat (g)</TableCell>
                <TableCell numeric>Carbs (g)</TableCell>
                <TableCell numeric>Protein (g)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map(n => {
                return (
                  <TableRow key={n.id}>
                    <TableCell component="th" scope="row">
                      {n.name}
                    </TableCell>
                    <TableCell numeric>{n.calories}</TableCell>
                    <TableCell numeric>{n.fat}</TableCell>
                    <TableCell numeric>{n.carbs}</TableCell>
                    <TableCell numeric>{n.protein}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Paper>
        {newCom.map((com, pk) => (
          <Card key={pk} className="card-cistella ">
            <CardHeader
              title={<div className="cards-title">{this.props.title + ' ' + com.comandes[0].dia_entrega.date}</div>}
            />
            <CardContent>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Producte</TableCell>
                    <TableCell numeric>Quantitat</TableCell>
                    <TableCell numeric>Preu Unitat</TableCell>
                    <TableCell numeric>Preu Total</TableCell>
                    <TableCell numeric> </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {cart.map((value, index) => {
                    preuTotal = preuTotal + value.preu;
                    return (
                      <TableRow key={value.pk}>
                        <div>
                          <TableCell component="th" scope="row">
                            {`${value.producte} - ${value.format.nom}`}
                          </TableCell>
                          <TableCell numeric>{value.cantitat}</TableCell>
                          <TableCell numeric>{`(${value.format.preu} €)`}</TableCell>
                          <TableCell numeric>{value.preu + ' €'}</TableCell>
                          <TableCell numeric>
                            <IconButton
                              className={classnames(classes.expand, {
                                [classes.expandOpen]: this.state.expanded[pk][index],
                              })}
                              onClick={() => this.handleExpandClick(pk, index)}
                              aria-expanded={this.state.expanded[pk][index]}
                              aria-label="Show more"
                            >
                              <ExpandMoreIcon />
                            </IconButton>
                          </TableCell>
                        </div>
                        <div>
                          <Collapse in={this.state.expanded[pk][index]} timeout="auto" unmountOnExit>
                            <div className="card-cistella-columns">
                              <img
                                className={classes.img}
                                alt=""
                                src={'https://lamassa.org' + value.format.producte.thumb}
                              />
                              <Typography className={classes.secondaryHeading}>
                                {value.format.producte.text_curt}
                              </Typography>
                            </div>
                            <div className="card-cistella-columns">
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
                              <TextField
                                autoFocus
                                margin="dense"
                                id="hora"
                                label="Preu Total:"
                                type="hora"
                                value={value.preu}
                              />
                            </div>
                          </Collapse>
                        </div>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </CardContent>
            {this.props.edit ? (
              <CardActions>
                <div className="card-cart-total">
                  <div className="cards-text">Total: </div>
                  <Chip label={preuTotal + ' €'} className={classes.chip} />
                </div>
              </CardActions>
            ) : null}
            <DialogConfirm
              open={this.state.open}
              handleConfirm={this.handleDelete}
              handleClose={this.handleCloseConfirm}
            />
          </Card>
        ))}
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

CartList.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles, {
  name: 'CartList',
})(CartList);
