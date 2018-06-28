import React, { Component } from 'react';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Hidden from '@material-ui/core/Hidden';
import SearchApp from '../components/SearchApp';
import MediaCard from '../components/MediaCard';
import CategoriesBar from '../components/CategoriesBar';
import { fetchList } from '../actions/apiActions';

class PreferScreen extends Component {
  componentWillMount() {
    this.props.fetchList();
  }

  render() {
    const { data, productors, etiquetes } = this.props;
    if (data.length) {
      return (
        <div style={{ width: '-webkit-fill-available' }}>
          <SearchApp />
          <Grid container spacing={0}>
            <Hidden smDown>
              <Grid item md={1} lg={2}>
                <Hidden mdDown>
                  <CategoriesBar etiquetes={etiquetes} />
                </Hidden>
              </Grid>
            </Hidden>
            <Grid item xs={12} sm={12} md={10} lg={10}>
              <MediaCard isFavorites data={data} productors={productors} etiquetes={etiquetes} />
            </Grid>
          </Grid>
        </div>
      );
    }
    return <div> CARGANDO... </div>;
  }
}

const mapStateToProps = ({ api }) => {
  const { filteredMessages, productors, etiquetes } = api;
  return { data: filteredMessages, productors, etiquetes };
};

export default compose(
  withStyles(null, {
    withTheme: true,
    name: 'PreferScreen',
  }),
  connect(mapStateToProps, { fetchList })
)(PreferScreen);
