import * as user from '../actions/userActions';
import * as auth from '../actions/authActions';
import * as api from '../actions/apiActions';

const initialState = {
  favorites: [],
  ts: 0,
  open: false,
  cart: [],
  nodes: [],
  historial: [],
};

export default (state = initialState, action) => {
  console.log(action);
  switch (action.type) {
    case user.ADD_FAVORITES:
      return {
        ...state,
        user: {
          ...state.user,
          preferits: action.payload,
        },
        ts: new Date().getTime(),
      };
    case user.ADD_CART:
      return {
        ...state,
        cart: action.payload,
        ts: new Date().getTime(),
      };
    case user.REMOVE_CART:
      return {
        ...state,
        cart: action.payload,
        ts: new Date().getTime(),
      };
    case user.HANDLE_DRAWER:
      return {
        ...state,
        open: action.payload,
      };
    case auth.LOGIN_SUCCESS:
      return {
        ...state,
        user: action.payload.user,
      };
    case api.FETCH_SUCCESS: {
      const { user_profile, nodes, historial } = action.payload;
      // const newProductes = mergeFormatsProductes(productes, formats);
      return {
        ...state,
        user: user_profile,
        nodes,
        historial,
      };
    }
    case user.POST_SUCCESS:
      return {
        ...state,
        user: action.payload.user_profile,
      };
    default:
      return state;
  }
};
