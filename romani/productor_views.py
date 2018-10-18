__author__ = 'sergi'

from romani.models import Comanda, Productor, Producte, DiaEntrega, TipusProducte, DiaProduccio, Stock, DiaFormatStock, Node, Entrega
from romani.forms import Adjunt, AdjuntForm, ProductorForm, ProducteForm, TipusProducteForm, DiaProduccioForm, StockForm, DiaFormatStockForm, ComandaProForm

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView, DetailView
from django.contrib import messages

from django.contrib.auth.models import Group

from django.shortcuts import render, get_object_or_404, redirect
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.utils import timezone
from notifications import notify

import xlwt
import datetime


def dis_export_comandes_xls(request, pk):
    response = HttpResponse(content_type='application/ms-excel')

    dia = DiaEntrega.objects.get(pk=pk)
    nom = str(dia.node.nom) + str(dia.date)

    productors = Productor.objects.filter(responsable=request.user)
    productes = Producte.objects.filter(productor__in=productors)

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
    rows = Entrega.objects.filter(dia_entrega__pk=pk, comanda__format__producte__in=productes).order_by('comanda__client').values_list('comanda__client__first_name', 'comanda__format__producte__nom', 'comanda__cantitat', 'comanda__format__nom', 'comanda__preu')
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
    rows = de.totals_productors_propis(request.user)
    rows.sort(key=lambda rw: rw[0])
    for row in rows:
        old_row=row[0]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    # messages.success(request, (u"S'ha descarregat el arxiu correctament"))
    wb.save(response)
    return response

def pro_export_comandes_xls(request, pro, pk):
    response = HttpResponse(content_type='application/ms-excel')

    dia = DiaEntrega.objects.get(pk=pk)
    nom = str(dia.node.nom) + str(dia.date)

    productor = Productor.objects.filter(pk=pro)
    productes = Producte.objects.filter(productor=productor)

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
    rows = Entrega.objects.filter(dia_entrega__pk=pk, comanda__format__producte__in=productes).order_by('comanda__client').values_list('comanda__client__first_name', 'comanda__format__producte__nom', 'comanda__cantitat', 'comanda__format__nom', 'comanda__preu')
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


    # messages.success(request, (u"S'ha descarregat el arxiu correctament"))
    wb.save(response)
    return response


class ComandesListView(ListView):
    # model = Comanda
    template_name = "romani/productors/comanda_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        return Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__gte=datetime.datetime.today()).order_by('-data_comanda')

    def get_context_data(self, **kwargs):
        context = super(ComandesListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        # context["contractes"] = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

class HistorialListView(ListView):
    # model = Comanda
    template_name = "romani/productors/historial_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        return Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__lte=datetime.datetime.today())

    def get_context_data(self, **kwargs):
        context = super(HistorialListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        productes = Producte.objects.filter(productor=productor)
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        # context["contractes"] = Contracte.objects.filter(producte__in=productes)
        return context

class ProductesListView(ListView):
    model = Producte
    template_name = "romani/productors/producte_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        return Producte.objects.filter(productor=productor, status=True)

    def get_context_data(self, **kwargs):
        context = super(ProductesListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        context["formats"] = TipusProducte.objects.filter(productor=productor)
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context


class CoopsListView(ListView):
    model = Node
    template_name = "romani/productors/coops.html"

    def get_queryset(self):
        return Productor.objects.filter(responsable=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CoopsListView, self).get_context_data(**kwargs)
        nodes = Node.objects.exclude(pk=1)
        context["nodes"] = nodes
        return context

class TipusProducteCreateView(CreateView):
    model = TipusProducte
    form_class = TipusProducteForm
    template_name = "romani/productors/format.html"

    def get_form_kwargs(self):
        kwargs = super(TipusProducteCreateView, self).get_form_kwargs()
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        kwargs["productor"] = productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TipusProducteCreateView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(TipusProducteCreateView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, (u"S'ha desat el nou format"))
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        return "/pro/" + str(productor.pk) + "/vista_productes/"


class TipusProducteUpdateView(UpdateView):
    model = TipusProducte
    form_class = TipusProducteForm
    template_name = "romani/productors/format.html"

    def get_form_kwargs(self):
        kwargs = super(TipusProducteUpdateView, self).get_form_kwargs()
        tipusproducte = TipusProducte.objects.get(pk=self.kwargs['pk'])
        kwargs["productor"] = tipusproducte.productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TipusProducteUpdateView, self).get_context_data(**kwargs)
        tipusproducte = TipusProducte.objects.get(pk=self.kwargs['pk'])
        context["productor"] = tipusproducte.productor
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(TipusProducteUpdateView, self).form_invalid(form)

    def get_success_url(self):
        # messages.success(self.request, (u"S'han desat les modificacions en el format"))
        p = TipusProducte.objects.get(pk=self.kwargs['pk'])
        pro_id = p.productor_id
        messages.success(self.request, (u"Format desat correctament"))
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
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(AdjuntCreateView, self).form_invalid(form)

    def get_success_url(self):
        # messages.success(self.request, (u"S'ha carregat la nova foto a l'àlbum del productor"))
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        messages.success(self.request, (u"Fotografia afegida a l'àlbum del productor"))
        return "/pro/" + str(productor.pk) + "/adjunts"


def adjuntsProductor(request, pro):

    productors = Productor.objects.filter(responsable=request.user)
    productor = Productor.objects.get(pk=pro)
    if productor in productors:
        adjunts = Adjunt.objects.filter(productor__pk=pro)
        return render(request, "romani/productors/fotos_productor.html",
                      {'adjunts': adjunts, 'productor': productor, 'productors': productors})
    else:
        messages.error(request, (u"Hi ha hagut un error. No tens permissos "
                                      u"per gestionar fotos d'aquest productor"))
        return render(request, "romani/productors/fotos_productor.html",
                      {'productor': productor, 'productors': productors})







def adjuntDelete(request, pk):

    productors = Productor.objects.filter(responsable=request.user)

    fotoDelete = Adjunt.objects.get(pk=pk)
    if fotoDelete.productor in productors:
        adjunts = Adjunt.objects.filter(productor=fotoDelete.productor)
        fotoDelete.delete()
        return render(request, "romani/productors/fotos_productor.html",
                      {'adjunts': adjunts, 'productor': fotoDelete.productor, 'productors': productors})
    else:
        messages.error(request, (u"Hi ha hagut un error. No tens permissos "
                                      u"per gestionar fotos d'aquest productor"))
        return render(request, "romani/productors/fotos_productor.html",
                      {'productor': fotoDelete.productor, 'productors': productors})






class ComandaCreateView(CreateView):

    model = Comanda
    form_class = ComandaProForm
    template_name = "romani/productors/comanda_form.html"

    def get_form_kwargs(self):
        kwargs = super(ComandaCreateView, self).get_form_kwargs()
        productor = Productor.objects.get(responsable=self.request.user, pk=self.kwargs['pro'])
        kwargs["productor"] = productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ComandaCreateView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(responsable=self.request.user, pk=self.kwargs['pro'])
        context["productor"] = productor
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(ComandaCreateView, self).form_invalid(form)

    def form_valid(self, form):
        form_valid = super(ComandaCreateView, self).form_valid(form)
        obj = form.save(commit=False)
        obj.externa = True
        # obj.lloc_entrega = form_valid.instance.dia_entrega.node
        # obj.producte = form_valid.instance.format.producte
        obj.save()
        return form_valid

    def get_success_url(self):
        # if self.object.frequencia.num > 0:
        # messages.success(self.request, (u"Comanda creada correctament"))
        return "/dies_entrega/" + str(self.object.pk) + "/1"
        # else:
        #     productor = Productor.objects.get(pk=self.kwargs['pro'])
        #     return "/pro/" + str(productor.pk) + "/vista_comandes/"



class ProductorsListView(ListView):
    model = Productor
    template_name = "romani/productors/productor_list.html"

    def get_queryset(self):
        g = Group.objects.get(name='Productors')
        u = self.request.user
        if not u in g.user_set.all():
            g.user_set.add(u)
        return Productor.objects.filter(responsable=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProductorsListView, self).get_context_data(**kwargs)
        productors = Productor.objects.filter(responsable=self.request.user)
        productes = Producte.objects.filter(productor__in=productors)
        # context["contractes"] = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True)
        context["comandes"] = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__gte=datetime.datetime.today()).order_by('-data_comanda')
        return context


class ProductorsCalListView(ListView):
    model = Productor
    template_name = "romani/productors/productor_list_cal.html"

    def get_queryset(self):
        g = Group.objects.get(name='Productors')
        u = self.request.user
        if not u in g.user_set.all():
            g.user_set.add(u)
        return Productor.objects.filter(responsable=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super(ProductorsCalListView, self).get_context_data(**kwargs)
    #     # productors = Productor.objects.filter(responsable=self.request.user)
    #     # productes = Producte.objects.filter(productor__in=productors)
    #     # context["contractes"] = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True)
    #     # context["comandes"] = Comanda.objects.filter(producte__in=productes, dia_entrega__date__gte=datetime.datetime.today())
    #     # context["user"] = self.request.user
    #     return context
class ProductorsHistListView(ListView):
    model = Productor
    template_name = "romani/productors/productor_list_hist.html"

    def get_queryset(self):
        g = Group.objects.get(name='Productors')
        u = self.request.user
        if not u in g.user_set.all():
            g.user_set.add(u)
        return Productor.objects.filter(responsable=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProductorsHistListView, self).get_context_data(**kwargs)
        productors = Productor.objects.filter(responsable=self.request.user)
        productes = Producte.objects.filter(productor__in=productors)
        # context["contractes"] = Contracte.objects.filter(producte__in=productes)
        comandes = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__lte=datetime.datetime.today())
        context["comandes"] = comandes
        preu_total = 0
        cant_total = 0
        for c in comandes:
            preu_total += c.comanda.preu
            cant_total += c.comanda.cantitat
        context["preu_total"]=preu_total
        context["cant_total"]=cant_total
        return context

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
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

def DiaEntregaDistribuidorView(request, dataentrega):

    # Trobem el objecte DataEntrega a partir de l'identificador pk
    diaentrega = DiaEntrega.objects.get(pk=dataentrega)
    # Calculem els productors lligats a l'usuari (distribuidor) per a informar la vista i la template quan surti del dia d'entrega
    productors_menu = Productor.objects.filter(responsable=request.user)
    # Calculem els productors controlats per l'usuari distribuidor que són acceptats en el dia d'entrega per a no mostrarli els que estan exclosos en el node del dia d'entrega seleccionat
    productors = Productor.objects.filter(responsable=request.user, nodes=diaentrega.node)
    # Seleccionem tots els possibles formats que podrien ser seleccionats pel productor per portarlos en el dia d'entrega seleccionat
    formats = TipusProducte.objects.filter(producte__productor__in=productors, producte__status=True)
    # Filtrem les comandes lligades al dia d'entrega
    comandes = Entrega.objects.filter(comanda__format__productor__in=productors, dia_entrega=diaentrega)
    #Calculem el total del dia per a cada un dels productors de la distribuidora
    totals_productors = diaentrega.totals_productors_propis(request.user)
    # Calculem el total del dia per a cada un dels productes de la distribuidora
    totals_productes = diaentrega.totals_productes_propis(request.user)
    # Calculem els totals (cantitat total i preu total) de les comandes lligades a aquest dia d'entrega
    preu_total = 0
    cant_total = 0
    for c in comandes:
        preu_total += c.comanda.preu
        cant_total += c.comanda.cantitat
    # Seleccionem tots els productes que ja estan confirmats pel productor o distribuidor com disponibles en el dia d'entrega
    diaformatstock = DiaFormatStock.objects.filter(dia=diaentrega, format__productor__in=productors, format__producte__status=True)
    if diaformatstock:
        # Si anteriorment ja s'havia seleccionat afirmativament el tipus d'stock d'algun format del productor per a aquest dia d'entrega...                                                                                             SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
        f_lst = []
        for d in diaformatstock:
            # Guardem tots els stocks de formats ja seleccionats afirmativament en sessions anteriors
            f_lst.append(d.format)
        for f in formats:
            if f in f_lst:
                # Si el stock del format ja ha estat introdüit, el treiem de la llista general. Per a així tenir 2 llistes: una amb els formats ja seleccionats i una altra amb els no seleccionats
                formats = formats.exclude(pk=f.pk)
        # Generem 1r el ModelFormSet indicant el objecte de referència, els camps extres que hi haurà a més dels que aporti el queryset i també li passem el formulari
        FormatStockFormset = modelformset_factory(DiaFormatStock, extra=len(formats), form=DiaFormatStockForm)
        # Ja creat el ModelFormSet li donem la queryset que omplirà els camps ordinaris, i a través d'un loop li passem els paràmetres que apareixeran en els camps extraordinaris
        formatstockform = FormatStockFormset(queryset=diaformatstock, initial=[{'format': x, 'dia':diaentrega, 'hores_limit':x.productor.hores_limit} for x in formats])
    else:
        # Si cap stock de format havia estat seleccionat prèviament, 1r creem el ModelFormSet, i a continuació, a través d'un loop informem el FormSet dels paràmetres inicials a mostrar
        FormatStockFormset = formset_factory(DiaFormatStockForm, extra=0)
        formatstockform = FormatStockFormset(initial=[{'format': x, 'dia':diaentrega, 'hores_limit':x.productor.hores_limit} for x in formats])

    if request.POST:
        # Recollim els formats seleccionats afirmativament per l'usuari
            formats_pk = request.POST.getlist('formats')
            formset = FormatStockFormset(request.POST)
            # Llista per guardar els formats el vincle dels quals amb el dia d'entrega ha d'afegir-se el registre a DiaFormatStock
            formats_crt = []
            # Llista per guardar els formats el vincle dels quals amb el dia d'entrega ha de modificarse en el registre corresponent a DiaFormatStock
            formats_mod = []
            # Llista per guardar els formats el vincle dels quals amb el dia d'entrega ha de borrarse el registre a DiaFormatStock
            formats_del = []
            if formset.is_valid():
                for f in formset:
                   cd = f.cleaned_data
                   format = cd.get('format')
                   tipus_stock = cd.get('tipus_stock')
                   hores_limit = cd.get('hores_limit')
                   if str(format.pk) in formats_pk:
                       # Si s'ha seleccionat afirmativament el format...
                       try:
                           s = DiaFormatStock.objects.get(dia=diaentrega, format=format)
                           # Si ja existia l'afegim a la llista de registres de DiaFormatStock a modificar
                           old_frmt={}
                           old_frmt['dia']=diaentrega
                           old_frmt['format']=format
                           old_frmt['tipus_stock']=tipus_stock
                           old_frmt['hores_limit']=hores_limit
                           formats_mod.append(old_frmt)
                           # s[0].tipus_stock = tipus_stock
                           # s[0].save()
                       except:
                           # Si no existia l'afegim a la llista de diccionaris que representen registres de DiaFormatStock a crear
                           new_frmt={}
                           new_frmt['dia'] = diaentrega
                           new_frmt['format'] = format
                           new_frmt['tipus_stock'] = tipus_stock
                           new_frmt['hores_limit']=hores_limit
                           formats_crt.append(new_frmt)
                   else:
                       # Si el format està deseleccionat...
                       try:
                           # Busquem el objecte que vincula el format amb aquest dia d'entrega
                           s = DiaFormatStock.objects.get(format=format, dia=diaentrega)
                           # Si trobem el format lligat al dia d'entrega vol dir que previament havia estat seleccionat, per tant els usuaris tenien aquest format disponible en el dia d'entrega
                           if not ((Entrega.objects.filter(comanda__format=format, dia_entrega=diaentrega))):
                                       # Si el format no té entregues solicitades pel clients l'afegim a una llista on guardem els formats que es volen retirar del dia d'entrega
                                       formats_del.append(s)
                           else:
                                   #  Si trobem que algun dels formats que intenta deseleccionar el distribuidor ja té entregues per aquest dia, aleshores no deixem que es retiri el format del dia ,d'entrega
                                   messages.error(request, (u"Ja t'han fet comandes per aquest dia, no pots cancel·lar l'entrega"))
                                   return render(request, "romani/productors/distri_diaentrega.html", {'dia': diaentrega, 'object_list': productors_menu, 'formatstockform': formatstockform,
                                                                                                       'comandes': comandes, 'preu_total': preu_total, 'cant_total': cant_total,
                                                                                                        'totals_productors': totals_productors, 'totals_productes': totals_productes})
                       except:
                           pass

                for f in formats_del:
                    f.delete()

                for f in formats_crt:
                    s = DiaFormatStock.objects.create(dia=f['dia'],format=f['format'], tipus_stock=f['tipus_stock'], hores_limit=f['hores_limit'])

                for f in formats_mod:
                    s = DiaFormatStock.objects.filter(dia=f['dia'],format=f['format']).update(tipus_stock=f['tipus_stock'], hores_limit=f['hores_limit'])


                if 'create' in request.POST:
                    messages.success(request, (u"Dia d'entrega guardat correctament"))
                    return render(request, "romani/productors/productor_list_cal.html", {'object_list': productors_menu})
                else:

                    messages.success(request, (u"Dia d'entrega guardat correctament"))
                    next_d = DiaEntrega.objects.filter(date__gte=diaentrega.date, node__productors__in=productors_menu).distinct()
                    unsorted = next_d.all()
                    # Aqui s'ha d'ordenar el queryset next_d per tal que quedi en el 1r registre el dia d'entrega seguent a editar
                    next_tab = sorted(unsorted, key = lambda obj: (obj.date, obj.franja_inici().inici))
                    aux = False

                    for n in next_tab:
                        if aux==False:
                            if n == diaentrega:
                                aux=True
                        elif aux==True:
                            return redirect('distri_data_comandes', dataentrega=n.pk)

                    return render(request, "romani/productors/productor_list_cal.html", {'object_list': productors_menu})

    return render(request, "romani/productors/distri_diaentrega.html", {'dia': diaentrega, 'object_list': productors_menu, 'formatstockform': formatstockform,
                                                                        'comandes': comandes, 'preu_total': preu_total, 'cant_total': cant_total,
                                                                        'totals_productors': totals_productors, 'totals_productes': totals_productes})




def DiaEntregaProductorView(request, pk, dataentrega):
    # Trobem els productors dels quals es responsable l'usuari per al menu
    productors = Productor.objects.filter(responsable=request.user)
    # Trobem el objecte DataEntrega a partir de l'identificador pk
    diaentrega = DiaEntrega.objects.get(pk=dataentrega)
    # Calculem el productorgestionat per l'usuari
    productor = Productor.objects.get(pk=pk)
    # Seleccionem tots els possibles formats que podrien ser seleccionats pel productor per portarlos en el dia d'entrega seleccionat
    formats = TipusProducte.objects.filter(producte__productor=productor, producte__status=True)
    # Filtrem les comandes lligades al dia d'entrega
    comandes = Entrega.objects.filter(comanda__format__productor=productor, dia_entrega=diaentrega)
    # Calculem el total del dia per a cada un dels productes de la productora
    totals_productes = diaentrega.totals_productesxproductor(pk)
    # Calculem els totals (cantitat total i preu total) de les comandes lligades a aquest dia d'entrega
    preu_total = 0
    cant_total = 0
    for c in comandes:
        preu_total += c.comanda.preu
        cant_total += c.comanda.cantitat
    # Seleccionem tots els productes que ja estan confirmats pel productor o distribuidor com disponibles en el dia d'entrega
    diaformatstock = DiaFormatStock.objects.filter(dia=diaentrega, format__productor=productor, format__producte__status=True)
    if diaformatstock:
        # Si anteriorment ja s'havia seleccionat afirmativament el tipus d'stock d'algun format del productor per a aquest dia d'entrega...                                                                                             SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
        f_lst = []
        for d in diaformatstock:
            # Guardem tots els stocks de formats ja seleccionats afirmativament en sessions anteriors
            f_lst.append(d.format)
        for f in formats:
            if f in f_lst:
                # Si el stock del format ja ha estat introdüit, el treiem de la llista general. Per a així tenir 2 llistes: una amb els formats ja seleccionats i una altra amb els no seleccionats
                formats = formats.exclude(pk=f.pk)
        # Generem 1r el ModelFormSet indicant el objecte de referència, els camps extres que hi haurà a més dels que aporti el queryset i també li passem el formulari
        FormatStockFormset = modelformset_factory(DiaFormatStock, extra=len(formats), form=DiaFormatStockForm)
        # Ja creat el ModelFormSet li donem la queryset que omplirà els camps ordinaris, i a través d'un loop li passem els paràmetres que apareixeran en els camps extraordinaris
        formatstockform = FormatStockFormset(queryset=diaformatstock, initial=[{'format': x, 'dia':diaentrega,'hores_limit':x.productor.hores_limit} for x in formats])
    else:
        # Si cap stock de format havia estat seleccionat prèviament, 1r creem el ModelFormSet, i a continuació, a través d'un loop informem el FormSet dels paràmetres inicials a mostrar
        FormatStockFormset = formset_factory(DiaFormatStockForm, extra=0)
        formatstockform = FormatStockFormset(initial=[{'format': x, 'dia':diaentrega,'hores_limit':x.productor.hores_limit} for x in formats])

    if request.POST:
        # Recollim els formats seleccionats afirmativament per l'usuari
            formats_pk = request.POST.getlist('formats')
            formset = FormatStockFormset(request.POST)
            # Llista per guardar els formats el vincle dels quals amb el dia d'entrega ha d'afegir-se el registre a DiaFormatStock
            formats_crt = []
            # Llista per guardar els formats el vincle dels quals amb el dia d'entrega ha de modificarse en el registre corresponent a DiaFormatStock
            formats_mod = []
            # Llista per guardar els formats el vincle dels quals amb el dia d'entrega ha de borrarse el registre a DiaFormatStock
            formats_del = []
            if formset.is_valid():
                for f in formset:
                   cd = f.cleaned_data
                   format = cd.get('format')
                   tipus_stock = cd.get('tipus_stock')
                   hores_limit = cd.get('hores_limit')
                   if str(format.pk) in formats_pk:
                       # Si s'ha seleccionat afirmativament el format...
                       try:
                           s = DiaFormatStock.objects.get(dia=diaentrega, format=format)
                           # Si ja existia l'afegim a la llista de registres de DiaFormatStock a modificar
                           old_frmt={}
                           old_frmt['dia']=diaentrega
                           old_frmt['format']=format
                           old_frmt['tipus_stock']=tipus_stock
                           old_frmt['hores_limit']=hores_limit
                           formats_mod.append(old_frmt)
                           # s[0].tipus_stock = tipus_stock
                           # s[0].save()
                       except:
                           # Si no existia l'afegim a la llista de diccionaris que representen registres de DiaFormatStock a crear
                           new_frmt={}
                           new_frmt['dia'] = diaentrega
                           new_frmt['format'] = format
                           new_frmt['tipus_stock'] = tipus_stock
                           new_frmt['hores_limit'] = hores_limit
                           formats_crt.append(new_frmt)
                   else:
                       # Si el format està deseleccionat...
                       try:
                           # Busquem el objecte que vincula el format amb aquest dia d'entrega
                           s = DiaFormatStock.objects.get(format=format, dia=diaentrega)
                           # Si trobem el format lligat al dia d'entrega vol dir que previament havia estat seleccionat, per tant els usuaris tenien aquest format disponible en el dia d'entrega
                           if not ((Entrega.objects.filter(comanda__format=format, dia_entrega=diaentrega))):
                                       # Si el format no té entregues solicitades pel clients l'afegim a una llista on guardem els formats que es volen retirar del dia d'entrega
                                       formats_del.append(s)
                           else:
                                   #  Si trobem que algun dels formats que intenta deseleccionar el distribuidor ja té entregues per aquest dia, aleshores no deixem que es retiri el format del dia ,d'entrega
                                   messages.error(request, (u"Ja t'han fet comandes per aquest dia, no pots cancel·lar l'entrega"))
                                   return render(request, "romani/productors/diaentrega.html", {'dia': diaentrega, 'productor': productor, 'formatstockform': formatstockform, 'productors': productors,
                                                                                                       'comandes': comandes, 'preu_total': preu_total, 'cant_total': cant_total,
                                                                        'totals_productes': totals_productes})
                       except:
                           pass

                for f in formats_del:
                    f.delete()

                for f in formats_crt:
                    s = DiaFormatStock.objects.create(dia=f['dia'],format=f['format'], tipus_stock=f['tipus_stock'], hores_limit=f['hores_limit'])

                for f in formats_mod:
                    s = DiaFormatStock.objects.filter(dia=f['dia'],format=f['format']).update(tipus_stock=f['tipus_stock'], hores_limit=f['hores_limit'])

                if 'create' in request.POST:
                    messages.success(request, (u"Dia d'entrega guardat correctament"))
                    return render(request, "romani/productors/dates_list.html", {'productor': productor, 'productors': productors})
                else:

                    messages.success(request, (u"Dia d'entrega guardat correctament"))
                    next_d = DiaEntrega.objects.filter(date__gte=diaentrega.date, node__productors=productor).distinct()
                    unsorted = next_d.all()
                    # Aqui s'ha d'ordenar el queryset next_d per tal que quedi en el 1r registre el dia d'entrega seguent a editar
                    next_tab = sorted(unsorted, key = lambda obj: (obj.date, obj.franja_inici().inici))
                    aux = False

                    for n in next_tab:
                        if aux==False:
                            if n == diaentrega:
                                aux=True
                        elif aux==True:
                            return redirect('data_comandes', pk=productor.pk, dataentrega=n.pk)

                    return render(request, "romani/productors/dates_list.html", {'productor': productor, 'productors': productors})

    return render(request, "romani/productors/diaentrega.html", {'dia': diaentrega, 'productor': productor, 'formatstockform': formatstockform, 'productors':productors,
                                                                        'comandes': comandes, 'preu_total': preu_total, 'cant_total': cant_total,
                                                                        'totals_productes': totals_productes})



from django.forms import formset_factory, modelformset_factory

def DiaProduccioCreateView(request, pro):

    productor = Productor.objects.get(pk=pro)
    productes = Producte.objects.filter(productor=productor, status=True)
    StockFormset = formset_factory(StockForm, extra=0)
    formats = TipusProducte.objects.filter(producte__in=productes)
    stockform = StockFormset(initial=[{'format': x} for x in formats])
    productors = Productor.objects.filter(responsable=request.user)

    if request.POST:

           form = DiaProduccioForm(request.POST)
           formset = StockFormset(request.POST)

           if form.is_valid() and formset.is_valid():

               try:
                   dia = request.POST.get('date')
                   caducitat = request.POST.get('caducitat')
                   node = request.POST.get('node')

                   if dia:

                       a = datetime.datetime.strptime(dia, '%d/%m/%Y').strftime('%Y-%m-%d')

                       if caducitat:
                            data_cad = datetime.datetime.strptime(caducitat, '%d/%m/%Y').strftime('%Y-%m-%d')
                            if node:
                                node_obj = Node.objects.get(pk=node)
                                dp = DiaProduccio.objects.create(date=a, productor=productor, caducitat=data_cad, node=node_obj)
                            else:
                                dp = DiaProduccio.objects.create(date=a, productor=productor, caducitat=data_cad)
                       else:
                           if node:
                                node_obj = Node.objects.get(pk=node)
                                dp = DiaProduccio.objects.create(date=a, productor=productor, node=node)
                           else:
                                dp = DiaProduccio.objects.create(date=a, productor=productor)
               except:
                   messages.warning(request, (u"Hem trobat errors en el formulari"))
                   return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productes': productes, 'productors': productors})


       # if formset.is_valid():
               for f in formset:
                   cd = f.cleaned_data
                   dia_prod = dp
                   format = cd.get('format')
                   stock_ini = cd.get('stock_ini')
                   s = Stock.objects.create(dia_prod=dia_prod, format=format, stock_ini=stock_ini )

               if 'create' in request.POST:
                   messages.success(request, (u"S'ha creat el dia de producció"))
                   return render(request, "romani/productors/dates_list.html", {'productor': productor, 'productors': productors})
               else:

                    messages.success(request, (u"S'ha creat el dia de producció"))
                    # next_d = DiaProduccio.objects.filter(date__gte=dp.date, node__productors=productor).distinct()
                    # unsorted = next_d.all()
                    # # Aqui s'ha d'ordenar el queryset next_d per tal que quedi en el 1r registre el dia d'entrega seguent a editar
                    # next_tab = sorted(unsorted, key = lambda obj: (obj.date))
                    # aux = False
                    #
                    # for n in next_tab:
                    #     if aux==False:
                    #         if n == dp:
                    #             aux=True
                    #     elif aux==True:
                    return redirect('diaproduccio_create', pro=productor.pk)

                    # return render(request, "romani/productors/dates_list.html", {'productor': productor})
           else:

               messages.warning(request, (u"Hem trobat errors en el formulari"))
               return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productes': productes, 'productors': productors})


    form = DiaProduccioForm()
    # form.fields['productor'].choices = [(x.pk, x) for x in Productor.objects.filter(pk=pro)]
    form.fields['node'].queryset = Node.objects.filter(productors__id__exact=pro)

    # form.fields['node'].initial = ''


    return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': stockform, 'productor': productor, 'productes': productes, 'productors': productors})



def DiaProduccioUpdateView(request, pro, pk):

    productor = Productor.objects.get(pk=pro)
    productors = Productor.objects.filter(responsable=request.user)
    productes = Producte.objects.filter(productor=productor, status=True)
    formats = TipusProducte.objects.filter(producte__in=productes)
    dp_obj = DiaProduccio.objects.get(pk=pk)
    stocks = Stock.objects.filter(dia_prod=dp_obj)
    StockFormset = modelformset_factory(Stock, extra=0, form=StockForm)
    stockform = StockFormset(queryset=stocks)
    entregas = Entrega.objects.filter(dia_produccio=dp_obj)
    preu_total = 0
    cant_total = 0
    for c in entregas:
        preu_total += c.comanda.preu
        cant_total += c.comanda.cantitat

    if request.POST:
           form = DiaProduccioForm(request.POST)
           formset = StockFormset(request.POST)
           if form.is_valid() and formset.is_valid():
               try:
                   prod = request.POST.getlist('formats')
                   dia = request.POST.get('date')
                   caducitat = request.POST.get('caducitat')
                   try:
                        node_pk = request.POST.get('node')
                        node = Node.objects.get(pk=node_pk)
                        dp_obj.node = node
                   except:
                        dp_obj.node = None
                   a = datetime.datetime.strptime(dia, '%d/%m/%Y').strftime('%Y-%m-%d')
                   dp_obj.date = a
                   dp_obj.productor = productor
                   b = datetime.datetime.strptime(caducitat, '%d/%m/%Y').strftime('%Y-%m-%d')
                   dp_obj.caducitat = b
                   dp_obj.save()
               except:
                   messages.warning(request, (u"Hem trobat errors en el formulari"))
                   return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productes': productes,
                                                                                  'comandes': entregas, 'preu_total': preu_total, 'cant_total': cant_total, 'productors': productors})

               for f in formset:
                   cd = f.cleaned_data
                   dia_prod = dp_obj
                   format = cd.get('format')
                   stock_ini = cd.get('stock_ini')
                   s = Stock.objects.get(pk=f.instance.pk)
                   s.dia_prod = dia_prod
                   s.format = format
                   s.stock_ini = stock_ini
                   s.save()
               if 'create' in request.POST:
                    messages.success(request, (u"S'ha desat el dia de producció"))
                    return render(request, "romani/productors/dates_list.html", {'productor': productor, 'productors':productors})
               else:
                    messages.success(request, (u"S'ha desat el dia de producció"))
                    # next_d = DiaProduccio.objects.filter(date__gte = dp_obj.date, node__productors=productor).distinct()
                    # unsorted = next_d.all()
                    # # Aqui s'ha d'ordenar el queryset next_d per tal que quedi en el 1r registre el dia d'entrega seguent a editar
                    # next_tab = sorted(unsorted, key = lambda obj: (obj.date))
                    # aux = False
                    #
                    # for n in next_tab:
                    #     if aux==False:
                    #         if n == dp_obj:
                    #             aux=True
                    #     elif aux==True:
                    #         return redirect('diaproduccio_update', pro=productor.pk, pk=n.pk)
                    #
                    return redirect('diaproduccio_create', pro=productor.pk)
                    # return render(request, "romani/productors/dates_list.html", {'productor': productor})
           else:
               messages.warning(request, (u"Hem trobat errors en el formulari"))
               return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productors':productors,
                                                                              'productes': productes, 'comandes': entregas, 'preu_total': preu_total, 'cant_total': cant_total})


    form = DiaProduccioForm()
    form.fields['date'].initial = dp_obj.date
    form.fields['node'].initial = dp_obj.node
    form.fields['caducitat'].initial = dp_obj.caducitat

    return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': stockform, 'productor': productor, 'productors':productors,
                                                                   'productes': productes, 'comandes': entregas, 'preu_total': preu_total, 'cant_total': cant_total})



class ProducteUpdateView(UpdateView):
    model = Producte
    form_class = ProducteForm
    # success_url="/vista_productes/"
    template_name = "romani/productors/producte_form.html"
    # user = request.user

    def get_form_kwargs(self):
        kwargs = super(ProducteUpdateView, self).get_form_kwargs()
        producte = Producte.objects.get(pk=self.kwargs['pk'])
        kwargs["productor"] = producte.productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProducteUpdateView, self).get_context_data(**kwargs)
        producte = Producte.objects.get(pk=self.kwargs['pk'])
        context["productor"] = producte.productor
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(ProducteUpdateView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, (u"S'ha desat el producte correctament"))
        p = Producte.objects.get(pk=self.kwargs['pk'])
        pro_id = p.productor_id
        return "/pro/" + str(pro_id) + "/vista_productes/"


class ProductorCreateView(CreateView):
    model = Productor
    form_class = ProductorForm
    template_name = "romani/productors/productor_form.html"
    success_url = "/vista_productors/"

    def get_form_kwargs(self):
        kwargs = super(ProductorCreateView, self).get_form_kwargs()
        user = self.request.user
        kwargs["user"] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductorCreateView, self).get_context_data(**kwargs)
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(ProductorCreateView, self).form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, (u"S'ha desat el productor"))
        return super(ProductorCreateView, self).form_valid(form)


class ProducteCreateView(CreateView):
    model = Producte
    form_class = ProducteForm
    template_name = "romani/productors/producte_form.html"

    def get_form_kwargs(self):
        kwargs = super(ProducteCreateView, self).get_form_kwargs()
        productor = Productor.objects.get(responsable=self.request.user, pk=self.kwargs['pro'])
        kwargs["productor"] = productor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProducteCreateView, self).get_context_data(**kwargs)
        context["productor"] = Productor.objects.get(pk=self.kwargs['pro'])
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(ProducteCreateView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, (u"S'ha creat el producte"))
        p = Productor.objects.get(pk=self.kwargs['pro'])
        return "/pro/" + str(p.pk) + "/vista_productes/"


class ProductorUpdateView(UpdateView):
    model = Productor
    form_class = ProductorForm
    # success_url="/vista_productors/"
    template_name = "romani/productors/productor_form.html"

    def get_form_kwargs(self):
        kwargs = super(ProductorUpdateView, self).get_form_kwargs()
        user = self.request.user
        kwargs["user"] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductorUpdateView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pk'])
        context["productor"] = productor
        adjunts = Adjunt.objects.filter(productor=productor)
        context["adjunts"] = adjunts
        productors = Productor.objects.filter(responsable=self.request.user)
        context["productors"] = productors
        return context

    def form_invalid(self, form):
        messages.warning(self.request, (u"Hem trobat errors en el formulari"))
        return super(ProductorUpdateView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, (u"S'ha desat el productor"))
        pro = Productor.objects.get(pk=self.kwargs['pk'])
        return "/productor/update/" + str(pro.id)



def eventsProductor(productor):
    eventList = set()
    formats = TipusProducte.objects.filter(productor=productor)

    for p in formats:
        for d in DiaEntrega.objects.filter(formats__format__id__exact=p.id):
            if d:
                eventList.add(d)
    return eventList






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
            day_str = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.inici)[:5]
            dayend = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.final)[:5]
            url = "/pro/" + str(pro) + "/data_comandes/" + str(event.pk)
            events.append({'title': event.node.nom, 'start': day_str, 'end': dayend, 'url': url })
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')

def diaEntregaSelected(request, pro):

    p = Productor.objects.get(pk=pro)
    eventList = eventsProductor(p)
    events = []
    for event in eventList:
        franja = event.franja_inici()
        day_str = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.inici)[:5]
        dayend = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.final)[:5]
        url = "/pro/" + str(pro) + "/data_comandes/" +  str(event.pk)
        events.append({'title': event.node.nom, 'start': day_str, 'end': dayend, 'url': url })
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')

def diaProdEvents(request, pro):

    p = Productor.objects.get(pk=pro)
    eventList = DiaProduccio.objects.filter(productor=p)
    events = []
    for event in eventList:
        day_str = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " 11:00"
        dayend = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " 11:00"
        url = "/pro/" + str(pro) + "/diaproduccio_update/" +  str(event.pk)
        events.append({'title': 'produccio', 'start': day_str, 'end': dayend
                          , 'url': url, 'allDay': 'true'
                       })
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')


def eventsProductors(user):
    eventList = set()
    formats = TipusProducte.objects.filter(productor__responsable=user)

    for p in formats:
        for d in DiaEntrega.objects.filter(formats__format=p):
            if d:
                eventList.add(d)

    return eventList


def distriCalendarEvents(request):

    pros_list = Productor.objects.filter(responsable=request.user)
    distribuidorAgenda = eventsProductors(request.user)
    eventList = set()
    for pros in pros_list:
        # p = Productor.objects.get(pk=pros.pk)
        d = DiaEntrega.objects.filter(node__productors=pros)
        for w in d:
            eventList.add(w)

    events = []
    for event in eventList:
        if event not in distribuidorAgenda:
            franja = event.franja_inici()
            day_str = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.inici)[:5]
            dayend = str(event.date.year) + "-" + str(event.date.month).zfill(2) + "-" + str(event.date.day).zfill(2) + " " + str(franja.final)[:5]
            url = "/pro/distri_dia/" + str(event.pk)
            events.append({'title': event.node.nom, 'start': day_str, 'end': dayend
                              , 'url': url
                           })
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')


def distriCalendarSelected(request):

    # pros_list = Productor.objects.filter(responsable=request.user)
    eventList = eventsProductors(request.user)
    # for pros in pros_list:
    #     p = Productor.objects.get(pk=pros.pk)
    events = []
    for event in eventList:
        franja = event.franja_inici()
        day_str = str(event.date.year) + "-" + str(event.date.month).zfill(2)  + "-" + str(event.date.day).zfill(2)  + " " + str(franja.inici)[:5]
        dayend = str(event.date.year) + "-" + str(event.date.month).zfill(2)  + "-" + str(event.date.day).zfill(2)  + " " + str(franja.final)[:5]
        url = "/pro/distri_dia/" + str(event.pk)
        events.append({'title': event.node.nom, 'start': day_str, 'end': dayend
                          , 'url': url
                       })
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')


# Funció per borrar comandes per part de l'usuari. Comprovem que el productor no hagi començat a elaborar el producte solicitat
def producteDelete(request, pk):

    producteDel = Producte.objects.get(pk=pk)


    dia = datetime.datetime.now()

    if request.user in producteDel.productor.responsable.all():
        if not Comanda.objects.filter(format__producte=producteDel, entregas__dia_entrega__date__gte=datetime.datetime.today()):
            notify.send(producteDel, recipient = request.user,  verb="Has borrat ", action_object=producteDel,
                description="de lamassa.org" , timestamp=timezone.now())
            # url=comandaDel.format.producte.foto.url,
            producteDel.status = False
            producteDel.save()
            messages.info(request, (u"Has borrat el producte"))
        else:
            messages.error(request, (u"Tens comandes d'aquest producte per entregar en el futur"))
    else:
        messages.error(request, (u"No ets responsable d'aquest productor"))
    productes = Producte.objects.filter(productor=producteDel.productor, status=True)
    productors = Productor.objects.filter(responsable=request.user)

    return render(request, "romani/productors/producte_list.html", {'object_list': productes,'productor': producteDel.productor, 'productors': productors})

from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import io
import matplotlib.pyplot as plt
from django.db.models import Count

def graphView(request, pro):
    f = Figure()
    buf = io.BytesIO()
    ax = f.add_subplot(211)
    des = DiaEntrega.objects.filter(date__lte=datetime.date.today()).order_by('date')

    totals = []
    for d in des:
        totals.append(d.total())

    des_v = des.values('date')
    # totals = list(map(lambda d: d['entregas'], des))
    dates = list(map(lambda d: d['date'], des_v))



    # x = np.arange(-2, 3, .01)
    # y = np.sin(np.exp(2 * x))
    # ax.title = "Dates"
    ax.plot(dates, totals)
    # f.title = pro
    canvas = FigureCanvas(f)

    f.savefig(buf, format='png')
    # plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

def productorGraphView(request, pro):
    f = Figure()
    buf = io.BytesIO()
    # ax = f.add_subplot(211)
    productor = Productor.objects.get(pk=pro)
    des = DiaEntrega.objects.filter(date__lte=datetime.date.today(), formats__format__productor=productor).order_by('date')

    nodes = set()



    totals = []
    for d in des:
        totals.append(d.total_productor(pro))
        # totals2.append(d.total())

    for x in des:
        nodes.add(x.node)

    des_v = des.values('date')
    # totals = list(map(lambda d: d['entregas'], des))
    dates = list(map(lambda d: d['date'], des_v))
    # ax.set_title(productor.nom)
    # ax.set_xlabel('Dies d entrega')
    # ax.set_ylabel('Ingrés')
    # ax.plot(dates, totals , '.-')

    nodes_in = []
    ax2 = f.add_subplot(111)
    for p in nodes:
        totals2 = []
        dates2 = []
        d = des.filter(node=p)
        zotal = 0
        for r in d:
            dates2.append(r.date)
            totals2.append(r.total_productor(pro))
            zotal += r.total_productor(pro)
        if zotal > 0:
            ax2.plot(dates2, totals2, '.-')
            nodes_in.append(p)
    ax2.legend(nodes_in)
    ax2.set_title(productor.nom)

    f.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5,
                    wspace=0.35)

    canvas = FigureCanvas(f)
    f.savefig(buf, format='png')
    # plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

def graphProductorView(request, pro):

    productor = Productor.objects.get(pk=pro)
    # Trobem els productors dels quals es responsable l'usuari per al menu
    productors = Productor.objects.filter(responsable=request.user)

    return render(request, "romani/productors/graph_productor.html", {'productor': productor, 'productors': productors})