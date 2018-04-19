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
    calendarData: initialState,
    color: BLUE,
    enabledDay: today.getDay(),
    diesHabils: [],
    diesFestius: [],
    frequencia: '',
  };

  componentWillMount() {
    const calendar = [];
    for (let i = today.getMonth(); i !== endTime.getMonth(); i++) {
      if (!calendar.includes(i)) {
        calendar.push(i);
      }
      if (i === 11) {
        i = -1;
      }
    }
    this.setState({ calendar });
    const { dies } = this.props;
    console.log(dies);
    let month = 0;
    // _.map(dies, obj => {
    //   if (month)
    // })
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.frequencia !== nextProps.frequencia) {
      this.onChangeFrequency(nextProps.frequencia);
    }
  }

  onChangeFrequency = frequencia => {
    const diesHabils = [];
    switch (frequencia) {
      case 'Cada Setmana': {
        for (let i = today.getTime(); i <= endTime; i = i + dayMiliseconds * 7) {
          diesHabils.push(new Date(i).toDateString());
        }
        break;
      }
      case 'Cada 2 Setmanes': {
        for (let i = today.getTime(); i <= endTime; i = i + dayMiliseconds * 14) {
          diesHabils.push(new Date(i).toDateString());
        }
        break;
      }
      case 'Cada 4 Setmanes': {
        for (let i = today.getTime(); i <= endTime; i = i + dayMiliseconds * 28) {
          diesHabils.push(new Date(i).toDateString());
        }
        break;
      }
      default:
        break;
    }
    this.setState({ diesHabils, frequencia });
  };

  onPressTile = value => {
    const data = new Date(value);
    const { diesHabils, diesFestius, color } = this.state;
    switch (color) {
      case BLUE: {
        if (diesHabils.includes(data.toDateString())) {
          diesHabils.splice(diesHabils.indexOf(data.toDateString()), 1);
        } else {
          diesHabils.push(data.toDateString());
          diesHabils.sort((a, b) => a - b);
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
          if (diesHabils.includes(data.toDateString())) {
            diesHabils.splice(diesHabils.indexOf(data.toDateString()), 1);
          }
        }
        break;
      }
      default:
        break;
    }
    this.setState({ diesHabils, diesFestius });
  };

  renderTileClassName(date, view, month) {
    const { diesHabils, diesFestius } = this.state;
    if (date.getMonth() === month && diesFestius.includes(`${date.toDateString()}`)) {
      return 'calendar-tile-holiday';
    } else if (date.getMonth() === month && diesHabils.includes(`${date.toDateString()}`)) {
      return 'calendar-tile-active';
    }
    return null;
  }

  renderTileDisabled({ date }) {
    if (date.getTime() < today.getTime()) return true;
    if (date.getDay() !== this.state.enabledDay) return true;
    return false;
  }

  render() {
    const { open, handleClose, handleConfirm, fullScreen, frequencia } = this.props;
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
                  onChange={e => this.onChangeFrequency(e.nativeEvent.target.value)}
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
            <Button onClick={handleConfirm} color="primary" autoFocus>
              Confirmar
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

DialogCalendar.propTypes = {
  fullScreen: PropTypes.bool.isRequired,
};

export default withMobileDialog()(DialogCalendar);
