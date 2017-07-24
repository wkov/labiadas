__author__ = 'sergi'

from django.shortcuts import render, get_object_or_404
from romani.models import Producte, Productor, Comanda, TipusProducte, Node, DiaEntrega, FranjaHoraria, Frequencia, DiaProduccio, Vote, Entrega, Stock
from django.db.models import Q
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from romani.models import UserProfile, Etiqueta, Adjunt
from romani.forms import ComandaForm, VoteForm
# from romani.views import stock_calc

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

    dies_node_entrega = user_p.lloc_entrega_perfil.dies_entrega.filter(date__gt = datetime.datetime.now())

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

        for d in dies_node_entrega:
            for t in TipusProducte.objects.filter(dies_entrega__dia=d):
                date = datetime.datetime.now() + timedelta(hours=t.productor.hores_limit)
                aux = d.franja_inici()
                daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
                if daytime > date:
                    stock_result = stock_check_cant(t, d, 1)
                    if stock_result:
                        prod_aux.add(t.producte.pk)

        p = Producte.objects.filter((Q(nom__icontains = searchString) | Q(descripcio__icontains = searchString) | Q(keywords__icontains = searchString)),
                                        esgotat=False, pk__in=prod_aux).distinct()

        productes = sorted(p, key=lambda a: a.karma(user_p.lloc_entrega_perfil), reverse=True)

        return render(request, "buscador.html", {
            'posts': productes,
            'etiquetes': etiquetes, 'up': user_p})
    else:
        return render(request, "buscador.html", {
            'etiquetes': etiquetes, 'up': user_p})



def coopeView(request):

    user_p = UserProfile.objects.filter(user=request.user).first()

    today = datetime.date.today()

    dies_node_entrega = user_p.lloc_entrega_perfil.dies_entrega.filter(date__gt = today)

    etiquetes_pre = Etiqueta.objects.all()

    etiquetes = set()

    for e in etiquetes_pre:
        for p in e.producte_set.all():
            for f in p.formats.all():
                for p2 in f.dies_entrega.all():
                    if p2.dia in dies_node_entrega:
                        etiquetes.add(e)
                        break

    nodes = Node.objects.all()


    prod_aux = set()

    for d in dies_node_entrega:
        for t in TipusProducte.objects.filter(dies_entrega__dia=d):
            date = datetime.datetime.now() + timedelta(hours=t.productor.hores_limit)
            aux = d.franja_inici()
            daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                stock_result = stock_check_cant(t, d, 1)
                if stock_result:
                    prod_aux.add(t.producte.pk)

    p = Producte.objects.filter(pk__in=prod_aux).distinct()


    productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega_perfil), reverse=True)

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

    return render(request, "productes.html", {'productes':products, 'etiquetes': etiquetes, 'nodes':nodes, 'up': user_p})


def producteView(request,pk):

    producte = Producte.objects.filter(pk=pk).first()
    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()
    return render(request, "producte.html",{'producte': producte, 'nodes': nodes, 'up': user_p})

def etiquetaView(request,pk):

    # etiquetes = Etiqueta.objects.all()
    etiqueta = Etiqueta.objects.filter(pk=pk).first()

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()


    dies_node_entrega = user_p.lloc_entrega_perfil.dies_entrega.filter(date__gt = datetime.datetime.now())


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

    for d in dies_node_entrega:
        for t in TipusProducte.objects.filter(dies_entrega__dia=d, producte__etiqueta=etiqueta):
            date = datetime.datetime.now() + timedelta(hours=t.productor.hores_limit)
            aux = d.franja_inici()
            daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                stock_result = stock_check_cant(t, d, 1)
                if stock_result:
                    prod_aux.add(t.producte.pk)



    p = Producte.objects.filter(pk__in=prod_aux).distinct()


    productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega_perfil), reverse=True)

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

    return render(request, "etiqueta.html",{'productes': products, 'etiquetes': etiquetes, 'etiqueta': etiqueta, 'nodes': nodes, 'up': user_p})


def productorView(request,pk):

    productor = Productor.objects.filter(pk=pk).first()
    user_p = UserProfile.objects.filter(user=request.user).first()
    dies_node_entrega = user_p.lloc_entrega_perfil.dies_entrega.filter(date__gt = datetime.datetime.now())
    p = Producte.objects.filter(productor=productor, formats__dies_entrega__dia__in = dies_node_entrega ).distinct()
    adjunts = Adjunt.objects.filter(productor=productor)
    productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega_perfil), reverse=True)

    return render(request, "productor.html",{'productor': productor, 'productes': productes, 'adjunts': adjunts, 'up': user_p})

def comandesView(request):

    now = datetime.datetime.now()
    entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__gte=now)).order_by('-data_comanda')
    comandes = Comanda.objects.filter(entregas=entregas).distinct()
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "comandes.html",{'comandes': comandes, 'up': user_p })


def entregasView(request):

    now = datetime.datetime.now()
    entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__lte=now)).order_by('dia_entrega__date')
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






def comandaDelete(request, pk):

    comandaDel = Comanda.objects.filter(pk=pk).first()
    message = ""

    dia = datetime.datetime.now() + timedelta(hours=comandaDel.format.productor.hores_limit)
    prox_entrega = comandaDel.prox_entrega()
    dia_prox_entrega = prox_entrega.dia_entrega
    aux = dia_prox_entrega.franja_inici()
    daytime = datetime.datetime(dia_prox_entrega.date.year, dia_prox_entrega.date.month, dia_prox_entrega.date.day, aux.inici.hour, aux.inici.minute)
    # tt = comandaDel.dia_entrega.date - time
    if daytime > dia:
        notify.send(comandaDel.format.producte, recipient = request.user,  verb="Has tret ",
            description="de la cistella" , url=comandaDel.format.producte.foto.url, timestamp=timezone.now())
        comandaDel.delete()
    else:

        message = u"El productor ja t'està preparant la comanda, no podem treure el producte de la cistella"

    now = datetime.datetime.now()
    entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__gte=now)).order_by('-data_comanda')
    comandes = Comanda.objects.filter(entregas=entregas).distinct()
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "comandes.html",{'comandes': comandes, 'up': user_p , 'message': message})




def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)




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


class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response



class ComandaFormBaseView(FormView):
    form_class = ComandaForm


    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    # def get_success_url(self):
    #     return reverse("comandes")

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
        # DiaEntrega.objects.filter(date__gt=data_entrega.date)
        # data_entrega_txt = data_entrega.dia()
        # data_entrega_num = data_entrega.dia_num()
        franja_pk = form.data["franjes"]
        franja = FranjaHoraria.objects.get(pk=franja_pk)



        lloc = form.data["lloc_entrega"]
        lloc_obj = get_object_or_404(Node, pk = lloc)
        # user_profile.lloc_entrega_perfil = lloc_obj
        # Aqui esta hardcodejat els llocs que son "a domicili", s'ha d'introduir el pk en el if de qualsevol node nou "a domicili"
        if (lloc_obj.a_domicili == True):

            user_profile.carrer = form.data["carrer"]
            user_profile.numero = form.data["numero"]
            user_profile.pis = form.data["pis"]
            user_profile.poblacio = form.data["poblacio"]
        user_profile.save()



        if frequencia == '0':
            stock_result = stock_calc(format, data_entrega, cantitat)
            # format.stock_fix = format.stock_fix - int(cantitat)
            # format.save()
            if stock_result['result'] == True:
                v = Comanda.objects.create(client=user, cantitat=cantitat, format=format, node=lloc_obj, preu=preu, frequencia=freq)
                if stock_result['dia_prod'] == '':
                    e = Entrega.objects.create(dia_entrega=data_entrega, comanda=v, franja_horaria=franja)
                else:
                    e = Entrega.objects.create(dia_entrega=data_entrega, comanda=v, franja_horaria=franja, dia_produccio=stock_result['dia_prod'] )
                ret = {"contracte": 0, "success": 1}
                notify.send(format, recipient= user, verb="Has afegit ", action_object=v,
                description="a la cistella" , timestamp=timezone.now())
                messages.success(self.request, (u"Comanda realitzada correctament"))
            else:
                ret = {"contracte": 0, "success": 0}
                messages.error(self.request, (u"Disculpa, NO disposem de la cantitat sol·licitada."))

        else:

            dies_entrega = prox_calc(format, lloc_obj, data_entrega, franja, freq)

            error = 0

            v = Comanda.objects.create(client=user, cantitat=cantitat, format=format, node=lloc_obj, preu=preu, frequencia=freq)

            for d in dies_entrega:
                stock_result = stock_calc(format, d, cantitat)
                if stock_result['result'] == True:
                    if stock_result['dia_prod'] == '':
                        e = Entrega.objects.create(dia_entrega=d, comanda=v, franja_horaria=franja)
                    else:
                        e = Entrega.objects.create(dia_entrega=d, comanda=v, franja_horaria=franja, dia_produccio=stock_result['dia_prod'] )
                else:
                    error = error + 1

            if error > 0:
                messages.error(self.request, (u"Disculpa, en algun dels dies seleccionats s'acaba d'esgotar el estoc disponible del producte"))
                ret = {"contracte": 0, "success": 0}
            else:
                messages.success(self.request, (u"Comanda realitzada correctament"))
                ret = {"contracte": 1, "success": 1, "pk": v.pk}
                notify.send(producte, recipient= user, verb="Has afegit ", action_object=v,
                description="a la cistella" , timestamp=timezone.now())

        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)



class ComandaFormView(JSONFormMixin, ComandaFormBaseView):
    pass


def diesEntregaView(request, pk, pro):

    now = datetime.datetime.now()
    comanda = Comanda.objects.get(pk=pk)
    user_p = UserProfile.objects.filter(user=request.user).first()
    date = datetime.datetime.now() + timedelta(hours=int(comanda.format.productor.hores_limit))

    # Llistat de dies futurs en que es posible demanar noves entregues de la comanda
    pk_lst = set()
    for d in DiaEntrega.objects.filter(date__gte=date, formats__format__id__exact=comanda.format.id, node=comanda.node).order_by('date'):
        aux = d.franja_inici()
        daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
        if daytime > date:
            stock_result = stock_check_cant(comanda.format, d, comanda.cantitat)
            if stock_result:
                pk_lst.add(d.pk)

    # Llistat de dies futurs en que ja ha demanat rebre producte
    pk2_lst = set()
    for d in Entrega.objects.filter(comanda=comanda, dia_entrega__node=comanda.node, dia_entrega__date__gte=date).order_by('dia_entrega__date'):
        aux = d.dia_entrega.franja_inici()
        daytime = datetime.datetime(d.dia_entrega.date.year, d.dia_entrega.date.month, d.dia_entrega.date.day, aux.inici.hour, aux.inici.minute)
        if daytime > date:
            pk2_lst.add(d.dia_entrega.pk)

    dies_entrega_possibles = DiaEntrega.objects.filter((Q(pk__in=pk_lst)|Q(pk__in=pk2_lst))).order_by('date')

    dies_entrega_ini = DiaEntrega.objects.filter(pk__in=pk2_lst)


    # Llistat de dies passats en que te entregues de la mateixa comanda
    pk3_lst = set()
    for d in Entrega.objects.filter(comanda=comanda, dia_entrega__node=comanda.node, dia_entrega__date__lte=date).order_by('dia_entrega__date'):
        aux = d.dia_entrega.franja_inici()
        daytime = datetime.datetime(d.dia_entrega.date.year, d.dia_entrega.date.month, d.dia_entrega.date.day, aux.inici.hour, aux.inici.minute)
        if daytime < date:
            pk3_lst.add(d.dia_entrega.pk)

    dies_entrega_pas = DiaEntrega.objects.filter(pk__in=pk3_lst).exclude(pk__in=pk_lst)


    if request.POST:
        try:
            dies_pk = request.POST.getlist('dies')
            for d in dies_pk:
                dia = DiaEntrega.objects.get(pk=d)
                if dia in dies_entrega_ini:
                    pass
                else:
                    stock_result = stock_calc(comanda.format, dia, comanda.cantitat)
                    if stock_result['result'] == True:
                        franja_pk = request.POST.get(str(dia.pk))
                        franja = FranjaHoraria.objects.get(pk=franja_pk)
                        if stock_result['dia_prod'] == '':
                            e = Entrega.objects.create(dia_entrega=dia, comanda=comanda, franja_horaria=franja)
                        else:
                            e = Entrega.objects.create(dia_entrega=dia, comanda=comanda, franja_horaria=franja, dia_produccio=stock_result['dia_prod'] )

            for d in dies_entrega_ini:
                if str(d.pk) not in dies_pk:
                    entrega = Entrega.objects.get(comanda=comanda, dia_entrega=d)
                    entrega.delete()

            if pro == '0':   #si el usuari es consumidor i prove de la pantalla de comanda principal

                entregas = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__gte=now)).order_by('-data_comanda')
                comandes = Comanda.objects.filter(entregas=entregas).distinct()

                return render(request, "comandes.html",{'comandes': comandes, 'up': user_p })

            elif pro == '1':  #si el usuari es productor i esta introduint comandes que li han arribat de fora la web

                productes = Producte.objects.filter(productor=comanda.format.productor)
                object_list = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__gte=now)

                return render(request, "romani/productors/comanda_list.html", {'object_list': object_list, 'productor': comanda.format.productor})

        except:
            pass

    return render(request, "dies_comanda.html",{'comanda': comanda, 'up': user_p, 'dies_entrega_pos': dies_entrega_possibles, 'dies_entrega_ini': dies_entrega_ini, 'dies_entrega_pas': dies_entrega_pas })




class VoteFormView(FormView):
    form_class = VoteForm
    success_url="/entregas/"

    def form_valid(self, form):

        user = self.request.user

        if form.data["entrega"]!="":
            entrega = get_object_or_404(Entrega, pk=int(form.data["entrega"]))
            if self.request.POST.get("Up"):
                v = Vote.objects.get(voter=user, entrega=entrega)
                v.positiu = True
                v.save()
            elif self.request.POST.get("Down"):
                v = Vote.objects.get(voter=user, entrega=entrega)
                v.positiu = False
                v.save()
            elif self.request.POST.get("NewUp"):
                v = Vote.objects.create(voter=user, entrega=entrega, positiu=True)
            elif self.request.POST.get("NewDown"):
                v = Vote.objects.create(voter=user, entrega=entrega, positiu=False)
            else:
                pass

        ret = {"success": 1}
        return super(VoteFormView, self).form_valid(form)



def stock_check_cant(format, dia, cantitat):
     # Comprova que hi hagi stock per a una quantitat determinada
     d = format.dies_entrega.get(dia=dia)
     if d.tipus_stock == '0':
            try:
                stocks = Stock.objects.filter((Q(dia_prod__node=dia.node)|Q(dia_prod__node=None)), dia_prod__date__lte=dia.date, dia_prod__caducitat__gte=dia.date, format=format).order_by('dia_prod__node','dia_prod__caducitat','dia_prod__date')
                for s in stocks:
                    diaproduccio = s.dia_prod
                    s = format.stocks.get(dia_prod=diaproduccio)
                    num = int(s.stock()) - int(cantitat)
                    if num >= 0:
                        return True
                return False

            except:
                    return False

     elif d.tipus_stock == '2':
            return True



def stock_calc(format, dia, cantitat):
     # Comproba que hi hagi stock i resta les unitats corresponents
     d = format.dies_entrega.get(dia=dia)
     if d.tipus_stock == '0':
            try:
                stocks = Stock.objects.filter(dia_prod__date__lte=dia.date, dia_prod__caducitat__gte=dia.date, format=format).order_by('dia_prod__caducitat','dia_prod__date')
                for s in stocks:
                    diaproduccio = s.dia_prod
                    s = format.stocks.get(dia_prod=diaproduccio)
                    num = int(s.stock()) - int(cantitat)
                    if num >= 0:
                       dict = {'result': True, 'dia_prod': diaproduccio}
                       return dict

                dict = {'result': False, 'dia_prod': ''}
                return dict

            except:
                dict = {'result': False, 'dia_prod': ''}
                return dict

     elif d.tipus_stock == '2':
            dict = {'result': True, 'dia_prod': ''}
            return dict



