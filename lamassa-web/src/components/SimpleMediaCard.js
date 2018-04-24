import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from 'material-ui/styles';
import Card, { CardActions, CardContent, CardMedia, CardHeader } from 'material-ui/Card';
import StarRatingComponent from 'react-star-rating-component';
import ShoppingCartIcon from 'material-ui-icons/ShoppingCart';
import IconButton from 'material-ui/IconButton';
import FavoriteIcon from 'material-ui-icons/Favorite';
import Select from 'material-ui/Select';
import DialogForm from './DialogForm';
import { addToCart, addFavorites } from '../actions/userActions';

class SimpleMediaCard extends Component {
  state = {
    quantitat: 0,
    tipus: '',
    openDialogCart: false,
  };
  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };
  handleDialogForm({ openDialogCart }) {
    this.setState({ openDialogCart });
  }
  handleAddCart(item, comanda) {
    const { cart } = this.props;
    this.props.addToCart(item, comanda, cart);
  }
  handleAddFavorites(itemPk) {
    const { favorites } = this.props;
    this.props.addFavorites({ favorites, itemPk });
  }
  render() {
    const totalQuantitat = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
    const { producte, favorites } = this.props;
    return (
      <div>
        <Card className="card-review-product">
          <CardMedia className="image-review-card" image={`http://lamassa.org${producte.foto}`} title={producte.nom} />
          <CardHeader
            style={{ paddingBottom: 5 }}
            action={
              <div>
                <div>
                  <IconButton />
                  <IconButton onClick={() => this.handleAddFavorites(producte.pk)} aria-label="Afegir a preferits">
                    <FavoriteIcon
                      style={favorites.includes(producte.pk) ? { color: '#da6d76' } : { color: '#c4d97e' }}
                    />
                  </IconButton>
                </div>
                <div style={{ fontSize: 20 }}>
                  <div className="cards-text">3.0 Estrelles</div>
                  <StarRatingComponent name="rate" editing={false} starCount={5} value={3} />
                </div>
              </div>
            }
            title={<div className="cards-title">{producte.nom}</div>}
            subheader={
              <div>
                <div className="cards-subtitle">{producte.productora.nom}</div>
              </div>
            }
          />
          <CardContent>
            <div className="cards-text">{producte.text_curt}</div>
            <div style={{ display: 'flex' }}>
              <div className="cards-selector-label">Quantitat:</div>
              <Select
                native
                value={this.state.quantitat}
                onChange={this.handleChange('quantitat')}
                className="cards-selector-text"
              >
                {totalQuantitat.map(value => (
                  <option className="cards-selector-text" key={value} value={value}>
                    {value}
                  </option>
                ))}
              </Select>
              <div className="cards-selector-label">Formats:</div>
              <Select
                native
                value={this.state.tipus}
                onChange={this.handleChange('tipus')}
                className="cards-selector-text"
              >
                {producte.formats_dis.map((value, index) => (
                  <option className="cards-selector-text" key={value.nom} value={index}>
                    {value.preu + ' € - ' + value.nom}
                  </option>
                ))}
              </Select>
            </div>
          </CardContent>
          <CardActions>
            <IconButton
              style={{ marginLeft: 'auto' }}
              size="large"
              onClick={() => {
                this.handleDialogForm({ openDialogCart: true });
              }}
              color="default"
              component="span"
            >
              <ShoppingCartIcon style={{ color: 'black', fontSize: 28 }} />
            </IconButton>
          </CardActions>
        </Card>
        <DialogForm
          submitForm={this.handleAddCart.bind(this)}
          handleClose={() => {
            this.handleDialogForm({ openDialogCart: false });
          }}
          open={this.state.openDialogCart}
          item={producte}
          selected={{
            quantitat: !this.state.quantitat ? 1 : this.state.quantitat,
            tipus: !this.state.tipus ? producte.formats_dis[0] : producte.formats_dis[this.state.tipus],
          }}
        />
      </div>
    );
  }
}

SimpleMediaCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = state => {
  const { favorites, ts, cart } = state.user;
  return { favorites, ts, cart };
};

export default compose(
  withStyles(null, {
    name: 'SimpleMediaCard',
  }),
  connect(mapStateToProps, { addFavorites, addToCart })
)(SimpleMediaCard);
