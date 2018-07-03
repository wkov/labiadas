import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import ResponsiveTable from 'material-ui-next-responsive-table/lib/ResponsiveTable';
import DeleteIcon from '@material-ui/icons/Delete';
import DialogConfirm from './DialogConfirm';

const columns = [
  {
    key: 'producte',
    label: 'Producte',
    primary: true,
  },
  {
    key: 'preu_unitat',
    label: 'Preu Unitat',
  },
  {
    key: 'quantitat',
    label: 'Quantitat',
  },
  {
    key: 'preu',
    label: 'Preu',
  },
  {
    key: 'delete',
    label: '',
  },
];

class CartTable extends Component {
  state = {
    open: false,
  };
  handleDelete = () => {
    this.props.removeFromCart(this.state.selectedItem);
    this.handleCloseConfirm();
  };

  render() {
    const newCart = _.map(this.props.cart, (obj, key) => ({
      pk: key,
      comandes: _.map(obj, (obj2, key2) => ({
        pk: key2,
        dia_entrega: obj2.dia_entrega.date,
        producte: 'obj2.comanda.format',
        preu_unitat: obj2.comanda.preu,
        quantitat: obj2.comanda.cantitat,
        preu: obj2.comanda.preu,
        delete: this.props.edit ? <DeleteIcon onClick={() => this.handleClickOpenConfirm(key2)} /> : null,
      })),
    }));
    if (!newCart[0]) return <div> Cargando...</div>;
    return (
      <div>
        {newCart.map((cistella, key) => (
          <Card style={{ margin: 20 }} key={key}>
            <CardHeader
              title={`Cistella: ${cistella.comandes[0].dia_entrega}`}
              subheader={`Preu Total: ${cistella.comandes.preu_unitat} `}
            />
            <CardContent>
              <ResponsiveTable columns={columns} data={cistella.comandes} />
            </CardContent>
          </Card>
        ))}
        <DialogConfirm open={this.state.open} handleConfirm={this.handleDelete} handleClose={this.handleCloseConfirm} />
      </div>
    );
  }

  handleClickOpenConfirm = itemPk => {
    this.setState({
      open: true,
      selectedItem: itemPk,
    });
  };
  handleCloseConfirm = () => {
    this.setState({ open: false });
  };
}

export default CartTable;
