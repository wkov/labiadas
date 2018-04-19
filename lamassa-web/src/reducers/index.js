import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';
import auth, * as fromAuth from './auth.js';
import api from './api.js';
import user from './user.js';

export default combineReducers({
  router: routerReducer,
  api: api,
  user: user,
  auth: auth,
});

export const isAuthenticated = state => fromAuth.isAuthenticated(state.auth);
export const accessToken = state => fromAuth.accessToken(state.auth);
export const isAccessTokenExpired = state => fromAuth.isAccessTokenExpired(state.auth);
export const refreshToken = state => fromAuth.refreshToken(state.auth);
export const isRefreshTokenExpired = state => fromAuth.isRefreshTokenExpired(state.auth);
export const authErrors = state => fromAuth.errors(state.auth);

export function withAuth(headers = {}) {
  return state => ({
    ...headers,
    Authorization: `Bearer ${accessToken(state)}`,
  });
}
