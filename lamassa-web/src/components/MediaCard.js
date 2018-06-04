import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import compose from 'recompose/compose';
import { withStyles } from 'material-ui/styles';
import Card, { CardHeader, CardContent, CardActions } from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import FavoriteIcon from 'material-ui-icons/Favorite';
import ShoppingCartIcon from 'material-ui-icons/ShoppingCart';
import MessageIcon from 'material-ui-icons/Message';
import Button from 'material-ui/Button';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import Select from 'material-ui/Select';
import { ListItemIcon } from 'material-ui/List';
import StarRatingComponent from 'react-star-rating-component';
import { addFavorites } from '../actions/userActions';
import { addRemoveItem } from '../actions/apiActions';
import { addToCart } from '../actions/userActions';
import DialogForm from './DialogForm';

const totalQuantitat = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

const styles = theme => ({
  gridItem: {
    padding: 10,
  },
  card: {
    width: 380,
    height: 380,
    backgroundColor: '#ebf9d6',
  },
  media: {
    maxWidth: 150,
    height: 150,
  },
  tipus: {
    flex: 'auto',
  },
  container: {
    display: 'flex',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 50,
  },
  selectEmpty: {
    marginLeft: 10,
  },
  button: {
    margin: theme.spacing.unit,
  },
  text: {
    textDecoration: 'none',
    color: '#508a4c',
    fontFamily: 'Satisfy',
    fontSize: 'larger',
  },
  div: {
    display: 'flex',
    flexGrow: 1,
  },
});

const url = 'http://localhost:8000';

class MediaCard extends Component {
  componentWillMount() {
    this.setState({
      openDialogCart: [],
      quantitat: [],
      tipus: [],
    });
  }

  handleDialogForm({ openDialogCart }) {
    this.setState({ openDialogCart });
  }

  handleAddFavorites(itemPk) {
    const { favorites } = this.props;
    this.props.addFavorites({ favorites, itemPk });
  }

  handleChange = (name, index) => event => {
    const element = this.state[name];
    element[index] = event.target.value;
    this.setState({
      element,
    });
  };
  handleAddCart(comanda) {
    const { cart } = this.props;
    // this.props.addToCart(item, comanda, cart);
    this.props.addToCart(comanda);
  }
  render() {
    const { classes, data, favorites, isFavorites } = this.props;
    return (
      <Grid container alignItems={'center'} spacing={24} direction={'row'} justify={'center'}>
        {data.map((value, index) => {
          if (!isFavorites || favorites.some(prod => prod.pk === value.pk)) {
            return (
              <Grid className={classes.gridItem} item key={value.nom}>
                <Card className="cards-list">
                  <CardHeader
                    style={{ paddingBottom: 5 }}
                    action={
                      <div>
                        <div>
                          <IconButton />
                          <IconButton onClick={() => this.handleAddFavorites(value.pk)} aria-label="Afegir a preferits">
                            <FavoriteIcon
                              style={
                                favorites.some(prod => prod.pk === value.pk)
                                  ? { color: '#da6d76' }
                                  : { color: '#c4d97e' }
                              }
                            />
                          </IconButton>
                        </div>
                        <div style={{ fontSize: 20 }}>
                          <StarRatingComponent name="rate" editing={false} starCount={5} value={value.estrelles} />
                        </div>
                      </div>
                    }
                    title={
                      <div className="title-cards">
                        <Link className="cards-title" to={`/producte/${value.pk}`}>
                          {value.nom}
                        </Link>
                        <ListItemIcon>
                          <img style={{ marginLeft: 10 }} alt="" src={url + value.etiqueta.img} />
                        </ListItemIcon>
                      </div>
                    }
                    subheader={
                      <div style={{ display: 'flex' }}>
                        <Typography type="button">
                          <a className="cards-subtitle" href="http://www.yahoo.com">
                            {value.productora.nom}
                          </a>
                        </Typography>
                        <Link to={`/contacte/productora=${value.productora.nom.replace(/\s/g, '')}`}>
                          <MessageIcon style={{ marginLeft: 10 }} />
                        </Link>
                      </div>
                    }
                  />
                  <div className="cards-media-container">
                    <img alt="" src={url + value.thumb} href={url + value.foto} className="cards-image" />
                    <CardContent>
                      <div className="cards-text">{value.text_curt}</div>
                    </CardContent>
                  </div>
                  <div className={(classes.formControl, 'form-card-select-product')}>
                    <div className="cards-selector-label">Quant:</div>
                    <Select
                      native
                      value={this.state.quantitat[index]}
                      onChange={this.handleChange('quantitat', index)}
                      className={(classes.selectEmpty, 'cards-selector-text')}
                    >
                      {totalQuantitat.map(value => (
                        <option className="cards-selector-text" key={value} value={value}>
                          {value}
                        </option>
                      ))}
                    </Select>
                    <div className="cards-selector-label">Format:</div>
                    <Select
                      native
                      value={this.state.tipus[index]}
                      onChange={this.handleChange('tipus', index)}
                      className={(classes.selectEmpty, 'cards-selector-text')}
                    >
                      {value.formats_dis.map((value, index) => (
                        <option className="cards-selector-text" key={value.nom} value={index}>
                          {value.preu + ' € - ' + value.nom}
                        </option>
                      ))}
                    </Select>
                  </div>
                  <CardActions className={classes.container} disableActionSpacing>
                    <Button
                      style={{ marginLeft: 'auto' }}
                      dense
                      onClick={() => {
                        const { openDialogCart } = this.state;
                        openDialogCart[index] = true;
                        this.handleDialogForm({ openDialogCart });
                      }}
                      color="default"
                    >
                      <ShoppingCartIcon style={{ color: 'black' }} />
                    </Button>
                    <DialogForm
                      submitForm={this.handleAddCart.bind(this)}
                      handleClose={() => {
                        const { openDialogCart } = this.state;
                        openDialogCart[index] = false;
                        this.handleDialogForm({ openDialogCart });
                      }}
                      open={this.state.openDialogCart[index]}
                      item={value}
                      selected={{
                        quantitat: !this.state.quantitat[index] ? 1 : this.state.quantitat[index],
                        tipus: !this.state.tipus[index]
                          ? value.formats_dis[0]
                          : value.formats_dis[this.state.tipus[index]],
                      }}
                    />
                  </CardActions>
                </Card>
              </Grid>
            );
          } else {
            return null;
          }
        })}
      </Grid>
    );
  }
}

MediaCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = state => {
  const { ts, cart } = state.user;
  return {
    favorites: state.user.user.preferits,
    ts,
    cart,
  };
};

export default compose(
  withStyles(styles, {
    name: 'MediaCard',
  }),
  connect(mapStateToProps, { addFavorites, addToCart, addRemoveItem })
)(MediaCard);
