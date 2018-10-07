__author__ = 'sergi'

from romani.models import Node, DiaEntrega, FranjaHoraria, Comanda, Entrega
from romani.forms import NodeForm, NodeProductorsForm, FranjaHorariaForm, DiaEntregaForm

from django.contrib.auth.models import Group, User
from django.contrib import messages

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic import ListView

import xlwt
# from itertools import chain

def export_comandes_xls(request, pk):
    response = HttpResponse(content_type='application/ms-excel')

    dia = DiaEntrega.objects.get(pk=pk)
    nom = str(dia.node.nom) + str(dia.date)

    # aux =  'attachment; filename="' +   nom + nom
    response['Content-Disposition'] = 'attachment; filename="comandes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')



    ws = wb.add_sheet(nom)
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nom', 'Producte', 'Cantitat', 'Format', 'Preu', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    old_row = ""
    total = ""
    rows = Entrega.objects.filter(dia_entrega__pk=pk).order_by('comanda__client').values_list('comanda__client__first_name', 'comanda__format__producte__nom', 'comanda__cantitat', 'comanda__format__nom', 'comanda__preu')
    rows = list(rows)
    rows.sort(key=lambda tup: tup[0])
    for row in rows:
        if row[0]!=old_row:
            row_num += 1
            ws.write(row_num, col_num, total, font_style)
            total = 0
        old_row=row[0]
        total = row[4] + total
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    row_num += 1
    ws.write(row_num, col_num, total, font_style)

    row_num += 2
    de = DiaEntrega.objects.get(pk=pk)
    rows = de.totals_productors()
    rows.sort(key=lambda rw: rw[0])
    for row in rows:
        old_row=row[0]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)






    # messages.success(request, (u"S'ha descarregat el arxiu correctament"))
    wb.save(response)
    return response


class NodesListView(ListView):
    model = Node
    template_name = "romani/nodes/node_list.html"

    # def get_queryset(self):
    #     g = Group.objects.get(name='Nodes')
    #     u = self.request.user
    #     if not u in g.user_set.all():
    #             g.user_set.add(u)
    #     return Node.objects.filter(responsable=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(NodesListView, self).get_context_data(**kwargs)
        g = Group.objects.get(name='Nodes')
        u = self.request.user
        if not u in g.user_set.all():
                g.user_set.add(u)
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context


class NodesDatesListView(ListView):
    model = Node
    template_name = "romani/nodes/nodedates_list.html"

    def get_queryset(self):
        return Node.objects.get(pk=self.kwargs['dis'])

    def get_context_data(self, **kwargs):
        context = super(NodesDatesListView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['dis'])
        context["node"] = node
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context


class NodeComandesListView(ListView):
    # model = Comanda
    template_name = "romani/nodes/nodecomanda_list.html"

    def get_queryset(self):
        diaentrega = DiaEntrega.objects.get(pk=self.kwargs["pk"])
        return Entrega.objects.filter(dia_entrega=diaentrega)

    def get_context_data(self, **kwargs):
        context = super(NodeComandesListView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['dis'])
        context["node"] = node
        diaentrega = DiaEntrega.objects.get(pk=self.kwargs["pk"])
        context["diaentrega"] = diaentrega
        context['formats'] = diaentrega.formats.all()
            # Calculem els totals (cantitat total i preu total) de les comandes lligades a aquest dia d'entrega
        preu_total = 0
        for c in self.get_queryset():
            preu_total += c.comanda.preu
        context["preu_total"] = preu_total
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context


class FranjaHorariaCreateView(CreateView):

    model = FranjaHoraria
    form_class = FranjaHorariaForm
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
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context

    def get_success_url(self):
        messages.success(self.request, (u"S'ha creat correctament la franja horària"))
        node = Node.objects.get(pk=self.kwargs['dis'])
        return "/dis/" + str(node.pk) + "/diaentrega/create/"



class DiaEntregaCreateView(CreateView):
    model = DiaEntrega
    form_class = DiaEntregaForm
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
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context

    def get_success_url(self):
        messages.success(self.request, (u"S'ha creat correctament el dia d'entrega"))
        node = Node.objects.get(pk=self.kwargs['dis'])
        if 'create' in self.request.POST:
            return "/dis/" + str(node.pk) + "/vista_nodesdates/"
        else:
            return "/dis/" + str(node.pk) + "/diaentrega/create/"

class DiaEntregaUpdateView(UpdateView):
    model = DiaEntrega
    form_class = DiaEntregaForm
    template_name = "romani/nodes/diaentrega_form.html"

    def get_form_kwargs(self):
        kwargs = super(DiaEntregaUpdateView, self).get_form_kwargs()
        d = DiaEntrega.objects.get(pk=self.kwargs['pk'])
        kwargs['node'] = d.node
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DiaEntregaUpdateView, self).get_context_data(**kwargs)
        d = DiaEntrega.objects.get(pk=self.kwargs['pk'])
        context["node"] = d.node
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context

    def get_success_url(self):
        messages.success(self.request, (u"S'han desat les modificacions"))
        d = DiaEntrega.objects.get(pk=self.kwargs['pk'])
        return "/dis/" + str(d.node.pk) + "/node_comandes/" + str(d.pk)


class NodeCreateView(CreateView):
    model = Node
    form_class = NodeForm
    template_name = "romani/nodes/node_form.html"
    success_url = "/vista_nodes/"

    def get_form_kwargs(self):
        kwargs = super(NodeCreateView, self).get_form_kwargs()
        user = self.request.user
        kwargs["user"] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NodeCreateView, self).get_context_data(**kwargs)
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context


    def form_valid(self, form):
        messages.success(self.request, (u"S'ha creat correctament el lloc d'entrega"))
    #     f = form.save(commit=False)
    #     g = Group.objects.get(name='Nodes')
    #
    #     for r in form.data["responsable"]:
    #         u = User.objects.get(pk=r)
    #         if not u in g.user_set.all():
    #             g.user_set.add(u)
    #     f.save()
        return super(NodeCreateView, self).form_valid(form)


class NodeUpdateView(UpdateView):
    model = Node
    form_class = NodeForm
    template_name = "romani/nodes/node_form.html"


    def get_form_kwargs(self):
        kwargs = super(NodeUpdateView, self).get_form_kwargs()
        user = self.request.user
        kwargs["user"] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(NodeUpdateView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['pk'])
        context["node"] = node
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context

    def get_success_url(self):
        messages.success(self.request, (u"S'han desat les modificacions"))
        node = Node.objects.get(pk=self.kwargs['pk'])
        return "/dis/" + str(node.pk) + "/vista_nodesdates/"

    # def form_valid(self, form):
    #     f = form.save(commit=False)
    #     g = Group.objects.get(name='Nodes')
    #
    #     for r in form.data["responsable"]:
    #         u = User.objects.get(pk=r)
    #         if not u in g.user_set.all():
    #             g.user_set.add(u)
    #     f.save()
    #     return super(NodeUpdateView, self).form_valid(form)


class NodeProductorsUpdateView(UpdateView):
    model = Node
    form_class = NodeProductorsForm
    template_name = "romani/nodes/nodeproductors_form.html"
    success_url="dis/(?P<dis>\d+)/vista_nodesdates/"

    def get_success_url(self):
        messages.success(self.request, (u"S'ha desat la llista de productors"))
        node = Node.objects.get(pk=self.kwargs['pk'])
        return "/dis/" + str(node.pk) + "/vista_nodesdates/"

    def get_context_data(self, **kwargs):
        context = super(NodeProductorsUpdateView, self).get_context_data(**kwargs)
        node = Node.objects.get(pk=self.kwargs['pk'])
        context["node"] = node
        context["nodes"] = Node.objects.filter(responsable=self.request.user)
        return context

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
            day_str = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.inici)[:5]
            dayend = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.final)[:5]
            url = "/dis/" + str(dis) + "/node_comandes/" + str(event.pk)
            events.append({'title': event.node.nom, 'start': day_str, 'end': dayend, 'url': url })
    # something similar for owned events, maybe with a different className if you like
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')