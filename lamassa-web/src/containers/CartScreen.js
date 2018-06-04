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
    return (
      <div>
        <CartList title={'Properes entregues'} cart={this.props.cart} removeFromCart={this.props.removeFromCart} />
      </div>
    );
  }
}

const mapStateToProps = ({ user }) => {
  const { cart } = user;
  return { cart };
};

export default connect(mapStateToProps, { removeFromCart, fetchList })(CartScreen);
