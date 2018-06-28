import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

const url = 'http://localhost:8000';

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
});

/**
 * The example data is structured as follows:
 *
 * import image from 'path/to/image.jpg';
 * [etc...]
 *
 * const tileData = [
 *   {
 *     img: image,
 *     title: 'Image',
 *     author: 'author',
 *   },
 *   {
 *     [etc...]
 *   },
 * ];
 */
function NewCategoriesBar(props) {
  const { etiquetes } = props;
  return (
    <div className="root">
      <Grid container spacing={24} className="grid" justify="center">
        {etiquetes.map(tile => (
          <Grid item md={2} sm={4} xs={6} key={url + tile.img}>
            <Paper className="paper" align="center">
              <Typography variant="headline" component="h3">
                {tile.nom}
                <img src={url + tile.img} alt={tile.nom} />
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </div>
  );
}

NewCategoriesBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(NewCategoriesBar);
