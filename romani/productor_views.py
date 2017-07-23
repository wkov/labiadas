__author__ = 'sergi'

from romani.models import Comanda, Productor, Producte, DiaEntrega, TipusProducte, DiaProduccio, Stock, DiaFormatStock, Node, Entrega
from romani.forms import Adjunt, AdjuntForm, ProductorForm, ProducteForm, TipusProducteForm, DiaProduccioForm, StockForm, DiaFormatStockForm, ComandaProForm

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView, DetailView
from django.contrib import messages

from django.contrib.auth.models import Group

from django.shortcuts import render, get_object_or_404

import datetime

class ComandesListView(ListView):
    # model = Comanda
    template_name = "romani/productors/comanda_list.html"

    def get_queryset(self):
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        return Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__gte=datetime.datetime.today())

    def get_context_data(self, **kwargs):
        context = super(ComandesListView, self).get_context_data(**kwargs)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        productes = Producte.objects.filter(productor=productor)
        # context["contractes"] = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True)
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        context["productor"] = productor
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
        # context["contractes"] = Contracte.objects.filter(producte__in=productes)
        return context

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
        return context

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
        return context

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
        return context

    def get_success_url(self):
        # messages.success(self.request, (u"S'ha carregat la nova foto a l'àlbum del productor"))
        productor = Productor.objects.get(pk=self.kwargs['pro'])
        messages.success(self.request, (u"Fotografia carregada 100%"))
        return "/productor/update/" + str(productor.pk)



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
        return context

    def form_valid(self, form):
        form_valid = super(ComandaCreateView, self).form_valid(form)
        obj = form.save(commit=False)
        obj.externa = True
        # obj.lloc_entrega = form_valid.instance.dia_entrega.node
        # obj.producte = form_valid.instance.format.producte
        obj.save()
        return form_valid

    def get_success_url(self):

        # messages.success(self.request, (u"S'ha carregat la nova foto a l'àlbum del productor"))
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
        context["comandes"] = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__gte=datetime.datetime.today())
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
        context["comandes"] = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega__date__lte=datetime.datetime.today())
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
        return context

def DiaEntregaDistribuidorView(request, dataentrega):



    diaentrega = DiaEntrega.objects.get(pk=dataentrega)
    productors_menu = Productor.objects.filter(responsable=request.user)
    productors = Productor.objects.filter(responsable=request.user, nodes=diaentrega.node)
    diaproduccio = DiaProduccio.objects.filter(date__lte=diaentrega.date, productor__in=productors).order_by('-date').first()
    formats = TipusProducte.objects.filter(producte__productor__in=productors)
    diaformatstock = DiaFormatStock.objects.filter(dia=diaentrega, format__productor__in=productors)

    if diaformatstock:
        f_lst = []
        for d in diaformatstock:
            f_lst.append(d.format)
        for f in formats:
            if f in f_lst:
                formats = formats.exclude(pk=f.pk)
        FormatStockFormset = modelformset_factory(DiaFormatStock, extra=len(formats), form=DiaFormatStockForm)
        formatstockform = FormatStockFormset(queryset=diaformatstock, initial=[{'format': x, 'dia':diaentrega} for x in formats])
    else:
        FormatStockFormset = formset_factory(DiaFormatStockForm, extra=0)
        formatstockform = FormatStockFormset(initial=[{'format': x, 'dia':diaentrega} for x in formats])

    if request.POST:
        try:
            formats_pk = request.POST.getlist('formats')
            formset = FormatStockFormset(request.POST)
            if formset.is_valid():
                for f in formset:
                   cd = f.cleaned_data
                   format = cd.get('format')
                   tipus_stock = cd.get('tipus_stock')
                   if str(format.pk) in formats_pk:
                       s = DiaFormatStock.objects.get_or_create(dia=diaentrega, format=format)
                       if s:
                           s[0].tipus_stock = tipus_stock
                           s[0].save()
                   else:
                       try:
                           s = DiaFormatStock.objects.get(format=format, dia=diaentrega)
                           if not ((Entrega.objects.filter(comanda__format=format, dia_entrega=diaentrega))):
                                       s.delete()
                           else:
                                   message = (u"Ja t'han fet comandes per aquest dia, no pots cancel·lar l'entrega")
                                   formats_sel = TipusProducte.objects.filter(dies_entrega__dia__id__exact=diaentrega.id)
                                   comandes = Entrega.objects.filter(comanda__format__in=formats, dia_entrega=diaentrega)
                                   # contractes = Contracte.objects.filter(format__in=formats, data_fi__isnull=True, dies_entrega__id__exact=diaentrega.id)
                                   return render(request, "romani/productors/distri_diaentrega.html", {'dia': diaentrega, 'productors': productors, 'formatstockform': formatstockform,
                                                                     'formats_sel': formats_sel, 'comandes': comandes, 'message': message})
                       except:
                           pass

                messages.success(request, (u"Dia d'entrega guardat correctament"))

                return render(request, "romani/productors/productor_list_cal.html", {'object_list': productors_menu})
        except:
               productes = Producte.objects.filter(productor__in=productors)
               for p in productes:
                   for f in p.formats.all():
                       s = DiaFormatStock.objects.filter(dia=diaentrega, format=f)
                       if s:
                           s.delete()

               messages.success(request, (u"Dia d'entrega guardat correctament"))

               return render(request, "romani/productors/productor_list_cal.html", {'object_list': productors_menu})

    productes = Producte.objects.filter(productor__in=productors)

    formats_sel = DiaFormatStock.objects.filter(dia=diaentrega)

    comandes = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega=diaentrega)


    return render(request, "romani/productors/distri_diaentrega.html", {'dia': diaentrega, 'productors': productors_menu, 'productes': productes, 'formatstockform': formatstockform,
                                                                 'formats_sel': formats_sel, 'comandes': comandes, 'dia_prod': diaproduccio})




def DiaEntregaProductorView(request, pk, dataentrega):

    productor = Productor.objects.get(pk=pk)
    diaentrega = DiaEntrega.objects.get(pk=dataentrega)
    diaproduccio = DiaProduccio.objects.filter(date__lte=diaentrega.date, productor=productor).order_by('-date').first()
    formats = TipusProducte.objects.filter(producte__productor=productor)
    diaformatstock = DiaFormatStock.objects.filter(dia=diaentrega, format__productor=productor)
    productes = Producte.objects.filter(productor=productor)

    if diaformatstock:
        f_lst = []
        for d in diaformatstock:
            f_lst.append(d.format)
        for f in formats:
            if f in f_lst:
                formats = formats.exclude(pk=f.pk)
        FormatStockFormset = modelformset_factory(DiaFormatStock, extra=len(formats), form=DiaFormatStockForm)
        formatstockform = FormatStockFormset(queryset=diaformatstock, initial=[{'format': x, 'dia':diaentrega} for x in formats])
    else:
        FormatStockFormset = formset_factory(DiaFormatStockForm, extra=0)
        formatstockform = FormatStockFormset(initial=[{'format': x, 'dia':diaentrega} for x in formats])

    if request.POST:
        try:
            formats_pk = request.POST.getlist('formats')
            formset = FormatStockFormset(request.POST)
            if formset.is_valid():
                for f in formset:
                   cd = f.cleaned_data
                   format = cd.get('format')
                   tipus_stock = cd.get('tipus_stock')
                   if str(format.pk) in formats_pk:
                       s = DiaFormatStock.objects.get_or_create(dia=diaentrega, format=format)
                       if s:
                           s[0].tipus_stock = tipus_stock
                           s[0].save()
                   else:
                       try:
                           s = DiaFormatStock.objects.get(format=format, dia=diaentrega)
                           if not (Entrega.objects.filter(comanda__format=format, dia_entrega=diaentrega)):
                                       s.delete()
                           else:
                                   message = (u"Ja t'han fet comandes per aquest dia, no pots cancel·lar l'entrega")
                                   formats_sel = TipusProducte.objects.filter(dies_entrega__dia__id__exact=diaentrega.id)
                                   comandes = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega=diaentrega)
                                   # contractes = Contracte.objects.filter(format__in=formats, data_fi__isnull=True, dies_entrega__id__exact=diaentrega.id)
                                   return render(request, "romani/productors/diaentrega.html", {'dia': diaentrega, 'productor': productor, 'formatstockform': formatstockform,
                                                                     'formats_sel': formats_sel, 'comandes': comandes, 'message': message})
                       except:
                           pass
                messages.success(request, (u"Dia d'entrega guardat correctament"))
                return render(request, "romani/productors/dates_list.html", {'productor': productor})
        except:
               productes_qs = Producte.objects.filter(productor=productor)
               for p in productes_qs:
                   for f in p.formats.all():
                       s = DiaFormatStock.objects.filter(dia=diaentrega, format=f)
                       if s:
                           s.delete()
               messages.success(request, (u"Dia d'entrega guardat correctament"))
               return render(request, "romani/productors/dates_list.html", {'productor': productor})


    formats_sel = DiaFormatStock.objects.filter(dia=diaentrega)

    comandes = Entrega.objects.filter(comanda__format__producte__in=productes, dia_entrega=diaentrega)

    # contractes = Contracte.objects.filter(producte__in=productes, data_fi__isnull=True, dies_entrega__id__exact=diaentrega.id)

    return render(request, "romani/productors/diaentrega.html", {'dia': diaentrega, 'productor': productor, 'productes': productes, 'formatstockform': formatstockform,
                                                                 'formats_sel': formats_sel, 'comandes': comandes, 'dia_prod': diaproduccio})


from django.forms import formset_factory, modelformset_factory

def DiaProduccioCreateView(request, pro):

    productor = Productor.objects.get(pk=pro)
    productes = Producte.objects.filter(productor=productor)
    StockFormset = formset_factory(StockForm, extra=0)
    formats = TipusProducte.objects.filter(producte__in=productes)
    stockform = StockFormset(initial=[{'format': x} for x in formats])

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

                   return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productes': productes})


       # if formset.is_valid():
               for f in formset:
                   cd = f.cleaned_data
                   dia_prod = dp
                   format = cd.get('format')
                   stock_ini = cd.get('stock_ini')
                   s = Stock.objects.create(dia_prod=dia_prod, format=format, stock_ini=stock_ini )

               messages.success(request, (u"S'ha creat el dia de producció"))

               return render(request, "romani/productors/dates_list.html", {'productor': productor})
           else:

               messages.success(request, (u"S'ha creat el dia de producció"))

               return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productes': productes})


    form = DiaProduccioForm()
    # form.fields['productor'].choices = [(x.pk, x) for x in Productor.objects.filter(pk=pro)]
    form.fields['node'].queryset = Node.objects.filter(productors__id__exact=pro)

    # form.fields['node'].initial = ''


    return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': stockform, 'productor': productor, 'productes': productes})



def DiaProduccioUpdateView(request, pro, pk):

    productor = Productor.objects.get(pk=pro)
    productes = Producte.objects.filter(productor=productor)
    formats = TipusProducte.objects.filter(producte__in=productes)
    dp_obj = DiaProduccio.objects.get(pk=pk)
    stocks = Stock.objects.filter(dia_prod=dp_obj)
    StockFormset = modelformset_factory(Stock, extra=0, form=StockForm)
    stockform = StockFormset(queryset=stocks)
    entregas = Entrega.objects.filter(dia_produccio=dp_obj)

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
                   return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productes': productes, 'comandes': entregas})

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

               messages.success(request, (u"S'ha desat el dia de producció"))
               return render(request, "romani/productors/dates_list.html", {'productor': productor})
           else:
               return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': formset, 'productor': productor, 'productes': productes, 'comandes': entregas})


    form = DiaProduccioForm()
    form.fields['date'].initial = dp_obj.date
    form.fields['node'].initial = dp_obj.node
    form.fields['caducitat'].initial = dp_obj.caducitat


    return render(request, "romani/productors/diaproduccio.html", {'form': form, 'stockform': stockform, 'productor': productor, 'productes': productes, 'comandes': entregas})



class ProducteUpdateView(UpdateView):
    model = Producte
    form_class = ProducteForm
    # success_url="/vista_productes/"
    template_name = "romani/productors/producte_form.html"
    # user = request.user

    # def get_form_kwargs(self):
    #     kwargs = super(ProducteUpdateView, self).get_form_kwargs()
    #     producte = Producte.objects.get(pk=self.kwargs['pk'])
    #     kwargs["productor"] = producte.productor
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProducteUpdateView, self).get_context_data(**kwargs)
        producte = Producte.objects.get(pk=self.kwargs['pk'])
        context["productor"] = producte.productor
        return context

    def get_success_url(self):
        messages.success(self.request, (u"S'ha desat el producte"))
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

    def form_valid(self, form):
        messages.success(self.request, (u"S'ha desat el productor"))
        return super(ProductorCreateView, self).form_valid(form)

class ProducteCreateView(CreateView):
    model = Producte
    form_class = ProducteForm
    template_name = "romani/productors/producte_form.html"

    def get_context_data(self, **kwargs):
        context = super(ProducteCreateView, self).get_context_data(**kwargs)
        context["productor"] = Productor.objects.get(pk=self.kwargs['pro'])
        return context

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
        return context

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
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')

def diaProdEvents(request, pro):

    p = Productor.objects.get(pk=pro)
    eventList = DiaProduccio.objects.filter(productor=p)
    events = []
    for event in eventList:
        day_str = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " 12:00"
        dayend = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " 12:00"
        url = "/pro/" + str(pro) + "/diaproduccio_update/" +  str(event.pk)
        events.append({'title': 'produccio', 'start': day_str, 'end': dayend
                          , 'url': url, 'allDay': 'true'
                       })
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')


def eventsProductors(user):
    eventList = set()
    formats = TipusProducte.objects.filter(productor__responsable=user)

    for p in formats:
        for d in DiaEntrega.objects.filter(formats__format__id__exact=p.id):
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
            day_str = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.inici)[:5]
            dayend = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.final)[:5]
            url = "/pro/distri_dia/" + str(event.pk)
            events.append({'title': event.node.nom, 'start': day_str, 'end': dayend
                              , 'url': url
                           })
    # something similar for owned events, maybe with a different className if you like
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')


def distriCalendarSelected(request):

    # pros_list = Productor.objects.filter(responsable=request.user)
    eventList = eventsProductors(request.user)
    # for pros in pros_list:
    #     p = Productor.objects.get(pk=pros.pk)
    events = []
    for event in eventList:
        franja = event.franja_inici()
        day_str = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.inici)[:5]
        dayend = str(event.date.year) + "-" + str(event.date.month) + "-" + str(event.date.day) + " " + str(franja.final)[:5]
        url = "/pro/distri_dia/" + str(event.pk)
        events.append({'title': event.node.nom, 'start': day_str, 'end': dayend
                          , 'url': url
                       })
    # something similar for owned events, maybe with a different className if you like
    return HttpResponse(json.dumps(events, cls=DjangoJSONEncoder), content_type='application/json')