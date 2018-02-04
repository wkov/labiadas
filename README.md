# la massa

Web platform for exchange in cooperation.

- Necessitaràs: 

    Python3.5 / Pip 9.0.1 / Virtualenv

on LINUX:

- Obre el terminal en la carpeta en la que vulguis instal·lar i escriu:

    $ virtualenv lamassa
    
    $ cd lamassa
    
    $ source bin/activate
    
    $ git clone https://github.com/wkov/labiadas.git
    
    $ cd labiadas
    
    $ pip install -r requirements.txt
    
    $ python manage.py migrate
    
    $ python init_new_db
    
    $ python manage.py createsuperuser
    
    $ python manage.py runserver

on WINDOWS:

- Obre el GIT en la carpeta en la que vulguis instal·lar i escriu:

    $ virtualenv lamassa
    
    $ cd lamassa
    
    $ source activate
    
    $ git clone https://github.com/wkov/labiadas.git
    
    $ cd labiadas
    
    $ pip install -r requirements.txt
    
    $ py manage.py migrate
    
    $ py init_new_db
    
    $ py manage.py createsuperuser
    
    $ py manage.py runserver
