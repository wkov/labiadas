import React, { Component } from 'react';
import SearchInput from 'react-search-input';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import { connect } from 'react-redux';
import Hidden from '@material-ui/core/Hidden';

import { searchUpdated, categoryUpdated } from '../actions/apiActions';

const url = 'http://localhost:8000';

const styles = {
  searchBar: {
    display: 'flex',
    paddingLeft: 20,
  },
  search: {
    flex: 1,
  },
};

class SearchApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchTerm: '',
      categoryTerm: {
        nom: '',
        img: '',
      },
      anchorEl: null,
    };
    this.searchUpdated = this.searchUpdated.bind(this);
  }

  handleClick = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  handleClose = () => {
    this.setState({ anchorEl: null });
  };

  handleMenuItemClick = (event, value) => {
    this.setState({ anchorEl: null });
    this.props.categoryUpdated({ term: [value] });
  };

  renderButtonCategory(category) {
    if (category.name) {
      return (
        <div>
          <ListItemIcon>
            <img alt="" src={category.img} />
          </ListItemIcon>
          {category.name}
        </div>
      );
    } else {
      return 'Categories';
    }
  }

  renderMenuCategory(anchorEl) {
    const { etiquetes } = this.props;
    return (
      <div>
        <Hidden lgUp>
          <Button aria-owns={anchorEl ? 'simple-menu' : null} aria-haspopup="true" onClick={this.handleClick}>
            {this.renderButtonCategory(this.state.categoryTerm)}
          </Button>
        </Hidden>
        <Menu id="simple-menu" anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={this.handleClose}>
          <MenuItem onClick={event => this.handleMenuItemClick(event, [])}>
            <ListItemText primary={'Totes Categories'} />
          </MenuItem>
          {etiquetes.map(value => (
            <div key={value.nom}>
              <MenuItem onClick={event => this.handleMenuItemClick(event, value)}>
                <ListItemIcon>
                  <img alt="" src={url + value.img} />
                </ListItemIcon>
                <ListItemText inset primary={value.nom} />
              </MenuItem>
            </div>
          ))}
        </Menu>
      </div>
    );
  }

  searchUpdated(term) {
    this.props.searchUpdated({ term });
  }

  render() {
    // const categoryData = message.filter(createFilter(this.state.categoryTerm.name, ['etiqueta.nom']));
    // const filteredList = categoryData.filter(createFilter(this.state.searchTerm, KEYS_TO_FILTERS));

    return (
      <div style={styles.searchBar}>
        {this.renderMenuCategory(this.state.anchorEl)}
        <div style={styles.search}>
          <SearchInput className="search-input" placeholder="Cerca" onChange={this.searchUpdated} />
        </div>
      </div>
    );
  }
}

const mapStateToProps = ({ api }) => {
  const { filteredMessages, etiquetes } = api;
  return { filteredMessages, etiquetes };
};

export default connect(mapStateToProps, { searchUpdated, categoryUpdated })(SearchApp);
