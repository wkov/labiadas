# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.html import format_html
from romani.models import UserProfile, Producte, TipusProducte, Key
from django.contrib.auth.models import Group
from romani.public_views import stock_check_cant

register = Library()

import datetime
from datetime import timedelta

@register.assignment_tag(takes_context=True)
def comandes_unread(context):
    user = user_context(context)
    if not user:
        return ''
    up = UserProfile.objects.get(user=user)
    num_comandes = up.comandes_cistella().count()
    # dos = up.contractes_cistella().count()
    # total = uno + dos
    return num_comandes

@register.assignment_tag(takes_context=True)
def productor_comandes_unread(context):
    user = user_context(context)
    if not user:
        return ''
    up = UserProfile.objects.get(user=user)
    entregas_num = up.pro_entregas().count()
    # dos = up.pro_contractes().count()
    # total = uno + dos
    return entregas_num


def user_context(context):
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user
    if user.is_anonymous():
        return None
    return user

@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()

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


@register.simple_tag(name='next_day')
def next_day(producte, node):
    ret = next_day_calc(producte, node)
    if ret:
        return ret
    return None

def next_day_calc(producte, node):

    date = datetime.datetime.now() + timedelta(hours=producte.productor.hores_limit)
    list = []
    for f in producte.formats.all():
        for s in f.dies_entrega.filter(dia__date__gte=date.date(), dia__node=node).order_by('dia__date'):

            aux = s.dia.franja_inici()
            daytime = datetime.datetime(s.dia.date.year, s.dia.date.month, s.dia.date.day, aux.inici.hour, aux.inici.minute)

            if daytime > date:

                res = stock_check_cant(s.format, s.dia, 1)
                if res:
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