# -*- coding: utf-8 -*-
from django.template import Library
from romani.models import UserProfile,TipusProducte, Key, DiaFormatStock
from django.contrib.auth.models import Group
# from romani.public_views import stock_calc

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

# @register.filter(name='has_stock')
# def has_stock(format, user_id):
#     up = UserProfile.objects.get(user__pk=user_id)
#     dies_node_entrega = up.lloc_entrega.dies_entrega.filter(date__gt = datetime.date.today)
#     for d in dies_node_entrega:
#         diaformatstock = DiaFormatStock.objects.get(dia=d, format=format)
#         date = datetime.datetime.now() + timedelta(hours=diaformatstock.hores_limit)
#         aux = d.franja_inici()
#         daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
#         if daytime > date:
#             stock_result = stock_calc(format, d, 1)
#             if stock_result['result'] == True:
#                 return True

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

    # date = datetime.datetime.now() + timedelta(hours=producte.productor.hores_limit)
    list = []
    for f in producte.formats.all():
        for s in f.dies_entrega.filter(dia__date__gte=datetime.datetime.now(), dia__node=node).order_by('dia__date'):
            date = datetime.datetime.now() + timedelta(hours=s.hores_limit)
            aux = s.dia.franja_inici()
            daytime = datetime.datetime(s.dia.date.year, s.dia.date.month, s.dia.date.day, aux.inici.hour, aux.inici.minute)

            if daytime > date:

                res = s.format.stock_calc(s.dia, 1)
                if res['result'] == True:
                    list.append(daytime)
                    break
    nes = producte.next_day_sec(node)
    if nes['result'] == True:
        d = divmod(nes['next_day'],86400)
        if d[0] > 1:
            return str(int(d[0])) + " dies"
        else:
            return str(int(divmod(nes['next_day'],3600)[0])) + " hores"
    else:
        return False