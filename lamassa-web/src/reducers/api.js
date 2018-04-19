import { createFilter } from 'react-search-input';
import * as api from '../actions/apiActions';

const initialState = {
  message: [],
  filteredMessages: [],
  reviewedProduct: {},
  productors: [],
  etiquetes: [],
};

const KEYS_TO_FILTERS = ['nom', 'text'];

export default (state = initialState, action) => {
  switch (action.type) {
    case api.FETCH_SUCCESS: {
      const { productes, productors, etiquetes } = action.payload;
      // const newProductes = mergeFormatsProductes(productes, formats);
      return {
        message: productes,
        filteredMessages: productes,
        productors,
        etiquetes,
      };
    }
    case api.SEARCH_UPDATED:
      return {
        ...state,
        filteredMessages: state.message.filter(createFilter(action.payload, KEYS_TO_FILTERS)),
      };
    case api.CATEGORY_UPDATED: {
      let msgs = state.message;
      let oldArray = [];
      if (action.payload.join()) {
        action.payload.map(value => {
          const newArray = state.message.filter(createFilter(`${value.pk}`, ['etiqueta']));
          msgs = oldArray.concat(newArray);
          oldArray = msgs;
          return null;
        });
      }
      return {
        ...state,
        filteredMessages: msgs,
      };
    }
    case api.FETCH_PRODUCT_REQUEST: {
      return {
        ...state,
        reviewedProductPk: action.payload,
      };
    }
    case api.FETCH_PRODUCT_SUCCESS: {
      const { productes, productors, etiquetes } = action.payload;
      const filteredProduct = productes.filter(createFilter(state.reviewedProductPk, ['pk']));
      // const reviewedProduct = mergeFormatsProduct(filteredProduct[0], formats);
      const filteredProductsProducer = productes.filter(
        createFilter(`${filteredProduct[0].productora.nom}`, ['productora.nom'])
      );
      // const productsProducer = mergeFormatsProductes(filteredProductsProducer, formats);
      return {
        ...state,
        reviewedProduct: filteredProduct[0],
        productsProducer: filteredProductsProducer,
        message: action.payload ? action.payload.productes : [],
        filteredMessages: action.payload ? action.payload.productes : [],
        productors,
        etiquetes,
      };
    }
    default:
      return state;
  }
};
//
// export const mergeFormatsProductes = (productes, formats) => {
//   const newProductes = [];
//   productes.map((value, index) => {
//     const newFormats = [];
//     value.formats.map(val => {
//       formats.find(obj => {
//         if (obj.pk === val) {
//           newFormats.push(obj);
//         }
//         return null;
//       });
//       return null;
//     });
//     newProductes[index] = { ...productes[index], formats: newFormats };
//     return null;
//   });
//   return newProductes;
// };
//
// export const mergeFormatsProduct = (producte, formats) => {
//   const newFormats = [];
//   producte.formats.map(val => {
//     formats.find(obj => {
//       if (obj.pk === val) {
//         newFormats.push(obj);
//       }
//       return null;
//     });
//     return null;
//   });
//   return { ...producte, formats: newFormats };
// };
