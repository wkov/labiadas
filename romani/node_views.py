__author__ = 'sergi'

from .models import Node, DiaEntrega, FranjaHoraria, Comanda, Contracte
from .forms import NodeForm, NodeProductorsForm, FranjaHorariaForm, DiaEntregaForm

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView




class NodesListView(ListView):
    model = Node
    template_name = "romani/nodes/node_list.html"

    def get_queryset(self):
        return Node.objects.filter(responsable=self.request.user)


class NodesDatesListView(ListView):
    model = Node
    template_name = "romani/nodes/nodedates_list.html"

    def get_queryset(self):
        return Node.objects.get(pk=self.kwargs['dis'])

    def get_context_data(self, **kwargs):
        context = super(NodesDatesListView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['dis'])
        context["node"] = node
        return context


class NodeComandesListView(ListView):
    model = Comanda
    template_name = "romani/nodes/nodecomanda_list.html"

    def get_queryset(self):
        diaentrega = DiaEntrega.objects.get(pk=self.kwargs["pk"])
        return Comanda.objects.filter(lloc_entrega=diaentrega.node, dia_entrega=diaentrega)

    def get_context_data(self, **kwargs):
        context = super(NodeComandesListView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['dis'])
        context["node"] = node
        diaentrega = DiaEntrega.objects.get(pk=self.kwargs["pk"])
        context["contractes"] = Contracte.objects.filter(dies_entrega__id__exact=diaentrega.id)
        return context


class FranjaHorariaCreateView(CreateView):

    model = FranjaHoraria
    form_class = FranjaHorariaForm
    # success_url = "/vista_nodesdates/"
    template_name = "romani/nodes/franjahoraria_form.html"

    def get_form_kwargs(self):
        kwargs = super(FranjaHorariaCreateView, self).get_form_kwargs()
        node = Node.objects.get(responsable=self.request.user, pk=self.kwargs['dis'])
        kwargs['node'] = node
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(FranjaHorariaCreateView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['dis'])
        context["node"] = node
        return context

    def get_success_url(self):
        node = Node.objects.get(pk=self.kwargs['dis'])
        return "/dis/" + str(node.pk) + "/diaentrega/create/"



class DiaEntregaCreateView(CreateView):
    model = DiaEntrega
    form_class = DiaEntregaForm
    # success_url = "/vista_nodesdates/"
    template_name = "romani/nodes/diaentrega_form.html"

    def get_form_kwargs(self):
        kwargs = super(DiaEntregaCreateView, self).get_form_kwargs()
        node = Node.objects.get(responsable=self.request.user, pk=self.kwargs['dis'])
        kwargs['node'] = node
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DiaEntregaCreateView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['dis'])
        context["node"] = node
        return context

    def get_success_url(self):
        node = Node.objects.get(pk=self.kwargs['dis'])
        return "/dis/" + str(node.pk) + "/vista_nodesdates/"

    # def form_valid(self, form):
    #     f = form.save(commit=False)
    #     f.save()
    #     return super(DiaEntregaCreateView, self).form_valid(form)


class NodeUpdateView(UpdateView):
    model = Node
    form_class = NodeForm
    # success_url="/vista_nodes/"
    template_name = "romani/nodes/node_form.html"

    def get_success_url(self):
        node = Node.objects.get(pk=self.kwargs['pk'])
        return "/dis/" + str(node.pk) + "/vista_nodesdates/"



class NodeProductorsUpdateView(UpdateView):
    model = Node
    form_class = NodeProductorsForm
    template_name = "romani/nodes/nodeproductors_form.html"
    success_url="dis/(?P<dis>\d+)/vista_nodesdates/"

    def get_success_url(self):
        node = Node.objects.get(pk=self.kwargs['pk'])
        return "/dis/" + str(node.pk) + "/vista_nodesdates/"










import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse


def diaNodeEvents(request, dis):
    # productor = Productor.objects.filter(responsable=request.user)
    # eventList = DiaEntrega.objects.filter(date__gte=datetime.datetime.now(), node__productors__id__exact=productor)
    p = Node.objects.get(pk=dis)
    eventList = DiaEntrega.objects.filter(node=p)
    events = []
    for event in eventList:
            franja = event.franja_inici()
            day_str = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.inici)[:5]
            dayend = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.final)[:5]
            url = "/dis/" + str(dis) + "/node_comandes/" + str(event.pk)
            events.append({'title': event.node.nom, 'start': day_str, 'end': dayend, 'url': url })
    # something similar for owned events, maybe with a different className if you like
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')