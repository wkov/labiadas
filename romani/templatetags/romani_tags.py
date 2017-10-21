# -*- coding: utf-8 -*-
from django.template import Library
from romani.models import UserProfile,TipusProducte, Key
from django.contrib.auth.models import Group
from romani.public_views import stock_calc

register = Library()

import datetime
from datetime import timedelta


# usuari_comandes s'utilitza al left_menu.html per a informar de les comandes pendents d'efectuar per part del productor
@register.assignment_tag(takes_context=True)
def usuari_comandes(context):
    user = user_context(context)
    if not user:
        return ''
    up = UserProfile.objects.get(user=user)
    num_comandes = up.comandes_cistella().count()
    return num_comandes

# productor_comandes s'utilitza al left_menu.html per a informar de les comandes pendents d'efectuar per part del productor
@register.assignment_tag(takes_context=True)
def productor_comandes(context):
    user = user_context(context)
    if not user:
        return ''
    up = UserProfile.objects.get(user=user)
    entregas_num = up.pro_entregas().count()
    return entregas_num

# Funció utilitzada per els 2 assignment_tags anteriors
def user_context(context):
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user
    if user.is_anonymous():
        return None
    return user

# has_group s'utilitza a left_menu.html per a saber els rols de l'usuari a l'hora de mostrarli opcions de node o de productor
@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()

#"model_object" s'utilitza al "user_menu.html" per saber en la mateixa template a quin objecte respresenta cada notificacio per a saber a quin camp de la variable notificació cal anar a buscar la foto que es mostra
@register.filter(name='model_object')
def model_object(object, object_name):
    if object_name == 'Producte':
        if isinstance(object, TipusProducte):
            return True
    if object_name == 'UserProfile':
        if isinstance(object, UserProfile):
            return True
    if object_name == 'Key':
        if isinstance(object, Key):
            return True

    return False

# "next_day" s'utilitza a "productes.html", "producte.html", "etiqueta.html" i "buscador.html" per a informar el proper dia en que l'usuari pot rebre el producte
@register.simple_tag(name='next_day')
def next_day(producte, node):
    ret = next_day_calc(producte, node)
    if ret:
        return ret
    return None

# Funció utilitzada per el simple_tag anterior que calcula quant queda per a la próxima possible entrega del producte en un node determinat
def next_day_calc(producte, node):

    date = datetime.datetime.now() + timedelta(hours=producte.productor.hores_limit)
    list = []
    for f in producte.formats.all():
        for s in f.dies_entrega.filter(dia__date__gte=date.date(), dia__node=node).order_by('dia__date'):

            aux = s.dia.franja_inici()
            daytime = datetime.datetime(s.dia.date.year, s.dia.date.month, s.dia.date.day, aux.inici.hour, aux.inici.minute)

            if daytime > date:

                res = stock_calc(s.format, s.dia, 1)
                if res['result'] == True:
                    list.append(daytime)
                    break
    if list:
        list.sort(key=lambda r: r)
        b = list[0]
        a = datetime.datetime.now()
        c = b - a
        d = divmod(c.total_seconds(),86400)
        if d[0] > 1:
            return str(int(d[0])) + " dies"
        else:
            return str(int(divmod(c.total_seconds(),3600)[0])) + " hores"
    else:
        return False