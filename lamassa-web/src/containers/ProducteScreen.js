import React, { Component } from 'react';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import SimpleMediaCard from '../components/SimpleMediaCard';
import MediaCard from '../components/MediaCard';
import ProductReviews from '../components/ProductReviews';
import { fetchProduct } from '../actions/apiActions';

class ProducteScreen extends Component {
  state = {
    product: '',
  };
  componentWillMount() {
    console.log('mounting');
    if (this.props.match.params.product) {
      console.log('mounting2');
      this.props.fetchProduct({ term: this.props.match.params.product });
      this.setState({ product: this.props.match.params.product });
    }
  }
  componentDidUpdate() {
    if (this.props.match.params.product !== this.state.product) {
      this.props.fetchProduct({ term: this.props.match.params.product });
      this.setState({ product: this.props.match.params.product });
      window.scrollTo(0, 0);
    }
  }
  render() {
    const { reviewedProduct, productsProducer, productors, etiquetes } = this.props;
    if (reviewedProduct && productsProducer) {
      return (
        <div style={{ width: '-webkit-fill-available' }}>
          <Grid container>
            <Grid item xs={12} sm={12} md={6}>
              <SimpleMediaCard producte={reviewedProduct} productsProducer={productsProducer} />
            </Grid>
            <Grid item xs={12} sm={12} md={6}>
              <ProductReviews />
            </Grid>
            <Grid item xs={12} sm={12} md={12} lg={12}>
              <div className="cards-title"> DEL MATEIX PRODUCTOR/A: </div>
              <br />
              <MediaCard data={productsProducer} productors={productors} etiquetes={etiquetes} />
            </Grid>
          </Grid>
        </div>
      );
    }
    return <div> CARGANDO...</div>;
  }
}

const mapStateToProps = ({ api }) => {
  const { reviewedProduct, productsProducer, productors, etiquetes } = api;
  return { reviewedProduct, productsProducer, productors, etiquetes };
};

export default compose(
  withStyles(null, {
    withTheme: true,
    name: 'ProducteScreen',
  }),
  connect(mapStateToProps, { fetchProduct })
)(ProducteScreen);
