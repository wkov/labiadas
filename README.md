# labiadas
Web platform for exchange in cooperation



necessitaràs: 

python3.5

obre el terminal en la carpeta en la que vulguis instal·lar i escriu:

virtualenv lamassa

cd lamassa

source bin/activate

git clone https://github.com/wkov/labiadas.git

cd labiadas

pip install -r requirements.txt

nano ../lib/python3.5/site-packages/django_messages/urls.py

¡¡Canvia tot el fitxer per el següent paràgraf  !!

   

from django.conf.urls import url
from django.views.generic import RedirectView
from django_messages.views import *
urlpatterns = [
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox/'), name='messag$
    url(r'^inbox/$', inbox, name='messages_inbox'),
    url(r'^outbox/$', outbox, name='messages_outbox'),
    url(r'^compose/$', compose, name='messages_compose'),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose$
    url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', view, name='messages_detail'),
    url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
    url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete$
    url(r'^trash/$', trash, name='messages_trash'),
]



Graba i surt

python manage.py makemigrations romani

yes a totes i l'últim 2

python manage.py migrate

python manage.py runserver

http://127.0.0.1:8000/
