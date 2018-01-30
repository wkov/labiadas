# la massa

Web platform for exchange in cooperation.

- Necessitaràs: 

    Python3.5 / pip 9.0.1 / virtualenv

- Obre el terminal en la carpeta en la que vulguis instal·lar i escriu:

    $ virtualenv lamassa
    $ cd lamassa
    $ source bin/activate
    $ git clone https://github.com/wkov/labiadas.git
    $ cd labiadas
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py collectstatic
    $ python init_new_db
    $ python manage.py createsuperuser
    $ python manage.py runserver
