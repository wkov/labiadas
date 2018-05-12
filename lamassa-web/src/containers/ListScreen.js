import React, { Component } from 'react';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import Hidden from 'material-ui/Hidden';
import SearchApp from '../components/SearchApp';
import MediaCard from '../components/MediaCard';
import CategoriesBar from '../components/CategoriesBar';
import { fetchList } from '../actions/apiActions';

class ListScreen extends Component {
  componentWillMount() {
    this.props.fetchList();
  }
  render() {
    const { data, productors, etiquetes } = this.props;
    if (data.length) {
      return (
        <div style={{ width: '-webkit-fill-available' }}>
          <SearchApp />
          <CategoriesBar etiquetes={etiquetes} />
          <Grid container spacing={0}>
            <Grid item xs={12} sm={12} md={12} lg={12}>
              <MediaCard data={data} productors={productors} etiquetes={etiquetes} />
            </Grid>
          </Grid>
        </div>
      );
    }
    return <div style={{ margin: '60px' }}>Cargando...</div>;
  }
}

const mapStateToProps = ({ api }) => {
  const { filteredMessages, productors, etiquetes } = api;
  return { data: filteredMessages, productors, etiquetes };
};

export default compose(
  withStyles(null, {
    withTheme: true,
    name: 'ListScreen',
  }),
  connect(mapStateToProps, { fetchList })
)(ListScreen);
