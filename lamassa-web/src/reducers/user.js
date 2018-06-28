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
  newCart: {},
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
        ts: new Date().getTime(),
      };
    case user.ADD_CART_SUCCESS:
      return {
        ...state,
        ts: new Date().getTime(),
        cart: action.payload.comandes,
        newCart: action.payload.new_com,
      };
    case user.REMOVE_CART:
      return {
        ...state,
        ts: new Date().getTime(),
      };
    case user.REMOVE_CART_SUCCESS:
      return {
        ...state,
        ts: new Date().getTime(),
        cart: action.payload.comandes,
      };
    case user.REMOVE_CART_FAILED:
      return {
        ...state,
        ts: new Date().getTime(),
        cart: action.payload.comandes,
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
      const { user_profile, nodes, historial, comandes, new_com } = action.payload;
      // const newProductes = mergeFormatsProductes(productes, formats);
      return {
        ...state,
        user: user_profile,
        nodes,
        historial,
        cart: comandes,
        newCart: new_com,
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
