import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import CardContent from '@material-ui/core/CardContent';
import Card from '@material-ui/core/Card';
import Divider from '@material-ui/core/Divider';

const ProductReviews = () => {
  const comentaris = [
    {
      usuari: 'Paco de los Palotes',
      comentari:
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Omnis et enim aperiam inventore, similique necessitatibus neque non! Doloribus, modi sapiente laboriosam aperiam fugiat laborum. Sequi mollitia, necessitatibus quae sint natus.',
      data: '14/01/2018',
    },
    {
      usuari: 'Paco de los Palotes',
      comentari:
        'Lorem ipsum dolo2r sit amet, consectetur adipisicing elit. Omnis et enim aperiam inventore, similique necessitatibus neque non! Doloribus, modi sapiente laboriosam aperiam fugiat laborum. Sequi mollitia, necessitatibus quae sint natus.',
      data: '14/01/2018',
    },
    {
      usuari: 'Paco de los Palotes',
      comentari:
        'Lo1rem ipsum dolo2r sit amet, consectetur adipisicing elit. Omnis et enim aperiam inventore, similique necessitatibus neque non! Doloribus, modi sapiente laboriosam aperiam fugiat laborum. Sequi mollitia, necessitatibus quae sint natus.',
      data: '14/01/2018',
    },
  ];
  return (
    <Card className="card-review-product">
      <CardContent>
        <div className="cards-title">Comentaris del producte</div>
        <Divider />
        <List>
          {comentaris.map(value => (
            <ListItem key={value.comentari} style={{ display: 'block' }}>
              <div className="cards-text">{value.comentari}</div>
              <br />
              <div className="cards-subtext">{`Enviat per ${value.usuari} el dia ${value.data}`}</div>
              <Divider />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default ProductReviews;
