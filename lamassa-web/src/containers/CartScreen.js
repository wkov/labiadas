import React, { Component } from 'react';
import { connect } from 'react-redux';
import CartList from '../components/CartList';
import Typography from 'material-ui/Typography';
import { removeFromCart } from '../actions/userActions';
import { fetchList } from '../actions/apiActions';

class CartScreen extends Component {
  componentWillMount() {
    this.props.fetchList();
  }
  render() {
    console.log(this.props.historial);
    if (!this.props.historial) {
      return <div>Cargando..</div>;
    }
    return (
      <div>
        <CartList title={'Properes entregues'} cart={this.props.cart} removeFromCart={this.props.removeFromCart} edit />
        <CartList title={'Historial comandes'} cart={this.props.historial} removeFromCart={this.props.removeFromCart} />
      </div>
    );
  }
}

const mapStateToProps = ({ user }) => {
  const { cart, historial } = user;
  return { cart, historial };
};

export default connect(mapStateToProps, { removeFromCart, fetchList })(CartScreen);
