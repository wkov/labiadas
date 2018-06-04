import storage from 'redux-persist/es/storage';
import { applyMiddleware, createStore, compose } from 'redux';
import { createFilter } from 'redux-persist-transform-filter';
import { persistReducer, persistStore } from 'redux-persist';
import { routerMiddleware } from 'react-router-redux';
import thunk from 'redux-thunk';
import rootReducer from './reducers';

export default history => {
  const persistedFilter = createFilter('auth', ['access', 'refresh']);
  const persistedUser = createFilter('user', ['cart', 'favorites', 'user', 'historial']);

  const reducer = persistReducer(
    {
      key: 'polls',
      storage,
      whitelist: ['auth', 'user'],
      transforms: [persistedFilter, persistedUser],
    },
    rootReducer
  );

  const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

  const store = createStore(reducer, applyMiddleware(thunk));

  persistStore(store);

  return store;
};
