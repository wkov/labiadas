import React, { Component } from 'react';
import { connect } from 'react-redux';
import Card, { CardContent, CardMedia, CardHeader } from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import Table, { TableBody, TableCell, TableRow, TableHead } from 'material-ui/Table';
import Grid from 'material-ui/Grid';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogTitle, // eslint-disable-next-line
} from 'material-ui/Dialog';
import Button from 'material-ui/Button';

import { postChanges } from '../actions/userActions';
import { fetchList } from '../actions/apiActions';
import { MyMapComponent } from '../components/MyMapComponent';

class UserProfileScreen extends Component {
  state = {
    product: '',
    open: false,
    detall: '',
    openDialogNodes: false,
    newNode: '',
    prop: '',
  };

  componentWillMount() {
    this.props.fetchList();
  }

  onClickEditar(e, value, prop) {
    this.setState({ open: true, detall: e.nativeEvent.target.id, value, prop });
  }

  render() {
    const {
      avatar,
      bio,
      carrer,
      invitacions,
      lloc_entrega,
      numero,
      phone_number,
      pis,
      poblacio,
      user,
      historial,
      direccio,
    } = this.props;
    const direccioEntrega = `${lloc_entrega.carrer} ${lloc_entrega.numero} ${lloc_entrega.pis}`;
    const poblacioEntrega = `${lloc_entrega.poblacio} ${lloc_entrega.codi_postal}`;
    const splitString = lloc_entrega.position.split(',');
    const coordinades = { lat: parseInt(splitString[0], 10), lng: parseInt(splitString[1], 10) };
    return (
      <Grid container spacing={40}>
        <Grid item>
          <Card className="userprofile-card">
            <CardHeader title={"Dades de l'usuari/a"} />
            <div className="userprofile-avatar-container">
              <Avatar className="userprofile-avatar" alt="Usuari/a" src={avatar ? avatar : '/item_espelta.jpg'} />
            </div>
            <CardContent>
              <Table>
                <TableBody>
                  <TableRow>
                    <TableCell className="userprofile-text">Nom:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={user.first_name} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Nom" onClick={e => this.onClickEditar(e, user.first_name, 'first_name')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Cognoms:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={user.last_name} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Cognoms" onClick={e => this.onClickEditar(e, user.last_name, 'last_name')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">{"Nom d'usuari/a:"}</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={user.username} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Nom usuari/a" onClick={e => this.onClickEditar(e, user.username, 'username')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Email:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={user.email} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Correu electronic" onClick={e => this.onClickEditar(e, user.email, 'email')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Telèfon:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={phone_number} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Telèfon" onClick={e => this.onClickEditar(e, phone_number, 'phone_number')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Direcció:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={direccio} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Direcció" onClick={e => this.onClickEditar(e, direccio, 'direccio')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Població:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={poblacio} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Població" onClick={e => this.onClickEditar(e, poblacio, 'poblacio')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Bio:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={bio} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Descripció" onClick={e => this.onClickEditar(e, bio, 'bio')}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Invitacions:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={invitacions} />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Data de registre:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={user.date_joined} />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Última conexió:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={user.last_login} />
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card className="userprofile-card">
            <CardHeader title="Punt de trobada" />
            {
              // <CardMedia
              //   component={() => <MyMapComponent isMarkerShown coordinades={coordinades} />}
              //   src="/item_espelta.jpg"
              // />
            }
            <CardContent>
              <Table>
                <TableBody>
                  <TableRow>
                    <TableCell className="userprofile-text">{"Lloc d'entrega:"}</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={lloc_entrega.nom} />
                    </TableCell>
                    <TableCell className="userprofile-editar">
                      <a id="Lloc d'entrega" onClick={() => this.setState({ openDialogNodes: true })}>
                        Editar
                      </a>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">{"Dia i hora d'entrega:"}</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value="Divendres a les 19h" />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Direcció:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={direccioEntrega} />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Població:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={poblacioEntrega} />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Coordinades al mapa:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <input className="userprofile-input" readOnly value={lloc_entrega.position} />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="userprofile-text">Descripció:</TableCell>
                    <TableCell className="userprofile-inputcell">
                      <div className="userprofile-text">{lloc_entrega.text}</div>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card className="userprofile-card">
            <CardHeader title="Historial comandes" />
            <CardContent>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell className="userprofile-text">Producte</TableCell>
                    <TableCell className="userprofile-text">Format</TableCell>
                    <TableCell className="userprofile-text">Preu</TableCell>
                    <TableCell className="userprofile-text">Quantitat</TableCell>
                    <TableCell className="userprofile-text">Preu Total</TableCell>
                    <TableCell className="userprofile-text">Freqüencia</TableCell>
                    <TableCell className="userprofile-text">Data</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {historial ? (
                    historial.map(value => (
                      <TableRow key={value.format.nom}>
                        <TableCell className="userprofile-text">{value.producte}</TableCell>
                        <TableCell className="userprofile-text">{value.format.nom}</TableCell>
                        <TableCell className="userprofile-text">{value.format.preu}</TableCell>
                        <TableCell className="userprofile-text">{value.cantitat}</TableCell>
                        <TableCell className="userprofile-text">{value.preu}</TableCell>
                        <TableCell className="userprofile-text">{value.frequencia.nom}</TableCell>
                        <TableCell className="userprofile-text">{value.data_comanda.split('T')[0]}</TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell className="userprofile-text">Carregant dades...</TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </Grid>
        {this.renderDialog()}
        {this.renderDialogNodes()}
      </Grid>
    );
  }

  renderDialog() {
    const { open } = this.state;
    return (
      <Dialog open={open ? open : false} onClose={this.handleCloseDialog}>
        <DialogTitle>{'Canvia: '}</DialogTitle>
        <DialogContent>
          <Table>
            <TableBody>
              <TableRow>
                <TableCell className="userprofile-text">{this.state.detall} actual</TableCell>
                <TableCell>
                  <input className="userprofile-input" readOnly value={this.state.value} />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="userprofile-text">Nou {this.state.detall}</TableCell>
                <TableCell>
                  <input
                    className="userprofile-input"
                    onChange={e => this.setState({ newValue: e.nativeEvent.target.value })}
                  />
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button raised onClick={this.onGuardaCanvis.bind(this)} color="default">
            Guarda
          </Button>
          <Button onClick={this.handleCloseDialog} color="primary">
            Cancel·la
          </Button>
        </DialogActions>
      </Dialog>
    );
  }

  renderDialogNodes() {
    const { openDialogNodes } = this.state;
    const { nodes, lloc_entrega } = this.props;
    let newNode = nodes ? nodes.find(obj => obj.nom === this.state.newNode) : '';
    if (!newNode) {
      newNode = this.props.lloc_entrega;
    }
    const direccioEntrega = `${newNode.carrer} ${newNode.numero} ${newNode.pis}`;
    const poblacioEntrega = `${newNode.poblacio} ${newNode.codi_postal}`;
    return (
      <Dialog open={openDialogNodes ? openDialogNodes : false} onClose={this.handleCloseDialogNodes}>
        <DialogTitle>{'Canvia: '}</DialogTitle>
        <DialogContent>
          <Table>
            <TableBody>
              <TableRow>
                <TableCell className="userprofile-text">{"Lloc d'entrega actual:"}</TableCell>
                <TableCell className="userprofile-inputcell">
                  <input className="userprofile-input" readOnly value={lloc_entrega.nom} />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="userprofile-text">{"Nou Lloc d'entrega:"}</TableCell>
                <TableCell className="userprofile-inputcell">
                  <select
                    className="userprofile-input"
                    defaultValue={newNode.nom}
                    onChange={value => this.setState({ newNode: value.nativeEvent.target.value })}
                  >
                    {nodes ? (
                      nodes.map(value => (
                        <option key={value.nom} value={value.nom}>
                          {value.nom}
                        </option>
                      ))
                    ) : (
                      <option key={''} value={'value'}>
                        ''
                      </option>
                    )}
                  </select>
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="userprofile-text">{"Dia i hora d'entrega:"}</TableCell>
                <TableCell className="userprofile-inputcell">
                  <input className="userprofile-input" readOnly value="Divendres a les 19h" />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="userprofile-text">Direcció:</TableCell>
                <TableCell className="userprofile-inputcell">
                  <input className="userprofile-input" readOnly value={direccioEntrega} />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="userprofile-text">Població:</TableCell>
                <TableCell className="userprofile-inputcell">
                  <input className="userprofile-input" readOnly value={poblacioEntrega} />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="userprofile-text">Coordinades al mapa:</TableCell>
                <TableCell className="userprofile-inputcell">
                  <input className="userprofile-input" readOnly value={newNode.position} />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="userprofile-text">Descripció:</TableCell>
                <TableCell className="userprofile-inputcell">
                  <div className="userprofile-text">{newNode.text}</div>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button raised onClick={this.onGuardaCanvisNodes.bind(this)} color="default">
            Guarda
          </Button>
          <Button onClick={this.handleCloseDialogNodes} color="primary">
            Cancel·la
          </Button>
        </DialogActions>
      </Dialog>
    );
  }
  handleCloseDialog = () => {
    this.setState({ open: false });
  };

  handleCloseDialogNodes = () => {
    this.setState({ openDialogNodes: false });
  };

  onGuardaCanvisNodes() {
    const { nodes } = this.props;
    let newNode = nodes ? nodes.find(obj => obj.nom === this.state.newNode) : '';
    if (!newNode) {
      newNode = this.props.lloc_entrega;
    }
    this.props.postChanges({ prop: 'lloc_entrega', value: newNode });
    this.setState({ openDialogNodes: false });
  }

  onGuardaCanvis() {
    this.props.postChanges({ prop: this.state.prop, value: this.state.newValue });
    this.setState({ open: false });
  }
}

const mapStateToProps = ({ user }) => {
  return { ...user.user, nodes: user.nodes, historial: user.historial };
};

export default connect(mapStateToProps, { postChanges, fetchList })(UserProfileScreen);
