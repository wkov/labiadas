__author__ = 'sergi'

from django.shortcuts import render, get_object_or_404
from romani.models import Producte, Productor, Comanda, TipusProducte, Node, DiaEntrega, FranjaHoraria, Frequencia, DiaProduccio, Vote, Entrega, Stock
from django.db.models import Q
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from romani.models import UserProfile, Etiqueta, Adjunt, DiaFormatStock
from romani.forms import ComandaForm, VoteForm
from romani.serializers import EntregaSerializer

from django.http import HttpResponse

from django.utils import timezone
from notifications import notify
import json
from django.contrib import messages

import datetime
from datetime import timedelta


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def buskadorProducte(request):

    searchString = request.POST.get('searchString', 0)
    #ToDo Afegir Cela al Buscador, Django no permet Ands i Ors, Construir query manualment

    # etiquetes = Etiqueta.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    etiquetes_pre = Etiqueta.objects.all()

    dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt = datetime.datetime.now())

    etiquetes = set()

    for e in etiquetes_pre:
        for p in e.producte_set.all():
            for f in p.formats.all():
                for p2 in f.dies_entrega.all():
                    if p2.dia in dies_node_entrega:
                        etiquetes.add(e)
                        break




    if not searchString == 0:




        prod_aux = set()
        formats_aux = set()

        for d in dies_node_entrega:
            for t in TipusProducte.objects.filter(dies_entrega__dia=d):
                diaformatstock = DiaFormatStock.objects.get(dia=d, format=t)
                date = datetime.datetime.now() + timedelta(hours=diaformatstock.hores_limit)
                aux = d.franja_inici()
                daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
                if daytime > date:
                    stock_result = t.stock_calc(d, 1)
                    if stock_result['result'] == True:
                        prod_aux.add(t.producte.pk)
                        formats_aux.add(t)
        p = Producte.objects.filter((Q(nom__icontains = searchString) | Q(descripcio__icontains = searchString) | Q(keywords__icontains = searchString)),
                                        pk__in=prod_aux).distinct()

        productes = sorted(p, key=lambda a: a.karma(user_p.lloc_entrega), reverse=True)

        return render(request, "buscador.html", {
            'posts': productes,
            'formats': formats_aux,
            'etiquetes': etiquetes, 'up': user_p})
    else:
        return render(request, "buscador.html", {
            'etiquetes': etiquetes, 'up': user_p})



def coopeView(request):

    user_p = UserProfile.objects.filter(user=request.user).first()

    today = datetime.date.today()

    dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt = today)

    # etiquetes_pre = Etiqueta.objects.all()

    etiquetes = set()

    # for e in etiquetes_pre:
    #     for p in e.producte_set.all():
    #         for f in p.formats.all():
    #             for p2 in f.dies_entrega.all():
    #                 if p2.dia in dies_node_entrega:
    #                     etiquetes.add(e)
    #                     break

    nodes = Node.objects.all()


    prod_aux = set()
    formats_aux = set()

    for d in dies_node_entrega:
        for t in TipusProducte.objects.filter(dies_entrega__dia=d):
            diaformatstock = DiaFormatStock.objects.get(dia=d, format=t)
            date = datetime.datetime.now() + timedelta(hours=diaformatstock.hores_limit)
            aux = d.franja_inici()
            daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                stock_result = t.stock_calc(d, 1)
                if stock_result['result'] == True:
                    prod_aux.add(t.producte.pk)
                    etiquetes.add(t.producte.etiqueta)
                    formats_aux.add(t)
    p = Producte.objects.filter(pk__in=prod_aux).distinct()


    productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega), reverse=True)

    paginator = Paginator(productes, 12) # Show 24 productes per page

    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, "productes.html", {'productes':products, 'formats':formats_aux, 'etiquetes': etiquetes, 'nodes':nodes, 'up': user_p})


def producteView(request,pk):

    producte = Producte.objects.filter(pk=pk).first()
    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()
    votes = Vote.objects.filter(entrega__comanda__format__producte=producte).exclude(text='').order_by('-entrega__dia_entrega__date')

    dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt = datetime.datetime.now())
    formats_aux = set()

    for d in dies_node_entrega:
        for t in TipusProducte.objects.filter(dies_entrega__dia=d, producte=producte):
            diaformatstock = DiaFormatStock.objects.get(dia=d, format=t)
            date = datetime.datetime.now() + timedelta(hours=diaformatstock.hores_limit)
            aux = d.franja_inici()
            daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                stock_result = t.stock_calc(d, 1)
                if stock_result['result'] == True:
                    formats_aux.add(t)

    return render(request, "producte.html",{'producte': producte, 'formats': formats_aux, 'nodes': nodes, 'up': user_p, 'votes': votes})

def etiquetaView(request,pk):

    # etiquetes = Etiqueta.objects.all()
    etiqueta = Etiqueta.objects.filter(pk=pk).first()

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()


    dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt = datetime.datetime.now())


    etiquetes_pre = Etiqueta.objects.all()

    etiquetes = set()

    for e in etiquetes_pre:
        for p in e.producte_set.all():
            for f in p.formats.all():
                for p2 in f.dies_entrega.all():
                    if p2.dia in dies_node_entrega:
                        etiquetes.add(e)
                        break


    prod_aux = set()
    formats_aux = set()

    for d in dies_node_entrega:
        for t in TipusProducte.objects.filter(dies_entrega__dia=d, producte__etiqueta=etiqueta):
            diaformatstock = DiaFormatStock.objects.get(dia=d, format=t)
            date = datetime.datetime.now() + timedelta(hours=diaformatstock.hores_limit)
            aux = d.franja_inici()
            daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                stock_result = t.stock_calc(d, 1)
                if stock_result['result'] == True:
                    prod_aux.add(t.producte.pk)
                    formats_aux.add(t)


    p = Producte.objects.filter(pk__in=prod_aux).distinct()


    productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega), reverse=True)

    paginator = Paginator(productes, 12) # Show 24 productes per page

    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, "etiqueta.html",{'productes': products, 'formats': formats_aux, 'etiquetes': etiquetes, 'etiqueta': etiqueta, 'nodes': nodes, 'up': user_p})


def productorView(request,pk):

    productor = Productor.objects.filter(pk=pk).first()
    user_p = UserProfile.objects.filter(user=request.user).first()
    dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt = datetime.datetime.now())
    p = Producte.objects.filter(productor=productor, formats__dies_entrega__dia__in = dies_node_entrega ).distinct()
    adjunts = Adjunt.objects.filter(productor=productor)
    productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega), reverse=True)

    return render(request, "productor.html",{'productor': productor, 'productes': productes, 'adjunts': adjunts, 'up': user_p})


def cistella(user):
    orders = []
    days = []
    day = {}
    date = ""
    entrega = ""
    total = 0
    now = datetime.datetime.now()
    entregas = Entrega.objects.filter(comanda__client=user, dia_entrega__date__gte=now).order_by(
        'dia_entrega__date', 'franja_horaria__inici')
    # com = Comanda.objects.filter(entregas__in=entregas).distinct()
    # entregas_hist = Entrega.objects.filter(comanda__client=user).filter(Q(dia_entrega__date__lte=now)).order_by(
    #     'dia_entrega__date', 'franja_horaria__inici')
    # hist = Comanda.objects.filter(entregas__in=entregas_hist).distinct()
    if entregas:
        for e in entregas:
            if date:
                if e.dia_entrega != date:
                    day = {'entregas': orders, 'dia': date.date, 'total':total}
                    days.append(day)
                    total = 0
                    orders = []
            date = e.dia_entrega
            e_dict = {'pk': e.comanda.pk,
                      'entrega_pk': e.pk,
                      'producte': e.comanda.format.producte.nom,
                      'productor': e.comanda.format.productor.nom,
                      'cantitat': e.comanda.cantitat,
                      'format': e.comanda.format.nom,
                      'preu': e.comanda.preu,
                      'lloc': e.dia_entrega.node.nom,
                      'hora': e.franja_horaria,
                      'dia': e.dia_entrega.date
                      }
            total += e.comanda.preu
            orders.append(e_dict)
        day = {'entregas': orders, 'dia': date.date, 'total': str(total)}
        days.append(day)
    return days

def cistellaView(request):

        # orders = {}
        # date = ""

    days = cistella(request.user)
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "romani/consumidors/comandes.html", {'comandes': days, 'up': user_p})



def comandesView(request):

    now = datetime.datetime.now()
    entregas = Entrega.objects.filter(comanda__client=request.user, dia_entrega__date__gte=now)

    com = Comanda.objects.filter(entregas__in=entregas).distinct()

    comandes = sorted(com, key=lambda a: (a.prox_entrega().dia_entrega.date, a.prox_entrega().franja_horaria.inici))

    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "romani/consumidors/comandes.html", {'comandes': comandes, 'up': user_p })

def historialView(request):
    orders = []
    days = []
    day = {}
    date = ""
    entrega = ""
    total = 0
    now = datetime.datetime.now()
    entregas_hist = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__lte=now)).order_by(
        '-dia_entrega__date', 'franja_horaria__inici')
    # hist = Comanda.objects.filter(entregas__in=entregas_hist).distinct()
    if entregas_hist:
        for e in entregas_hist:
            if date:
                if e.dia_entrega != date:
                    day = {'entregas': orders, 'dia': date.date, 'total': total}
                    days.append(day)
                    total = 0
                    orders = []
            date = e.dia_entrega
            e_dict = {'pk': e.pk,
                      'comanda_pk':e.comanda.pk,
                      'producte': e.comanda.format.producte.nom,
                      'productor': e.comanda.format.productor.nom,
                      'cantitat': e.comanda.cantitat,
                      'format': e.comanda.format.nom,
                      'preu': e.comanda.preu,
                      'lloc': e.dia_entrega.node.nom,
                      'hora': e.franja_horaria,
                      'dia': e.dia_entrega.date
                      }
            total += e.comanda.preu
            orders.append(e_dict)
        day = {'entregas': orders, 'dia': date.date, 'total': str(total)}
        days.append(day)

    voted = Vote.objects.filter(voter=request.user)

    comandes_in_page = [comanda.pk for comanda in entregas_hist]

    upvoted_comandes = voted.filter(entrega_id__in=comandes_in_page, positiu=True)

    if upvoted_comandes:
        upvoted_comandes = upvoted_comandes.values_list('entrega_id', flat=True)

    downvoted_comandes = voted.filter(entrega_id__in=comandes_in_page, positiu=False)

    if downvoted_comandes:
        downvoted_comandes = downvoted_comandes.values_list('entrega_id', flat=True)

    user_p = UserProfile.objects.filter(user=request.user).first()
    return render(request, "romani/consumidors/historial.html", {'comandes': days, 'up': user_p,
                                                                 'upvoted_comandes': upvoted_comandes,
                                                                 'downvoted_comandes': downvoted_comandes
                                                                 })


def entregasView(request):

    now = datetime.datetime.now()
    entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__lte=now)).order_by('-dia_entrega__date', 'franja_horaria__inici')
    voted = Vote.objects.filter(voter=request.user)

    comandes_in_page = [comanda.pk for comanda in entregas]

    upvoted_comandes = voted.filter(entrega_id__in=comandes_in_page, positiu = True)

    if upvoted_comandes:
        upvoted_comandes = upvoted_comandes.values_list('entrega_id', flat=True)

    downvoted_comandes = voted.filter(entrega_id__in=comandes_in_page, positiu = False)

    if downvoted_comandes:
        downvoted_comandes = downvoted_comandes.values_list('entrega_id', flat=True)

    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "entregas.html",{'comandes': entregas, 'up': user_p, 'upvoted_comandes': upvoted_comandes,
                                            'downvoted_comandes': downvoted_comandes })


def entregaDelete(request, pk):

    entregaDel = Entrega.objects.filter(pk=pk).first()

    dia_entregatime = entregaDel.comanda.format.dies_entrega.get(dia=entregaDel.dia_entrega)
    # time = dies_entrega.get(dia=entregaDel.dia_entrega)
    dia = datetime.datetime.now() + timedelta(hours=dia_entregatime.hores_limit)
    # prox_entrega = comandaDel.prox_entrega()
    dia_prox_entrega = entregaDel.dia_entrega
    aux = dia_prox_entrega.franja_inici()
    daytime = datetime.datetime(dia_prox_entrega.date.year, dia_prox_entrega.date.month, dia_prox_entrega.date.day, aux.inici.hour, aux.inici.minute)

    if daytime > dia:
        notify.send(entregaDel.comanda.format, recipient = request.user,  verb="Has tret ", action_object=entregaDel,
            description="de la cistella" , timestamp=timezone.now())
        # url=comandaDel.format.producte.foto.url,
        entregaDel.delete()
        messages.info(request, (u"Has anulat la entrega i hem tret el producte de la cistella"))
    else:
        messages.error(request, (u"El productor ja t'està preparant la comanda, no podem treure el producte de la cistella"))

    # now = datetime.datetime.now()
    # entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__gte=now)).order_by('-data_comanda')
    # comandes = Comanda.objects.filter(entregas__in=entregas).distinct()
    user_p = UserProfile.objects.filter(user=request.user).first()
    days = cistella(request.user)

    return render(request, "romani/consumidors/comandes.html",{'comandes': days, 'up': user_p})




# No es fa servir ara mateix. Ara es fa servir entregaDelete
#  Funció per borrar comandes per part de l'usuari. Comprovem que el productor no hagi començat a elaborar el producte solicitat
def comandaDelete(request, pk):

    comandaDel = Comanda.objects.filter(pk=pk).first()


    dia = datetime.datetime.now() + timedelta(hours=comandaDel.format.productor.hores_limit)
    prox_entrega = comandaDel.prox_entrega()
    dia_prox_entrega = prox_entrega.dia_entrega
    aux = dia_prox_entrega.franja_inici()
    daytime = datetime.datetime(dia_prox_entrega.date.year, dia_prox_entrega.date.month, dia_prox_entrega.date.day, aux.inici.hour, aux.inici.minute)

    if daytime > dia:
        notify.send(comandaDel.format, recipient = request.user,  verb="Has tret ", action_object=comandaDel,
            description="de la cistella" , timestamp=timezone.now())
        # url=comandaDel.format.producte.foto.url,
        comandaDel.delete()
        messages.info(request, (u"Has anulat la comanda i hem tret el producte de la cistella"))
    else:
        messages.error(request, (u"El productor ja t'està preparant la comanda, no podem treure el producte de la cistella"))

    # now = datetime.datetime.now()
    # entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__gte=now)).order_by('-data_comanda')
    # comandes = Comanda.objects.filter(entregas__in=entregas).distinct()
    user_p = UserProfile.objects.filter(user=request.user).first()
    days = cistella(request.user)

    return render(request, "romani/consumidors/comandes.html",{'comandes': days, 'up': user_p})



# Funció que donat un dia d i un dia de la setmana calcula el pròxim dia en que serà el dia de la setmana indicat
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)



# Aquesta funció calcula els dies d'entrega d'un producte donats els paràmetres inicials de freqüència, 1r dia d'entrega, franja horària desitjada i el node
# on el recollirà. Escull tots els dies en que es cumpleixen les condicions fins a trobar el 1r cas en que no és possible i allà s'atura
def prox_calc(format, node, dia_entrega, franja, frequencia):

        d = dia_entrega.date
        d_list = []
        next_val = True
        d_list.append(dia_entrega)

        if frequencia.num == 1:
            while(next_val):
                d = next_weekday(d, int(dia_entrega.dia_num()))
                try:
                    s = DiaEntrega.objects.get(date=d, node=node, franjes_horaries__id__exact=franja.id, formats__format__id__exact=format.pk)
                    d_list.append(s)
                except:
                    return d_list
        if frequencia.num == 2:
            while(next_val):
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                try:
                    s = DiaEntrega.objects.get(date=d, node=node, franjes_horaries__id__exact=franja.id, formats__format__id__exact=format.pk)
                    d_list.append(s)
                except:
                    return d_list

        if frequencia.num == 3:
            while(next_val):
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                try:
                    s = DiaEntrega.objects.get(date=d, node=node, franjes_horaries__id__exact=franja.id, formats__format__id__exact=format.pk)
                    d_list.append(s)
                except:
                    return d_list

        if frequencia.num == 4:
            while(next_val):
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                try:
                    s = DiaEntrega.objects.get(date=d, node=node, franjes_horaries__id__exact=franja.id, formats__format__id__exact=format.pk)
                    d_list.append(s)
                except:
                    return d_list
        return d_list



# Complement de ComandaFormBaseView per a permetre la comunicació amb "comanda.js"
class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

# Vista del Formulari que confirma una comanda després que l'usuari ratifiqui el que demana en la finestra modal. Lligat a "comanda.js"
class ComandaFormBaseView(FormView):
    form_class = ComandaForm


    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        producte = get_object_or_404(Producte, pk=form.data["producte_pk"])
        user = self.request.user
        format = get_object_or_404(TipusProducte, pk=form.data["format_pk"])
        user_profile = UserProfile.objects.filter(user = user).first()
        cantitat = form.data["cantitat_t"]
        preu_aux = format.preu
        preu = preu_aux * float(cantitat)
        data = form.data["dataentrega"]
        frequencia = form.data["frequencia"]
        freq = Frequencia.objects.filter(num=frequencia).first()
        data_entrega = DiaEntrega.objects.get(pk=data)
        franja_pk = form.data["franjes"]
        franja = FranjaHoraria.objects.get(pk=franja_pk)

        lloc = form.data["lloc_entrega"]
        lloc_obj = get_object_or_404(Node, pk = lloc)

        # if (lloc_obj.a_domicili == True):
        #
        #     user_profile.carrer = form.data["carrer"]
        #     user_profile.numero = form.data["numero"]
        #     user_profile.pis = form.data["pis"]
        #     user_profile.poblacio = form.data["poblacio"]
        # user_profile.save()



        if frequencia == '6':   #freqüència: una sola vegada
            stock_result = format.stock_calc(data_entrega, cantitat)
            if stock_result['result'] == True:
                v = Comanda.objects.create(client=user, cantitat=cantitat, format=format, node=lloc_obj, preu=preu, frequencia=freq)
                if stock_result['dia_prod'] == '':
                    e = Entrega.objects.create(dia_entrega=data_entrega, comanda=v, franja_horaria=franja)
                else:
                    e = Entrega.objects.create(dia_entrega=data_entrega, comanda=v, franja_horaria=franja, dia_produccio=stock_result['dia_prod'] )
                ret = {"contracte": 0, "success": 1}
                # notify.send(format, recipient= user, verb="Has afegit a la cistella", action_object=v,
                #     description=e.dia_entrega.date , timestamp=timezone.now())
                # messages.success(self.request, (u"Comanda realitzada correctament"))
            else:
                ret = {"contracte": 0, "success": 0}
                # messages.error(self.request, (u"Disculpa, NO està disponible la cantitat sol·licitada"))

        else:     #freqüència: més d'una vegada o periòdic

            dies_entrega = prox_calc(format, lloc_obj, data_entrega, franja, freq)

            error = 0

            v = Comanda.objects.create(client=user, cantitat=cantitat, format=format, node=lloc_obj, preu=preu, frequencia=freq)

            for d in dies_entrega:
                stock_result = format.stock_calc(d, cantitat)
                if stock_result['result'] == True:
                    if stock_result['dia_prod'] == '':
                        e = Entrega.objects.create(dia_entrega=d, comanda=v, franja_horaria=franja)
                    else:
                        e = Entrega.objects.create(dia_entrega=d, comanda=v, franja_horaria=franja, dia_produccio=stock_result['dia_prod'] )
                else:
                    error = error + 1

            if error > 0:
                messages.error(self.request, (u"En algun dels dies en que volies producte, NO està disponible"))
                ret = {"contracte": 0, "success": 0}
            else:
                # En aquest cas al ser una comanda amb varies entregues, no donem encara pere finalitzat el procés. A l'usuari se li mostrarà
                # "dies_comanda.html" per a que trii tots els dies d'entrega que desitji
                ret = {"contracte": 1, "success": 1, "pk": v.pk}

            notify.send(format, recipient= user, verb="Has afegit a la cistella", action_object=v,
            description=v.frequencia , timestamp=timezone.now())

        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)

# Fusió de les classes JSONFormMixin, ComandaFormBaseView.ñ Utilització per part de la URL "/comanda/" per a AJAX amb "comanda.js"
class ComandaFormView(JSONFormMixin, ComandaFormBaseView):
    pass


# Visualització que permet triar els dies d'entrega que conté una comanda al realitzarla
def diesEntregaView(request, pk, pro):
    now = datetime.datetime.now()
    comanda = Comanda.objects.get(pk=pk)
    user_p = UserProfile.objects.filter(user=request.user).first()
    date = datetime.datetime.now() + timedelta(hours=int(comanda.format.productor.hores_limit))

    # Llistat de dies futurs en que es posible demanar noves entregues de la comanda
    pk_lst = set()
    for d in DiaEntrega.objects.filter(date__gte=datetime.datetime.now(), formats__format__id__exact=comanda.format.id, node=comanda.node).order_by('date'):
        try:
            diaformatstock = DiaFormatStock.objects.get(dia=d, format=comanda.format)
            date = datetime.datetime.now() + timedelta(hours=int(diaformatstock.hores_limit))
            aux = d.franja_inici()
            daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                stock_result = comanda.format.stock_calc(d, comanda.cantitat)
                if stock_result['result'] == True:
                    pk_lst.add(d.pk)
        except:
            pass
    # Llistat de dies futurs en que ja ha demanat rebre producte
    pk2_lst = set()
    for d in Entrega.objects.filter(comanda=comanda, dia_entrega__node=comanda.node, dia_entrega__date__gte=date).order_by('dia_entrega__date'):
        try:
            diaformatstock = DiaFormatStock.objects.get(dia=d.dia_entrega, format=comanda.format)
            date = datetime.datetime.now() + timedelta(hours=int(diaformatstock.hores_limit))
            aux = d.dia_entrega.franja_inici()
            daytime = datetime.datetime(d.dia_entrega.date.year, d.dia_entrega.date.month, d.dia_entrega.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                pk2_lst.add(d.dia_entrega.pk)
        except:
            pass
    dies_entrega_possibles = DiaEntrega.objects.filter((Q(pk__in=pk_lst)|Q(pk__in=pk2_lst))).order_by('date')

    dies_entrega_ini = DiaEntrega.objects.filter(pk__in=pk2_lst)

    # Llistat de dies passats en que té entregues de la mateixa comanda
    pk3_lst = set()
    for d in Entrega.objects.filter(comanda=comanda, dia_entrega__node=comanda.node, dia_entrega__date__lte=date).order_by('dia_entrega__date'):
        try:
            diaformatstock = DiaFormatStock.objects.get(dia=d.dia_entrega, format=comanda.format)
            date = datetime.datetime.now() + timedelta(hours=int(diaformatstock.hores_limit))
            aux = d.dia_entrega.franja_inici()
            daytime = datetime.datetime(d.dia_entrega.date.year, d.dia_entrega.date.month, d.dia_entrega.date.day, aux.inici.hour, aux.inici.minute)
            if daytime < date:
                pk3_lst.add(d.pk)
        except:
            pass

    entregas_pas = Entrega.objects.filter(pk__in=pk3_lst).exclude(dia_entrega__pk__in=pk_lst)



    if request.POST:
        try:
            dies_pk = request.POST.getlist('dies')
            for d in dies_pk:
                dia = DiaEntrega.objects.get(pk=d)
                if dia in dies_entrega_ini:
                    franja_pk = request.POST.get(str(dia.pk))
                    franja = FranjaHoraria.objects.get(pk=franja_pk)
                    entrega = Entrega.objects.get(comanda=comanda, dia_entrega=d)
                    if entrega.franja_horaria == franja:
                        pass
                    else:
                        # Aquí processem les entregues quan ja existien i simplement l'usuari modifica l'hora d'entrega dins el mateix dia en que ja havia demanat
                        entrega.delete() #1r borrem l'anterior entrega pq al canviar la hora ja no és vàlida
                        stock_result = comanda.format.stock_calc(dia, comanda.cantitat)
                        if stock_result['dia_prod'] == '':
                            e = Entrega.objects.create(dia_entrega=dia, comanda=comanda, franja_horaria=franja)
                        else:
                            e = Entrega.objects.create(dia_entrega=dia, comanda=comanda, franja_horaria=franja, dia_produccio=stock_result['dia_prod'] )
                        notify.send(e.comanda.format, recipient= user_p.user, verb="Has modificat l'hora d'entrega de ", action_object=e.comanda,
                        description=e.dia_entrega.date , timestamp=timezone.now())
                else:
                    # Aquí processem les entregues que encara no existien i que es creen noves
                    stock_result = comanda.format.stock_calc(dia, comanda.cantitat)
                    if stock_result['result'] == True:
                        franja_pk = request.POST.get(str(dia.pk))
                        franja = FranjaHoraria.objects.get(pk=franja_pk)
                        if stock_result['dia_prod'] == '':
                            e = Entrega.objects.create(dia_entrega=dia, comanda=comanda, franja_horaria=franja)
                        else:
                            e = Entrega.objects.create(dia_entrega=dia, comanda=comanda, franja_horaria=franja, dia_produccio=stock_result['dia_prod'] )
                        notify.send(e.comanda.format, recipient= user_p.user, verb="Has afegit a la cistella", action_object=e.comanda,
                        description=e.dia_entrega.date , timestamp=timezone.now())
            for d in dies_entrega_ini:
                if str(d.pk) not in dies_pk:
                    # Borrem les entregues que han deixat d'estar seleccionades
                    entrega = Entrega.objects.get(comanda=comanda, dia_entrega=d)

                    dia_entregatime = entrega.comanda.format.dies_entrega.get(dia=entrega.dia_entrega)
                    # time = dies_entrega.get(dia=entregaDel.dia_entrega)
                    dia = datetime.datetime.now() + timedelta(hours=dia_entregatime.hores_limit)
                    # prox_entrega = comandaDel.prox_entrega()
                    dia_prox_entrega = entrega.dia_entrega
                    aux = dia_prox_entrega.franja_inici()
                    daytime = datetime.datetime(dia_prox_entrega.date.year, dia_prox_entrega.date.month,
                                                dia_prox_entrega.date.day, aux.inici.hour, aux.inici.minute)

                    if daytime > dia:





                        entrega.delete()
                        notify.send(entrega.comanda.format, recipient= user_p.user, verb="Has tret de la cistella", action_object=entrega.comanda,
                        description=entrega.dia_entrega.date , timestamp=timezone.now())
                    else:
                        messages.error(request, (
                            u"El productor ja t'està preparant alguna de les comandes que vols anul·lar"
                            u", NO podem treure el producte de la cistella"))

            if pro == '0':   #si el usuari es consumidor i prove de la pantalla de comanda principal

                # entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__gte=now)).order_by('-data_comanda')
                # comandes = Comanda.objects.filter(entregas__in=entregas).distinct()
                days = cistella(request.user)

                messages.success(request, (u"Comanda desada correctament"))

                return render(request, "romani/consumidors/comandes.html",{'comandes': days, 'up': user_p })

            elif pro == '1':  #si el usuari es productor i esta introduint comandes que li han arribat de fora la web

                productes = Producte.objects.filter(productor=comanda.format.productor)
                object_list = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__gte=now)
                productors = Productor.objects.filter(responsable=request.user)
                
                messages.success(request, (u"Comanda desada correctament"))
                
                return render(request, "romani/productors/comanda_list.html", {'object_list': object_list, 'productor': comanda.format.productor, 'productors': productors})

        except:
            messages.warning(request, (u"Hem trobat errors en el formulari"))
            pass

    return render(request, "dies_comanda.html",
                  {'comanda': comanda, 'up': user_p, 'dies_entrega_pos': dies_entrega_possibles,
                   'dies_entrega_ini': dies_entrega_ini, 'entregas_pas': entregas_pas })



# Formulari que permet votar les entregues rebudes per l'usuari a "entregas.html"
class VoteFormView(FormView):
    form_class = VoteForm
    success_url="/entregas/"

    # def create_response(self, vdict=dict(), valid_form=True):
    #     response = HttpResponse(json.dumps(vdict))
    #     response.status = 200 if valid_form else 500
    #     return response

    def form_valid(self, form):
        user = self.request.user
        if form.data["entrega"]!="":
            entrega = get_object_or_404(Entrega, pk=int(form.data["entrega"]))
            if form.data["vote"]=="Up":
                v = Vote.objects.get(voter=user, entrega=entrega)
                v.positiu = True
                v.text = form.data["text"]
                v.save()
                messages.success(self.request, (u"Hem rebut la teva valoració. Gràcies"))
            elif form.data["vote"]=="Down":
                v = Vote.objects.get(voter=user, entrega=entrega)
                v.positiu = False
                v.text = form.data["text"]
                v.save()
                messages.success(self.request, (u"Hem rebut la teva valoració. Gràcies"))
            elif form.data["vote"]=="NewUp":
                v = Vote.objects.create(voter=user, entrega=entrega, positiu=True, text=form.data["text"])
                messages.success(self.request, (u"Hem rebut la teva valoració. Gràcies"))
            elif form.data["vote"]=="NewDown":
                v = Vote.objects.create(voter=user, entrega=entrega, positiu=False, text=form.data["text"])
                messages.success(self.request, (u"Hem rebut la teva valoració. Gràcies"))
            else:
                pass
        ret = {"success": 1}
        return super(VoteFormView, self).form_valid(form)





