__author__ = 'sergi'

from django.shortcuts import render, get_object_or_404
from .models import Producte, Productor, Comanda, Contracte, TipusProducte, Node, DiaEntrega, FranjaHoraria, Frequencia
from django.db.models import Q
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from .models import UserProfile, Etiqueta, Adjunt
from .forms import ComandaForm,ContracteForm

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

    etiquetes = []

    for e in etiquetes_pre:
        for p in e.producte_set.all():
            for p2 in p.dies_entrega.all():
                if p2 in dies_node_entrega:
                    etiquetes.append(e)
                    break
            break


    if not searchString == 0:
        posts = Producte.objects.filter((Q(nom__icontains = searchString) | Q(descripcio__icontains = searchString) | Q(keywords__icontains = searchString)),
                                        nodes__id__exact=user_p.lloc_entrega_perfil.pk, esgotat=False, dies_entrega__in = dies_node_entrega ).distinct()

        productes = sorted(posts, key=lambda a: a.karma(), reverse=True)

        return render(request, "buscador.html", {
            'posts': productes,
            'etiquetes': etiquetes, 'up': user_p})
    else:
        return render(request, "buscador.html", {
            'etiquetes': etiquetes, 'up': user_p})



def coopeView(request):

    user_p = UserProfile.objects.filter(user=request.user).first()

    dies_node_entrega = user_p.lloc_entrega_perfil.dies_entrega.filter(date__gt = datetime.datetime.now())

    etiquetes_pre = Etiqueta.objects.all()

    etiquetes = []

    for e in etiquetes_pre:
        for p in e.producte_set.all():
            for p2 in p.dies_entrega.all():
                if p2 in dies_node_entrega:
                    etiquetes.append(e)
                    break
            break

    nodes = Node.objects.all()


    # productes = Producte.objects.filter(nodes__id__exact=user_p.lloc_entrega_perfil.pk, esgotat=False).order_by(karma descending)


    p = Producte.objects.filter(esgotat=False, dies_entrega__in = dies_node_entrega ).distinct()



    productes = sorted(p, key=lambda a: a.karma(), reverse=True)

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

    return render(request, "productes.html", {'productes':products,'etiquetes': etiquetes, 'up': user_p, 'nodes': nodes})


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

    etiquetes = []

    for e in etiquetes_pre:
        for p in e.producte_set.all():
            for p2 in p.dies_entrega.all():
                if p2 in dies_node_entrega:
                    etiquetes.append(e)
                    break
            break

    p = Producte.objects.filter(etiqueta=etiqueta, nodes__id__exact=user_p.lloc_entrega_perfil.pk, esgotat=False, dies_entrega__in = dies_node_entrega ).distinct()

    productes = sorted(p, key=lambda a: a.karma(), reverse=True)

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
    # productes = Producte.objects.filter(productor=productor)

    user_p = UserProfile.objects.filter(user=request.user).first()

    dies_node_entrega = user_p.lloc_entrega_perfil.dies_entrega.filter(date__gt = datetime.datetime.now())

    p = Producte.objects.filter(productor=productor, esgotat=False, dies_entrega__in = dies_node_entrega ).distinct()

    adjunts = Adjunt.objects.filter(productor=productor)

    productes = sorted(p, key=lambda a: a.karma(), reverse=True)


    return render(request, "productor.html",{'productor': productor, 'productes': productes, 'adjunts': adjunts})

def comandesView(request):

    now = datetime.datetime.now()
    comandes = Comanda.objects.filter(client=request.user).filter(Q(dia_entrega__date__gte=now)|Q(dia_entrega__date__isnull=True)).order_by('-data_comanda')
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__gte=now)|Q(data_fi__isnull=True)).order_by('-data_comanda')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "comandes.html",{'comandes': comandes, 'nodes': nodes,'contractes':contractes, 'up': user_p })


def entregasView(request):

    now = datetime.datetime.now()
    entregas = Comanda.objects.filter(client=request.user).filter(Q(dia_entrega__date__lte=now)).order_by('dia_entrega__date')
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__lte=now) & Q(data_fi__isnull=False)).order_by('data_fi')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "entregas.html",{'comandes': entregas, 'contractes': contractes, 'nodes': nodes, 'up': user_p})

def comandaDelete(request, pk):

    comandaDel = Comanda.objects.filter(pk=pk).first()

    time = timedelta(hours=48)
    tt = comandaDel.dia_entrega__date - time
    if datetime.datetime.date(datetime.datetime.now()) < tt.date():
        notify.send(comandaDel.producte, recipient = request.user,  verb="Has tret ",
            description="de la cistella" , url=comandaDel.producte.adjunt.url, timestamp=timezone.now())
        comandaDel.delete()
    else:
        messages.error(request, (u"Falten menys de 48h, no podem treure el producte de la cistella"))

    comandes = Comanda.objects.filter(client=request.user).filter(Q(dia_entrega__date__gte=datetime.datetime.now())|Q(dia_entrega__date__isnull=True)).order_by('-data_comanda')
    now = datetime.datetime.now()
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__gte=now)|Q(data_fi__isnull=True)).order_by('-data_comanda')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()



    return render(request, "comandes.html",{'comandes': comandes, 'contractes': contractes, 'nodes': nodes, 'up': user_p})

def contracteDelete(request, pk):

    contracteDel = Contracte.objects.filter(pk=pk).first()

    notify.send(contracteDel.producte, recipient = request.user,  verb="Has tret ",
          description="de la cistella" , url=contracteDel.producte.adjunt.url, timestamp=timezone.now())

    contracteDel.data_fi = datetime.datetime.now()
    contracteDel.save()

    comandes = Comanda.objects.filter(client=request.user).filter(Q(dia_entrega__date__gte=datetime.datetime.now())|Q(dia_entrega__date__isnull=True)).order_by('-data_comanda')
    now = datetime.datetime.now()
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__gte=now)|Q(data_fi__isnull=True)).order_by('-data_comanda')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()


    return render(request, "comandes.html",{'comandes': comandes, 'contractes': contractes, 'nodes': nodes, 'up': user_p})


class ContracteUpdateView(UpdateView):
    model = Contracte
    form_class = ContracteForm
    success_url="/comandes/"
    template_name = "romani/consumidors/contracte_form.html"






def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)




def prox_calc(producte, node, dia_entrega, franja, frequencia):

        d = dia_entrega.date
        d_list = []
        next_val = True
        d_list.append(dia_entrega)

        if frequencia.num == 1:
            while(next_val):
                d = next_weekday(d, int(dia_entrega.dia_num()))
                try:
                    s = DiaEntrega.objects.get(date=d, node=node, franjes_horaries__id__exact=franja.id, productes__id__exact=producte.pk)
                    d_list.append(s)
                except:
                    return d_list
        if frequencia.num == 2:
            while(next_val):
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                try:
                    s = DiaEntrega.objects.get(date=d.date, node=node, franjes_horaries__id__exact=franja.id, productes__id__exact=producte.pk)
                    d_list.append(s)
                except:
                    return d_list

        if frequencia.num == 3:
            while(next_val):
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                d = next_weekday(d, int(dia_entrega.dia_num()))
                try:
                    s = DiaEntrega.objects.get(date=d.date, node=node, franjes_horaries__id__exact=franja.id, productes__id__exact=producte.pk)
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
                    s = DiaEntrega.objects.get(date=d.date, node=node, franjes_horaries__id__exact=franja.id, productes__id__exact=producte.pk)
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
        freq_txt = freq.nom
        data_entrega = DiaEntrega.objects.get(pk=data)
        # DiaEntrega.objects.filter(date__gt=data_entrega.date)
        # data_entrega_txt = data_entrega.dia()
        # data_entrega_num = data_entrega.dia_num()
        franja_pk = form.data["franjes"]
        franja = FranjaHoraria.objects.get(pk=franja_pk)

        format.stock = format.stock - int(cantitat)
        format.save()

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
            v = Comanda.objects.create(client=user, producte=producte, cantitat=cantitat, format=format, dia_entrega=data_entrega, franja_horaria=franja, lloc_entrega=lloc_obj, preu=preu)

            ret = {"contracte": 0, "success": 1}

        else:

            dies_entrega = prox_calc(producte, lloc_obj, data_entrega, franja, freq)

            v = Contracte.objects.create(client=user, producte=producte, cantitat=cantitat, format=format, franja_horaria=franja, lloc_entrega=lloc_obj, preu=preu, freq_txt=freq_txt, frequencia=frequencia)

            ret = {"contracte": 1, "success": 1, "pk": v.pk}

            for d in dies_entrega:
                v.dies_entrega.add(d)

        # ret = {"success": 1}
        notify.send(producte, recipient= user, verb="Has afegit ", action_object=v,
                  description="a la cistella" , timestamp=timezone.now())

        messages.success(self.request, (u"Comanda realitzada correctament"))


        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)



class ComandaFormView(JSONFormMixin, ComandaFormBaseView):
    pass



