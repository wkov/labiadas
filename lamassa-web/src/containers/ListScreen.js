import React, { Component } from 'react';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Hidden from '@material-ui/core/Hidden';
import SearchApp from '../components/SearchApp';
import MediaCard from '../components/MediaCard';
import NewCategoriesBar from '../components/NewCategoriesBar';
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
          <NewCategoriesBar etiquetes={etiquetes} />
          <Grid container>
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
