import { RSAA } from 'redux-api-middleware';
import { withAuth } from '../reducers';

export const POST_REQUEST = '@@user/POST_REQUEST';
export const POST_SUCCESS = '@@user/POST_SUCCESS';
export const POST_FAILURE = '@@user/POST_FAILURE';

export const ADD_FAVORITES = '@@user/ADD_FAVORITES';
export const HANDLE_DRAWER = '@@user/HANDLE_DRAWER';
export const ADD_CART = '@@user/ADD_CART';
export const ADD_CART_SUCCESS = '@@user/ADD_CART_SUCCESS';
export const REMOVE_CART = '@@user/REMOVE_CART';

export const addFavorites = ({ favorites, itemPk }) => {
  const csrf = getCookie('csrftoken');
  return dispatch => {
    fetch('http://localhost:8000/api/auth/example', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        preferits: itemPk,
      }),
    })
      .then(response => {
        dispatch({
          type: ADD_FAVORITES,
          payload: favorites,
        });
        return response.json();
      })
      .then(function(data) {
        console.log('Data is ok', data);
        dispatch({
          type: POST_SUCCESS,
          payload: data,
        });
      })
      .catch(function(ex) {
        console.log('parsing failed', ex);
      });
  };
};

export const postChanges = ({ prop, value }) => {
  return {
    [RSAA]: {
      endpoint: 'http://localhost:8000/api/auth/example',
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        [prop]: value,
      }),
      types: [POST_REQUEST, POST_SUCCESS, POST_FAILURE],
    },
  };
};

export const addToCart = (item, comanda, cart) => {
  const csrf = getCookie('csrftoken');
  return dispatch => {
    fetch('http://localhost:8000/api/auth/example', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        comanda: item,
      }),
    })
      .then(response => {
        dispatch({
          type: ADD_CART,
          payload: favorites,
        });
        return response.json();
      })
      .then(function(data) {
        console.log('Data is ok', data);
        dispatch({
          type: ADD_CART_SUCCESS,
          payload: data,
        });
      })
      .catch(function(ex) {
        console.log('parsing failed', ex);
      });
  };
};

export const removeFromCart = (cart, itemPk) => {
  let pos = false;
  const exist = cart.map((value, index) => {
    if (value.item.pk === itemPk) {
      pos = index;
      return true;
    }
    return false;
  });
  if (exist) {
    cart.splice(pos, 1);
  }
  return {
    type: REMOVE_CART,
    payload: cart,
  };
};

export const handleDrawer = ({ open }) => ({
  type: HANDLE_DRAWER,
  payload: open,
});

export const getCookie = name => {
  if (!document.cookie) {
    return null;
  }
  const token = document.cookie
    .split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (token.length === 0) {
    return null;
  }
  return decodeURIComponent(token[0].split('=')[1]);
};
