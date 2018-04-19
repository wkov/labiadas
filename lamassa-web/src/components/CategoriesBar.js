import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import compose from 'recompose/compose';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemSecondaryAction } from 'material-ui/List';
import Checkbox from 'material-ui/Checkbox';
import Avatar from 'material-ui/Avatar';
import { categoryUpdated } from '../actions/apiActions';

const url = 'http://localhost:8000';

const styles = theme => ({
  titleList: {
    fontFamily: 'Satisfy',
    textAlign: 'center',
    fontSize: 26,
  },
  textList: {
    fontSize: 16,
  },
  root: {
    width: '100%',
    minWidth: 200,
    // backgroundColor: theme.palette.background.paper,
  },
});

class CategoriesBar extends React.Component {
  state = {
    checked: [],
  };

  handleToggle = value => () => {
    const { checked } = this.state;
    const currentIndex = checked.indexOf(value);
    let newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }
    if (value === 0) newChecked = [];
    this.props.categoryUpdated({ term: newChecked });
    this.setState({
      checked: newChecked,
    });
  };

  render() {
    const { etiquetes } = this.props;
    return (
      <div className="categories-bar">
        <div className="cards-title" style={{ textAlign: 'center' }}>
          Categories
        </div>
        <List>
          <ListItem dense button>
            <div style={{ marginLeft: 10 }} className="cards-text">
              {'Totes les categories'}{' '}
            </div>
            <ListItemSecondaryAction>
              <Checkbox onChange={this.handleToggle(0)} checked={!this.state.checked.join()} />
            </ListItemSecondaryAction>
          </ListItem>
          {etiquetes.map(value => (
            <ListItem key={value.nom} dense button>
              <Avatar alt={value.nom} src={url + value.img} />
              <div style={{ marginLeft: 10 }} className="cards-text">
                {value.nom}{' '}
              </div>
              <ListItemSecondaryAction>
                <Checkbox onChange={this.handleToggle(value)} checked={this.state.checked.indexOf(value) !== -1} />
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </div>
    );
  }
}

CategoriesBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default compose(
  withStyles(styles, {
    name: 'CategoriesBar',
  }),
  connect(null, { categoryUpdated })
)(CategoriesBar);
