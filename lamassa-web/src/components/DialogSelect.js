import React from 'react';
import Button from 'material-ui/Button';
import Avatar from 'material-ui/Avatar';
import List, { ListItem, ListItemText } from 'material-ui/List';
import Dialog, { DialogTitle } from 'material-ui/Dialog';

const emails = ['username@gmail.com', 'user02@gmail.com'];

class DialogSelect extends React.Component {
  handleClose = () => {
    this.props.onClose(this.props.selectedValue);
  };

  handleListItemClick = value => {
    const { horaris } = this.props;
    this.props.clickItem({ ...horaris, franjes: value });
  };

  render() {
    const { onClose, selectedValue, horaris, open } = this.props;
    return (
      <Dialog open={open} onClose={this.handleClose}>
        <DialogTitle id="simple-dialog-title">Tria una franja horaria:</DialogTitle>
        <div>
          <List>
            {horaris.franjes
              ? horaris.franjes.map(franjes => (
                  <ListItem button onClick={() => this.handleListItemClick(franjes)} key={franjes}>
                    <ListItemText primary={`${franjes.inici} - ${franjes.final}`} />
                  </ListItem>
                ))
              : null}
          </List>
        </div>
      </Dialog>
    );
  }
}

export default DialogSelect;
