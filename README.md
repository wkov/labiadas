# labiadas
Web platform for exchange in cooperation



necessitaràs: 

python3.5, pip, virtualenv

obre el terminal en la carpeta en la que vulguis instal·lar i escriu:

virtualenv lamassa

cd lamassa

source bin/activate

git clone https://github.com/wkov/labiadas.git

cd labiadas

pip install -r requirements.txt

python manage.py makemigrations romani

yes a totes i l'últim 2

python manage.py migrate

python manage.py runserver

http://127.0.0.1:8000/
