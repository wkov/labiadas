import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { FormGroup, FormFeedback, Label, Input } from 'reactstrap';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
  },
});

const FormInput = props => {
  const { classes, name, label, error, type, ...rest } = props;
  const id = `id_${name}`,
    input_type = type ? type : 'text';
  return (
    <div className={classes.container}>
      <FormControl
        className={classes.formControl}
        error
        aria-describedby={error ? 'name-error-text' : 'name-helper-text'}
      >
        <InputLabel htmlFor={error ? 'name-error' : 'name-helper'}>{label}</InputLabel>
        <Input type={input_type} id={id} value={name} {...rest} />
        {error ? <FormHelperText id="name-error-text">{error}</FormHelperText> : ''}
      </FormControl>
    </div>
  );
};

FormInput.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(FormInput);
