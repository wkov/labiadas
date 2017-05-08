__author__ = 'sergi'

from .models import Comanda, Productor, Producte, Contracte, DiaEntrega, TipusProducte
from .forms import Adjunt, AdjuntForm, ProductorDiaEntregaForm, ProductorForm, ProducteForm, TipusProducteForm

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView

from django.shortcuts import render, get_object_or_404

import datetime

class ComandesListView(ListView):
    model = Comanda
    template_name = "romani/productors/comanda_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        return Comanda.objects.filter(producte__in=productes, dia_entrega__date__gte=datetime.datetime.today())

    def get_context_data(self, **kwargs):
        context = super(ComandesListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        context["contractes"] = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        return context

# class DataComandesListView(ListView):
#     model = Comanda
#     template_name = "romani/productors/datacomandes_list.html"
#
#     def get_queryset(self):
#         diaentrega = DiaEntrega.objects.filter(pk=self.kwargs["pk"]).first()
#         productor = Productor.objects.get(pk=self.kwargs['pro'])
#         productes = Producte.objects.filter(productor=productor)
#         return Comanda.objects.filter(producte__in=productes, dia_entrega=diaentrega)
#
#     def get_context_data(self, **kwargs):
#         context = super(DataComandesListView, self).get_context_data(**kwargs)
#         productor = Productor.objects.get(pk=self.kwargs['pro'])
#         context["productor"] = productor
#         productes = Producte.objects.filter(productor=productor)
#         diaentrega = DiaEntrega.objects.get(pk=self.kwargs["pk"]).first()
#         context["contractes"] = Contracte.objects.filter(producte__in=productes, dies_entrega__id__exact=diaentrega )
#         return context



class HistorialListView(ListView):
    model = Comanda
    template_name = "romani/productors/historial_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        return Comanda.objects.filter(producte__in=productes, dia_entrega__date__lte=datetime.datetime.today())

    def get_context_data(self, **kwargs):
        context = super(HistorialListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        productes = Producte.objects.filter(productor=productor)
        context["contractes"] = Contracte.objects.filter(producte__in=productes)

        return context

    # def get_context_data(self, **kwargs):
    #     context = super(HistorialListView, self).get_context_data(**kwargs)
    #     productor = Productor.objects.filter(responsable=self.request.user).first()
    #     context["productor"] = productor
    #     return context

class ProductesListView(ListView):
    model = Producte
    template_name = "romani/productors/producte_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        return Producte.objects.filter(productor=productor)

    def get_context_data(self, **kwargs):
        context = super(ProductesListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        context["formats"] = TipusProducte.objects.filter(productor=productor)
        return context

class LlocsListView(ListView):
    model = Producte
    template_name = "romani/productors/llocsentrega.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        return Producte.objects.filter(productor=productor)

    def get_context_data(self, **kwargs):
        context = super(LlocsListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        return context
        context["nodes"] = Node.objects.filter()

# class LlocsUpdateView(UpdateView):
#     model = Producte
#     form_class = LlocsForm
#     template_name = "romani/productors/llocsentrega_form.html"
#     success_url="/vista_llocs/"
#     # user = request.user
#
#     def get_context_data(self, **kwargs):
#         context = super(LlocsUpdateView, self).get_context_data(**kwargs)
#         productors = Productor.objects.filter(responsable=self.request.user)
#         context["productors"] = productors
#         return context

class TipusProducteCreateView(CreateView):

    model = TipusProducte
    form_class = TipusProducteForm
    template_name = "romani/productors/format.html"

    def get_form_kwargs(self):
        kwargs = super(TipusProducteCreateView, self).get_form_kwargs()
        producte = Producte.objects.get(productor__responsable=self.request.user, pk=self.kwargs['pro'])
        kwargs["productor"] = producte.productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TipusProducteCreateView, self).get_context_data(**kwargs)
        producte = Producte.objects.get(productor__responsable=self.request.user, pk=self.kwargs['pro'])
        context["productor"] = producte.productor
        return context

    def get_success_url(self):
        producte = Producte.objects.get(pk=self.kwargs['pro'])
        return "/producte/update/" + str(producte.pk)


class TipusProducteUpdateView(UpdateView):
    model = TipusProducte
    form_class = TipusProducteForm
    # success_url="/vista_productes/"
    template_name = "romani/productors/format.html"
    # user = request.user

    def get_form_kwargs(self):
        kwargs = super(TipusProducteUpdateView, self).get_form_kwargs()
        tipusproducte = TipusProducte.objects.get(pk=self.kwargs['pk'])
        kwargs["productor"] = tipusproducte.productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TipusProducteUpdateView, self).get_context_data(**kwargs)
        tipusproducte = TipusProducte.objects.get(pk=self.kwargs['pk'])
        context["productor"] = tipusproducte.productor
        return context

    def get_success_url(self):
        p = TipusProducte.objects.get(pk=self.kwargs['pk'])
        pro_id = p.productor_id
        return "/pro/" + str(pro_id) + "/vista_productes/"


class AdjuntCreateView(CreateView):

    model = Adjunt
    form_class = AdjuntForm
    template_name = "romani/productors/adjunt.html"

    def get_form_kwargs(self):
        kwargs = super(AdjuntCreateView, self).get_form_kwargs()
        productor = Productor.objects.get(responsable=self.request.user, pk=self.kwargs['pro'])
        kwargs["productor"] = productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AdjuntCreateView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(responsable=self.request.user, pk=self.kwargs['pro'])
        context["productor"] = productor
        return context

    def get_success_url(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        return "/productor/update/" + str(productor.pk)



class ProductorsListView(ListView):
    model = Productor
    template_name = "romani/productors/productor_list.html"

    def get_queryset(self):
        return Productor.objects.filter(responsable=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super(ProductorsListView, self).get_context_data(**kwargs)
    #     productor = Productor.objects.filter(responsable=self.request.user).first()
    #     context["productor"] = productor
    #     return context

class DatesListView(ListView):
    model = Producte
    template_name = "romani/productors/dates_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        return Producte.objects.filter(productor=productor)

    def get_context_data(self, **kwargs):
        context = super(DatesListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(DatesListView, self).get_context_data(**kwargs)
    #     productor = Productor.objects.filter(responsable=self.request.user).first()
    #     context["productor"] = productor
    #     return context

# class NodesHistorialListView(ListView):
#     model = Node
#     template_name = "romani/nodes/nodehistorial_list.html"
#
#     def get_queryset(self):
#         return Node.objects.get(pk=self.kwargs['dis'])
#
#     def get_context_data(self, **kwargs):
#         context = super(NodesHistorialListView, self).get_context_data(**kwargs)
#         node = Node.objects.get(pk=self.kwargs['dis'])
#         context["node"] = node
#         return context

def DiaEntregaProductorView(request, pk, dataentrega):

    productor = Productor.objects.get(pk=pk)
    diaentrega = DiaEntrega.objects.get(pk=dataentrega)


    if request.POST:

           form=ProductorDiaEntregaForm(request.POST)

           try:
               prod = request.POST.getlist('productes')

               productes_dia = []
               for d in prod:
                   aux = Producte.objects.get(pk=d)
                   if aux:
                       productes_dia.append(aux)



               productes = Producte.objects.filter(productor=productor)
               for p in productes:
                   if p not in productes_dia:
                       if p in diaentrega.productes.all():
                           if not Comanda.objects.filter(producte=p, dia_entrega=diaentrega):
                                diaentrega.productes.remove(p)
                           else:
                               message = (u"Ja t'han fet comandes per aquest dia, no pots cancel·lar l'entrega")
                               productes_sel = Producte.objects.filter(dies_entrega__id__exact=diaentrega.id)
                               comandes = Comanda.objects.filter(producte__in=productes, dia_entrega=diaentrega)
                               contractes = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True, dies_entrega__id__exact=diaentrega.id)
                               return render(request, "romani/productors/diaentrega.html", {'form': form, 'dia': diaentrega, 'productor': productor, 'productes': productes,
                                                                 'productes_sel': productes_sel, 'comandes': comandes, 'contractes': contractes, 'message': message})


               for dp in productes_dia:
                   if dp not in diaentrega.productes.all():
                       diaentrega.productes.add(dp)
           except:
               productes = Producte.objects.filter(productor=productor)
               for p in productes:
                   if p in diaentrega.productes.all():
                       diaentrega.productes.remove(p)

           return render(request, "romani/productors/dates_list.html", {'productor': productor})


    productes = Producte.objects.filter(productor=productor)

    productes_sel = Producte.objects.filter(dies_entrega__id__exact=diaentrega.id)

    comandes = Comanda.objects.filter(producte__in=productes, dia_entrega=diaentrega)

    contractes = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True, dies_entrega__id__exact=diaentrega.id)

    form=ProductorDiaEntregaForm()

    form.fields['productes'].choices = [(x.pk, x) for x in Producte.objects.filter(productor=productor)]

    form.fields['productes'].label = "Productes que portaras el dia d entrega"

    return render(request, "romani/productors/diaentrega.html", {'form': form, 'dia': diaentrega, 'productor': productor, 'productes': productes,
                                                                 'productes_sel': productes_sel, 'comandes': comandes, 'contractes': contractes})


# class DiaEntregaProductorView(FormView):
#     # model = Productor
#     form_class = ProductorDiaEntregaForm
#     success_url = "/vista_productors/"
#     template_name = "romani/productors/diaentrega.html"
#
#     def get_object(self, queryset=None):
#         return Productor.objects.get(pk=self.kwargs['pk'])
#
#     def get_context_data(self, **kwargs):
#         context = super(DiaEntregaProductorView, self).get_context_data(**kwargs)
#         productor = Productor.objects.get(pk=self.kwargs['pk'])
#         context["productor"] = productor
#         return context
class ProducteUpdateView(UpdateView):
    model = Producte
    form_class = ProducteForm
    # success_url="/vista_productes/"
    template_name = "romani/productors/producte_form.html"
    # user = request.user

    def get_context_data(self, **kwargs):
        context = super(ProducteUpdateView, self).get_context_data(**kwargs)
        producte = Producte.objects.get(pk=self.kwargs['pk'])
        context["productor"] = producte.productor
        return context

    def get_success_url(self):
        p = Producte.objects.get(pk=self.kwargs['pk'])
        pro_id = p.productor_id
        return "/pro/" + str(pro_id) + "/vista_productes/"

class ProductorUpdateView(UpdateView):
    model = Productor
    form_class = ProductorForm
    # success_url="/vista_productors/"
    template_name = "romani/productors/productor_form.html"

    # def get_form_kwargs(self):
    #     kwargs = super(ProductorUpdateView, self).get_form_kwargs()
    #     productor = Productor.objects.get(responsable=self.request.user, pk=self.kwargs['pro'])
    #     kwargs["productor"] = productor
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductorUpdateView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pk'])
        context["productor"] = productor
        adjunts = Adjunt.objects.filter(productor=productor)
        context["adjunts"] = adjunts
        return context

    def get_success_url(self):
        pro = Productor.objects.get(pk=self.kwargs['pk'])
        return "/pro/" + str(pro.id) + "/vista_dates/"



def eventsProductor(productor):
    # productor = Productor.objects.filter(responsable=user)
    eventList = set()
    productes = Producte.objects.filter(productor=productor)

    for p in productes:
        for d in DiaEntrega.objects.filter(productes__id__exact=p.id):
            if d:
                eventList.add(d)

    return eventList




import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse


def diaEntregaEvents(request, pro):
    # productor = Productor.objects.filter(responsable=request.user)
    # eventList = DiaEntrega.objects.filter(date__gte=datetime.datetime.now(), node__productors__id__exact=productor)
    p = Productor.objects.get(pk=pro)
    eventList = DiaEntrega.objects.filter(node__productors__id__exact=p.id)
    productorAgenda = eventsProductor(p)
    events = []
    for event in eventList:
        if event not in productorAgenda:
            franja = event.franja_inici()
            day_str = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.inici)[:5]
            dayend = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.final)[:5]
            url = "/pro/" + str(pro) + "/data_comandes/" + str(event.pk)
            events.append({'title': event.node.nom, 'start': day_str, 'end': dayend, 'url': url })
    # something similar for owned events, maybe with a different className if you like
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')

def diaEntregaSelected(request, pro):

    p = Productor.objects.get(pk=pro)
    eventList = eventsProductor(p)
    events = []
    for event in eventList:
        franja = event.franja_inici()
        day_str = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.inici)[:5]
        dayend = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.final)[:5]
        url = "/pro/" + str(pro) + "/data_comandes/" +  str(event.pk)
        events.append({'title': event.node.nom, 'start': day_str, 'end': dayend, 'url': url })
    # something similar for owned events, maybe with a different className if you like
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')