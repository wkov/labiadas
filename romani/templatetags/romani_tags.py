# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.html import format_html
from romani.models import UserProfile, Producte
from django.contrib.auth.models import Group

register = Library()


@register.assignment_tag(takes_context=True)
def comandes_unread(context):
    user = user_context(context)
    if not user:
        return ''
    up = UserProfile.objects.get(user=user)
    uno = up.comandes_cistella().count()
    dos = up.contractes_cistella().count()
    total = uno + dos
    return total

@register.assignment_tag(takes_context=True)
def productor_comandes_unread(context):
    user = user_context(context)
    if not user:
        return ''
    up = UserProfile.objects.get(user=user)
    uno = up.pro_comandes().count()
    dos = up.pro_contractes().count()
    total = uno + dos
    return total


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

@register.filter(name='next_day')
def next_day(producte, node):
    ret = producte.next_day(node)
    if ret:
        return ret
    return None

