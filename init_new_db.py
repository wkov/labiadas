


import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labiadas.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


from romani.models import UserProfile, Node, Frequencia
#from django.contrib.auth.models import User

#user = User.objects.get(pk=1)

freq1 = Frequencia.objects.create(num=1, nom="cada setmana")
freq2 = Frequencia.objects.create(num=2, nom="cada 2 setmanes")
freq3 = Frequencia.objects.create(num=3, nom="cada 3 setmanes")
freq4 = Frequencia.objects.create(num=4, nom="cada 4 setmanes")
freq5 = Frequencia.objects.create(num=5, nom="mes d una vegada")
freq6 = Frequencia.objects.create(num=6, nom="una sola vegada")

node = Node.objects.create(nom="la massa", position="41.5,1.3", poblacio="Mollet", a_domicili="False", frequencia=freq5)

#node.responsable.add(user)

#node.save()

#up = UserProfile.objects.create(user=user, lloc_entrega=node, invitacions=1000)

