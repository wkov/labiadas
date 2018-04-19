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

class PreferScreen extends Component {
  componentWillMount() {
    this.props.fetchList();
  }

  render() {
    const { data, productors, etiquetes } = this.props;
    return (
      <div style={{ width: '-webkit-fill-available' }}>
        <main>
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
        </main>
      </div>
    );
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
