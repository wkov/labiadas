import { RSAA } from 'redux-api-middleware';
import { withAuth } from '../reducers';

export const POST_REQUEST = '@@user/POST_REQUEST';
export const POST_SUCCESS = '@@user/POST_SUCCESS';
export const POST_FAILURE = '@@user/POST_FAILURE';

export const ADD_FAVORITES = '@@user/ADD_FAVORITES';
export const HANDLE_DRAWER = '@@user/HANDLE_DRAWER';
export const ADD_CART = '@@user/ADD_CART';
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
//
// export const addFavorites = ({ favorites, itemPk }) => {
//   if (favorites.includes(itemPk)) {
//     const index = favorites.indexOf(itemPk);
//     favorites.splice(index, 1);
//   } else {
//     favorites.push(itemPk);
//   }
//   return {
//     [RSAA]: {
//       endpoint: 'http://aamping.pythonanywhere.com/api/auth/example',
//       method: 'POST',
//       headers: withAuth({ 'Content-Type': 'application/json' }),
//       body: JSON.stringify({
//         preferits: itemPk,
//       }),
//       types: [
//         {
//           type: ADD_FAVORITES,
//           payload: favorites,
//         },
//         POST_SUCCESS,
//         POST_FAILURE,
//       ],
//     },
//   };
//   // return {
//   //   type: ADD_FAVORITES,
//   //   payload: favorites,
//   // };
// };

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
  const { pk } = item;
  const exist = cart.map(value => {
    if (value.item.pk === pk) {
      return true;
    }
    return false;
  });
  if (exist) {
    cart.push({ item, comanda });
  } else {
    cart.push({ item, comanda });
  }
  return {
    type: ADD_CART,
    payload: cart,
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
