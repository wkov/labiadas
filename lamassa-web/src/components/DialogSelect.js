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
    this.props.onClose(value);
  };

  render() {
    const { onClose, selectedValue, horaris, ...other } = this.props;
    return (
      <Dialog onClose={this.handleClose} aria-labelledby="simple-dialog-title" {...other}>
        <DialogTitle id="simple-dialog-title">Tria una franja horaria:</DialogTitle>
        <div>
          <List>
            {horaris.map(horari => (
              <ListItem button onClick={() => this.handleListItemClick(horari)} key={horari}>
                <ListItemText primary={horari} />
              </ListItem>
            ))}
          </List>
        </div>
      </Dialog>
    );
  }
}

export default DialogSelect;
