import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { ListItem, ListItemIcon } from 'material-ui/List';
import MailIcon from 'material-ui-icons/Mail';
import ShoppingCartIcon from 'material-ui-icons/ShoppingCart';
import FavoriteIcon from 'material-ui-icons/Favorite';
import HelpIcon from 'material-ui-icons/Help';
import HomeIcon from 'material-ui-icons/Home';
import Badge from 'material-ui/Badge';
import Divider from 'material-ui/Divider';
import ShareIcon from 'material-ui-icons/Share';
import { snackMessage } from '../../actions/userActions';

const DrawerIcons = props => {
  return (
    <div>
      <Divider />
      <Link className="drawer-list" to="/">
        <ListItem button>
          <ListItemIcon>
            <HomeIcon className="drawer-icon" />
          </ListItemIcon>
          <div className="drawer-text">Botiga</div>
        </ListItem>
      </Link>
      <Link className="drawer-list" to="/preferits">
        <ListItem button>
          <ListItemIcon>
            <Badge badgeContent={props.favorites ? props.favorites.length : 0} className="drawer-badge">
              <FavoriteIcon className="drawer-icon" />
            </Badge>
          </ListItemIcon>
          <div className="drawer-text">Preferits</div>
        </ListItem>
      </Link>
      <Link className="drawer-list" to="/cart">
        <ListItem button>
          <ListItemIcon>
            <Badge badgeContent={props.cart ? props.cart.length : 0} className="drawer-badge">
              <ShoppingCartIcon className="drawer-icon" />
            </Badge>
          </ListItemIcon>
          <div className="drawer-text">Cistella</div>
        </ListItem>
      </Link>
      <Divider />
      <ListItem className="drawer-list" button>
        <ListItemIcon>
          <MailIcon className="drawer-icon" onClick={() => props.snackMessage()} />
        </ListItemIcon>
        <div className="drawer-text">Missatges</div>
      </ListItem>
      <ListItem className="drawer-list" button>
        <ListItemIcon>
          <HelpIcon className="drawer-icon" />
        </ListItemIcon>
        <div className="drawer-text">Ajuda</div>
      </ListItem>
      <ListItem className="drawer-list" button>
        <ListItemIcon aria-label="Convidar">
          <ShareIcon style={{ color: '#ebf9d6' }} />
        </ListItemIcon>
        <div className="drawer-text">Convida</div>
      </ListItem>
    </div>
  );
};

const mapStateToProps = ({ user }) => {
  return {
    cart: user.cart,
    favorites: user.user ? user.user.preferits : null,
    ts: user.ts,
  };
};

export default connect(mapStateToProps, { snackMessage })(DrawerIcons);
