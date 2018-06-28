import React, { Component } from 'react';
import PropTypes from 'prop-types';
import _ from 'lodash';
import { withStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Select from '@material-ui/core/Select';

const styles = theme => ({
  root: {
    width: '90%',
  },
  backButton: {
    marginRight: theme.spacing.unit,
  },
  instructions: {
    marginTop: theme.spacing.unit,
    marginBottom: theme.spacing.unit,
  },
});

function getStepContent(stepIndex) {
  switch (stepIndex) {
    case 0:
      return "Selecciona data d'entrega:";
    case 1:
      return 'Franja horària:';
    case 2:
      return 'I freqüència:';

    default:
      return 'Defecte';
  }
}

const frequencies = {
  1: 'Una sola vegada',
  2: 'Cada Setmana',
  3: 'Cada 2 Setmanes',
  4: 'Cada 4 Setmanes',
};

class StepperCart extends Component {
  state = {
    activeStep: 0,
    dia: '',
    hora: '',
    frequencia: '',
    error: '',
    steps: ["Dia d'entrega del producte", 'Franja horària disponible', 'Freqüència de la comanda'],
  };

  handleNext = () => {
    const { activeStep } = this.state;
    this.setState({
      activeStep: activeStep + 1,
      error: '',
    });
  };

  handleBack = () => {
    const { activeStep } = this.state;
    this.setState({
      activeStep: activeStep - 1,
    });
  };

  handleReset = () => {
    this.setState({
      activeStep: 0,
    });
  };

  handleChange = name => event => {
    const { steps, activeStep } = this.state;
    steps[activeStep] = event.target.value;
    this.setState({
      steps,
      [name]: event.target.value,
    });
  };

  handleChangeFrequencia = event => {
    const { steps, activeStep } = this.state;
    const key = parseInt(event.target.value, 10);
    steps[activeStep] = frequencies[key];
    this.setState({
      steps,
      frequencia: key,
    });
    this.props.onChangeFrequencia(key, this.state.hora);
  };

  handleChangeDia = event => {
    const { steps, activeStep } = this.state;
    const stocksData = this.props.data.tipus.dies_stocks_futurs;
    const key = parseInt(event.nativeEvent.target.value, 10);
    steps[activeStep] = new Date(stocksData[key].dia).toDateString();
    this.setState({
      steps,
      dia: stocksData[key],
    });
  };

  handleEmptySelection = () => {
    this.setState({
      error: 'red',
    });
  };

  handleSubmit = () => {
    const { data } = this.props;
    const stocksData = data.tipus.dies_stocks_futurs;
    const { dia, hora, frequencia } = this.state;
    console.log(stocksData);
    const stocks = _.map(stocksData, (obj, key) => ({
      pk: key,
      dia: obj.dia,
      franjes: _.map(obj.franjes, (data, key) => ({ pk: key, ...data })),
    }));
    const diaSel = stocks.find(obj => new Date(obj.dia).toDateString() === new Date(dia.dia).toDateString());
    this.props.submit({
      ...diaSel,
      franjes: diaSel.franjes.find(obj => `${obj.inici} - ${obj.final}` === hora),
      frequencia,
    });
  };

  render() {
    const { classes, data } = this.props;
    const { activeStep, steps } = this.state;
    const stocksData = data.tipus.dies_stocks_futurs;
    return (
      <div className={classes.root}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map(label => {
            return (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            );
          })}
        </Stepper>
        <div>
          {this.state.activeStep === steps.length ? (
            <div>
              <Typography className={classes.instructions}>
                Comproba que les dades siguin correctes i confirma la comanda:
              </Typography>
              <Button onClick={this.handleReset}>Torna</Button>
              <Button raised color="primary" onClick={this.handleSubmit}>
                Confirmar
              </Button>
            </div>
          ) : this.state.activeStep === 0 ? (
            <div>
              <Typography style={{ color: this.state.error }} className={classes.instructions}>
                {getStepContent(activeStep)}
              </Typography>
              <div style={{ display: 'flex' }}>
                <Button disabled={activeStep === 0} onClick={this.handleBack} className={classes.backButton}>
                  Enrere
                </Button>
                <Select style={{ marginRight: 20 }} native fullWidth onChange={this.handleChangeDia}>
                  <option value="" />
                  {_.map(stocksData, (value, key) => (
                    <option key={value.dia} value={key}>
                      {new Date(value.dia).toDateString()}
                    </option>
                  ))}
                </Select>
                <Button raised color="primary" onClick={this.state.dia ? this.handleNext : this.handleEmptySelection}>
                  {activeStep === steps.length - 1 ? 'Acabar' : 'Següent'}
                </Button>
              </div>
            </div>
          ) : this.state.activeStep === 1 ? (
            <div>
              <Typography style={{ color: this.state.error }} className={classes.instructions}>
                {getStepContent(activeStep)}
              </Typography>
              <div style={{ display: 'flex' }}>
                <Button disabled={activeStep === 0} onClick={this.handleBack} className={classes.backButton}>
                  Enrere
                </Button>
                <Select
                  native
                  style={{ marginRight: 20 }}
                  fullWidth
                  value={this.state.hora}
                  onChange={this.handleChange('hora')}
                >
                  <option value="" />
                  {_.map(this.state.dia.franjes, value => (
                    <option key={value.inici} value={`${value.inici} - ${value.final}`}>
                      {`${value.inici} - ${value.final}`}
                    </option>
                  ))}
                </Select>
                <Button raised color="primary" onClick={this.state.hora ? this.handleNext : this.handleEmptySelection}>
                  {activeStep === steps.length - 1 ? 'Acabar' : 'Següent'}
                </Button>
              </div>
            </div>
          ) : (
            <div>
              <Typography style={{ color: this.state.error }} className={classes.instructions}>
                {getStepContent(activeStep)}
              </Typography>
              <div style={{ display: 'flex' }}>
                <Button disabled={activeStep === 0} onClick={this.handleBack} className={classes.backButton}>
                  Enrere
                </Button>
                <Select
                  style={{ marginRight: 20 }}
                  native
                  fullWidth
                  value={this.state.frequencia}
                  onChange={this.handleChangeFrequencia}
                >
                  <option value="" />
                  {_.map(frequencies, (value, index) => (
                    <option key={value} value={index}>
                      {value}
                    </option>
                  ))}
                </Select>
                <Button
                  raised
                  color="primary"
                  onClick={this.state.frequencia ? this.handleNext : this.handleEmptySelection}
                >
                  {activeStep === steps.length - 1 ? 'Acabar' : 'Següent'}
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }
}

StepperCart.propTypes = {
  classes: PropTypes.object,
};

export default withStyles(styles)(StepperCart);
