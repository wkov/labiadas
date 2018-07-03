import React, { Component } from 'react';
import { connect } from 'react-redux';
import CartList from '../components/CartList';
import NewCartList from '../components/NewCartList';
import CartTable from '../components/CartTable';
import TabsComponent from '../components/TabsComponent';
import Typography from '@material-ui/core/Typography';
import { removeFromCart } from '../actions/userActions';
import { fetchList } from '../actions/apiActions';

class CartScreen extends Component {
  componentWillMount() {
    this.props.fetchList();
  }
  render() {
    console.log(this.props.newCart);
    if (!this.props.historial) {
      return <div>Cargando..</div>;
    }
    return (
      <TabsComponent
        tabOne={<CartTable cart={this.props.newCart} removeFromCart={this.props.removeFromCart} edit />}
        tabTwo={<CartTable cart={this.props.newHist} />}
      />
    );
  }
}

// <NewCartList
//   title={'Cistella'}
//   cart={this.props.cart}
//   newCart={this.props.newCart}
//   removeFromCart={this.props.removeFromCart}
//   edit
// />
// <CartList title={'Properes entregues'} cart={this.props.cart} removeFromCart={this.props.removeFromCart} edit />
// <CartList title={'Historial comandes'} cart={this.props.historial} removeFromCart={this.props.removeFromCart} />

const mapStateToProps = ({ user }) => {
  const { newCart, cart, historial, newHist } = user;
  console.log(user);
  return { cart, newCart, historial, newHist };
};

export default connect(mapStateToProps, { removeFromCart, fetchList })(CartScreen);
