import React from 'react';
import PropTypes from 'prop-types';
import _ from 'lodash';
import Calendar from 'react-calendar';
import Button from 'material-ui/Button';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  withMobileDialog,
} from 'material-ui/Dialog';
import Grid from 'material-ui/Grid';
import DialogSelect from './DialogSelect';

const months = [
  'Gener',
  'Febrer',
  'Març',
  'Abril',
  'Maig',
  'Juny',
  'Juliol',
  'Agost',
  'Setembre',
  'Octubre',
  'Novembre',
  'Desembre',
];
const BLUE = 'blue';
const RED = 'red';
const weekDays = [1, 2, 3, 4, 5, 6, 7];
const frequency = ['Cada Setmana', 'Cada 2 Setmanes', 'Cada 4 Setmanes'];

const dayMiliseconds = 86400000;
const today = new Date();
const endTime = new Date(2018, 8, 1);

const initialState = [
  {
    mes: 'Gener',
    diesHabils: [3, 10, 31],
    diesFestius: [17],
  },
  {
    mes: 'Febrer',
    diesHabils: [7, 21],
    diesFestius: [14],
  },
  {
    mes: 'Març',
    diesHabils: [7, 21, 28],
    diesFestius: [14],
  },
];

class DialogCalendar extends React.Component {
  state = {
    open: false,
    openDialogSelect: false,
    calendarData: initialState,
    color: BLUE,
    enabledDay: today.getDay(),
    diesHabils: [],
    diesFestius: [],
    diesSelected: [],
    frequencia: '',
    franjes: [],
    selDia: {},
    hora: {},
  };

  componentWillMount() {
    const { dies } = this.props;
    const lastDia = new Date(dies[Object.keys(dies).reduce((a, b) => (dies[a] > dies[b] ? a : b))].dia);
    const calendar = [];
    for (let i = today.getMonth(); i <= lastDia.getMonth(); i++) {
      if (!calendar.includes(i)) {
        calendar.push(i);
      }
      if (i === 11) {
        i = -1;
      }
    }
    const diesHabils = _.map(dies, (obj, key) => ({
      pk: key,
      dia: obj.dia,
      franjes: _.map(obj.franjes, (data, key) => ({ pk: key, ...data })),
    }));
    this.setState({ calendar, diesHabils });
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.frequencia !== nextProps.frequencia) {
      this.setState({ frequencia: nextProps.frequencia });
    }
    if (this.props.entrega !== nextProps.entrega) {
      this.setState({ hora: nextProps.entrega.franjes });
      this.onChangeDates(nextProps.entrega.franjes);
    }
  }

  onChangeDates = (franjes = this.props.entrega.franjes) => {
    const { frequencia } = this.state;
    const diesSelected = [];
    const semanesDisponibles = [];
    const { dies } = this.props;
    const { diesHabils } = this.state;
    _.map(dies, obj => semanesDisponibles.push(new Date(obj.dia).getWeek()));
    switch (frequencia) {
      case 'Cada Setmana': {
        for (
          let i = new Date(diesHabils[0].dia).getWeek();
          i <= new Date(diesHabils[diesHabils.length - 1].dia).getWeek();
          i++
        ) {
          if (semanesDisponibles.includes(i)) {
            diesSelected.push({ ...diesHabils[semanesDisponibles.indexOf(i)], franjes });
          }
        }
        break;
      }
      case 'Cada 2 Setmanes': {
        for (
          let i = new Date(diesHabils[0].dia).getWeek();
          i <= new Date(diesHabils[diesHabils.length - 1].dia).getWeek();
          i = i + 2
        ) {
          if (semanesDisponibles.includes(i)) {
            diesSelected.push({ ...diesHabils[semanesDisponibles.indexOf(i)], franjes });
          }
        }
        break;
      }
      case 'Cada 4 Setmanes': {
        for (
          let i = new Date(diesHabils[0].dia).getWeek();
          i <= new Date(diesHabils[diesHabils.length - 1].dia).getWeek();
          i = i + 4
        ) {
          if (semanesDisponibles.includes(i)) {
            diesSelected.push({ ...diesHabils[semanesDisponibles.indexOf(i)], franjes });
          }
        }
        break;
      }
      default:
        break;
    }
    console.log(diesSelected);
    this.setState({ diesSelected, frequencia });
  };

  onPressTile = (value, e) => {
    const data = new Date(value);
    const { diesSelected, diesFestius, color, diesHabils } = this.state;
    const item = diesSelected.find(obj => new Date(obj.dia).toDateString() === data.toDateString());
    switch (color) {
      case BLUE: {
        if (item) {
          diesSelected.splice(diesSelected.indexOf(item), 1);
        } else {
          const dia = diesHabils.find(obj => new Date(obj.dia).toDateString() === data.toDateString());
          this.handleDialogSelect(dia);
          if (diesFestius.includes(data.toDateString())) {
            diesFestius.splice(diesFestius.indexOf(data.toDateString()), 1);
          }
        }
        break;
      }
      case RED: {
        if (diesFestius.includes(data.toDateString())) {
          diesFestius.splice(diesFestius.indexOf(data.toDateString()), 1);
        } else {
          diesFestius.push(data.toDateString());
          diesFestius.sort((a, b) => a - b);
          if (item) {
            diesSelected.splice(diesSelected.indexOf(item), 1);
          }
        }
        break;
      }
      default:
        break;
    }
    this.setState({ diesSelected, diesFestius });
  };

  renderTileClassName(date, view, month) {
    const { diesSelected, diesFestius } = this.state;
    if (date.getMonth() === month && diesFestius.includes(`${date.toDateString()}`)) {
      return 'calendar-tile-holiday';
    } else if (
      date.getMonth() === month &&
      diesSelected.find(obj => new Date(obj.dia).toDateString() === date.toDateString())
    ) {
      return 'calendar-tile-active';
    }
    return null;
  }

  renderTileDisabled({ date }) {
    const diesDisponibles = [];
    const { dies } = this.props;
    _.map(dies, obj => diesDisponibles.push(new Date(obj.dia).toDateString()));
    if (diesDisponibles.includes(date.toDateString())) return false;
    return true;
  }

  handleConfirm = () => {
    const { dies } = this.props;
    const { diesSelected } = this.state;
    const diesEntrega = diesSelected.map(dia => ({
      dia_entrega: dia.pk,
      franja_horaria: dia.franjes.pk,
    }));
    this.props.handleConfirm(diesEntrega);
  };

  render() {
    const { open, handleClose, fullScreen, frequencia, dies } = this.props;
    const { calendar, enabledDay } = this.state;
    return (
      <div>
        <Dialog
          maxWidth={false}
          classes={{ paper: 'dialog-calendar-paper' }}
          fullScreen={fullScreen}
          open={open}
          onClose={handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle>{"Selecciona els dies en què vols l'entrega"}</DialogTitle>
          <div onClick={() => this.setState({ openDialogSelect: true })}> Prova </div>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {"Blau - Dies en què es farà l'entrega del producte"}
            </DialogContentText>
            <DialogContentText id="alert-dialog-description">
              {"Vermell - No hi ha disponibilitat per part del productor/a o el lloc d'entrega"}
            </DialogContentText>
            <div className="calendar-controlpanel">
              <div className="calendar-control">
                <div> Color (Festius?) </div>
                <select onChange={e => this.setState({ color: e.nativeEvent.target.value })}>
                  <option value={BLUE}>blue</option>
                  <option value={RED}>red</option>
                </select>
              </div>
              <div className="calendar-control">
                <div> Enabled Day </div>
                <select
                  value={enabledDay}
                  onChange={e => this.setState({ enabledDay: parseInt(e.nativeEvent.target.value, 10) })}
                >
                  {weekDays.map(value => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </div>
              <div className="calendar-control">
                <div> Frenqüència </div>
                <select
                  defaultValue={this.state.frequencia}
                  onChange={e => this.onChangeDates(e.nativeEvent.target.value)}
                >
                  {frequency.map(value => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="calendar-app">
              <Grid container spacing={8}>
                {calendar.map((value, index) => {
                  return (
                    <div key={months[value]} className="calendar-container">
                      <div className="calendar-month">{months[value]}</div>
                      <Calendar
                        locale="ca-CA"
                        tileClassName={({ date, view }) => this.renderTileClassName(date, view, value)}
                        maxDetail="month"
                        showNavigation={false}
                        view="month"
                        showNeighboringMonth={false}
                        tileDisabled={this.renderTileDisabled.bind(this)}
                        onChange={this.onPressTile}
                        activeStartDate={new Date(2018, value, 1)}
                      />
                    </div>
                  );
                })}
              </Grid>
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} color="primary">
              Cancel·lar
            </Button>
            <Button onClick={this.handleConfirm} color="primary" autoFocus>
              Confirmar
            </Button>
          </DialogActions>
        </Dialog>
        <DialogSelect
          open={this.state.openDialogSelect}
          horaris={this.state.selDia}
          onClose={() => this.setState({ openDialogSelect: false })}
          clickItem={this.handleDialogSelectConfirm}
        />
      </div>
    );
  }
  handleDialogSelectConfirm = dia => {
    const { diesSelected } = this.state;
    diesSelected.push(dia);
    this.setState({ diesSelected, openDialogSelect: false });
  };
  handleDialogSelect = selDia => {
    this.setState({ openDialogSelect: true, selDia });
  };
}

DialogCalendar.propTypes = {
  fullScreen: PropTypes.bool.isRequired,
};

export default withMobileDialog()(DialogCalendar);

Date.prototype.getWeek = function() {
  var date = new Date(this.getTime());
  date.setHours(0, 0, 0, 0);
  // Thursday in current week decides the year.
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  // January 4 is always in week 1.
  var week1 = new Date(date.getFullYear(), 0, 4);
  // Adjust to Thursday in week 1 and count number of weeks from date to week1.
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
};

// Returns the four-digit year corresponding to the ISO week of the date.
Date.prototype.getWeekYear = function() {
  var date = new Date(this.getTime());
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  return date.getFullYear();
};
