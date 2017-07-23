
from django import forms
# from .models import Comanda
from romani.models import UserProfile, Comanda, Productor, Producte, DiaEntrega, Node, TipusProducte, FranjaHoraria,Adjunt, Frequencia, DiaProduccio, Stock, DiaFormatStock, Vote
# from romani.views import stock_check_cant
from django.contrib.auth.models import  User, Group
from django.forms.widgets import CheckboxSelectMultiple
from romani.widgets import SelectTimeWidget
import datetime
from datetime import timedelta

class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        exclude = ("data_comanda","client", "preu", "format", "cantitat", "externa", "node" ,"frequencia")

class ComandaProForm(forms.ModelForm):
    class Meta:
        model = Comanda
        exclude = ("data_entrega_txt", "externa", "producte")

    def __init__(self, productor, *args, **kwargs):

        super(ComandaProForm, self).__init__(*args, **kwargs)
        # self.fields["producte"].queryset = Producte.objects.filter(productor=productor)
        self.fields["format"].queryset = TipusProducte.objects.filter(productor=productor)
        self.fields["format"].label = "Producte"
        # self.fields["client"].queryset = TipusProducte.objects.filter(productor=productor)
        eventList = set()
        # productes = Producte.objects.filter(productor=productor)
        formats = TipusProducte.objects.filter(productor=productor)

        # for p in formats:
        #     for d in DiaEntrega.objects.filter(formats__format__id__exact=p.id):
        #         if d:
        #             eventList.add(d.pk)

        # self.fields["dia_entrega"].queryset = DiaEntrega.objects.filter(pk__in=eventList)
        # self.fields["franja_horaria"].queryset = FranjaHoraria.objects.filter(node__productors=productor)
        self.fields["client"].queryset = User.objects.filter(user_profile__lloc_entrega_perfil__in=productor.nodes.all())
        # self.fields["lloc_entrega"].queryset = Node.objects.filter(productors=productor)

    # def save(self, *args, **kwargs):
    #     comanda = En.objects
    #
    #     comanda_form = super(ComandaProForm, self).save(*args,**kwargs)
    #     return comanda_form


class InfoForm(forms.ModelForm):
   class Meta:
        model = Comanda
        exclude = ("data_comanda", "client","preu", "format", "externa", "node", "frequencia")


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        try:
            # self.fields['email'].initial = self.instance.user.email
            # self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    # email = forms.EmailField()
    # username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = UserProfile
        exclude = ("user","invitacions", "bio")

    def save(self, *args, **kwargs):
      """
      Update the primary email address on the related User object as well.
      """
      u = self.instance.user
      # u.email = self.cleaned_data['email']
      # u.username = self.cleaned_data['username']
      u.first_name = self.cleaned_data['first_name']
      u.last_name = self.cleaned_data['last_name']
      u.save()
      profile = super(UserProfileForm, self).save(*args,**kwargs)
      return profile

class TipusProducteForm(forms.ModelForm):

    class Meta:
        model = TipusProducte
        fields = ("nom", "preu", "productor", "producte" )

    def __init__(self, productor, *args, **kwargs):

        super(TipusProducteForm, self).__init__(*args, **kwargs)
        self.fields["productor"].queryset = Productor.objects.filter(pk=productor.pk)
        self.fields["productor"].initial = productor
        self.fields["producte"].queryset = Producte.objects.filter(productor=productor)

class ProductorForm(forms.ModelForm):

    # adjunts = forms.MultipleChoiceField()

    class Meta:
        model = Productor
        fields = ("nom", "text", "hores_limit", "responsable")
        # exclude = ("")

    def __init__(self, user, *args, **kwargs):
        super(ProductorForm, self).__init__(*args, **kwargs)
        self.fields["responsable"].widget = CheckboxSelectMultiple()
        g = Group.objects.get(name='Productors')
        self.fields["responsable"].queryset = g.user_set.all()
        # self.fields["responsable"].queryset = User.objects.filter(pk=user.pk)
        # self.fields["responsable"].initial = user

class AdjuntForm(forms.ModelForm):

    class Meta:
        model = Adjunt
        fields = ("arxiu", "productor")

    def __init__(self, productor, *args, **kwargs):

        super(AdjuntForm, self).__init__(*args, **kwargs)
        self.fields["productor"].queryset = Productor.objects.filter(pk=productor.pk)
        self.fields["productor"].initial = productor
        # self.fields["adjunts"].queryset = Adjunt.objects.filter(pk=productor.pk)


class DiaEntregaForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y', attrs={'id': 'datepicker'}),
                                 input_formats=('%d/%m/%Y',))
    # date = forms.DateField(input_formats='%d/%m/%Y')

    class Meta:
        model = DiaEntrega
        fields = ("date", "franjes_horaries", "node")
    #     # exclude = ("")
    #     widgets = {'date': forms.DateInput(format = '%d/%m/%Y', attrs={'id': 'datepicker'})}

    def __init__(self, node, *args, **kwargs):

        super(DiaEntregaForm, self).__init__(*args, **kwargs)
        self.fields["node"].queryset = Node.objects.filter(pk=node.pk)
        self.fields["node"].initial = node
        self.fields["franjes_horaries"].widget = CheckboxSelectMultiple()
        self.fields["franjes_horaries"].queryset = FranjaHoraria.objects.filter(node=node).order_by('inici', 'final').distinct()


class DiaProduccioForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y', attrs={'id': 'datepicker'}),
                                 input_formats=('%d/%m/%Y',))
    caducitat = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y', attrs={'id': 'datepicker2'}),
                                 input_formats=('%d/%m/%Y',))

    class Meta:
        model = DiaProduccio
        fields = ("date", "caducitat", "node")
        exclude = ("dies_entrega", "productor")


class DiaFormatStockForm(forms.ModelForm):


    class Meta:
        model = DiaFormatStock
        fields = ("tipus_stock","format", "dia")




class StockForm(forms.ModelForm):

    stock_ini = forms.CharField(max_length=5, label='Stock inicial')



    class Meta:
        model = Stock
        fields = ("stock_ini", "format")
        # exclude = ("format",  )
    #
    #
    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields["stock_ini"].initial = self.instance.stock_ini
        self.fields['format'].widget = forms.HiddenInput()
        # self.fields["format"].
        # self.fields['format'].queryset = TipusProducte.objects.filter(pk__lte=10)
        # self.fields['format'].queryset = TipusP

# class ProductorDiaEntregaForm(forms.Form):
#
#     productes = forms.MultipleChoiceField(widget=CheckboxSelectMultiple())


class FranjaHorariaForm(forms.ModelForm):

    class Meta:
        model = FranjaHoraria
        fields = ("inici", "final", "node")
        # exclude = ("node", )

    def __init__(self, node, *args, **kwargs):
        super(FranjaHorariaForm, self).__init__(*args, **kwargs)
        self.fields["node"].queryset = Node.objects.filter(pk=node.pk)
        self.fields["node"].initial = node
        self.fields["inici"].widget=SelectTimeWidget()
        self.fields["final"].widget=SelectTimeWidget()

class NodeForm(forms.ModelForm):

    class Meta:
        model = Node
        fields = ("nom", "carrer", "numero", "pis", "poblacio", "codi_postal", "text", "frequencia", "a_domicili", "responsable")

    def __init__(self, user, *args, **kwargs):
        super(NodeForm, self).__init__(*args, **kwargs)
        self.fields["responsable"].widget=CheckboxSelectMultiple()
        g = Group.objects.get(name='Nodes')
        self.fields["responsable"].queryset = g.user_set.all()
        # self.fields["frequencies"].widget=CheckboxSelectMultiple()
        self.fields["frequencia"].queryset = Frequencia.objects.all()


class ProducteForm(forms.ModelForm):

    class Meta:
        model = Producte
        fields = ("nom", "etiqueta", "foto", "text_curt", "descripcio", "frequencies", "keywords")
        exclude = ("productor", "karma_value", "datahora", "karma_date", "dies_entrega", "nodes")

    # def __init__(self, productor, *args, **kwargs):
    #     super(ProducteForm, self).__init__(*args, **kwargs)
    #     self.fields["formats"].widget = CheckboxSelectMultiple()
    #     self.fields["formats"].queryset = TipusProducte.objects.filter(productor=productor)





#
# def stock_check_cant(format, dia, cantitat):
#      # Comprova que hi hagi stock per a una quantitat determinada
#      d = format.dies_entrega.get(dia=dia)
#      if d.tipus_stock == '0':
#             try:
#                 diaproduccio = DiaProduccio.objects.filter(date__lte=d.dia.date, productor=format.productor).order_by('-date').first()
#                 if diaproduccio:
#                    s = format.stocks.get(dia_prod=diaproduccio)
#                    num = int(s.stock) - int(cantitat)
#                    if num >= 0:
#                        return True
#                    else:
#                        return False
#             except:
#                 return False
#
#      elif d.tipus_stock == '1':
#             num = int(format.stock_fix) - int(cantitat)
#             if num >= 0:
#                 return True
#             else:
#                 return False
#
#      elif d.tipus_stock == '2':
#             return True



# class ContracteForm(forms.ModelForm):
#
#     class Meta:
#         model = Contracte
#         fields = ("dies_entrega", )
#         labels = {"dies_entrega": "Dies d'entrega"}
#
#     def __init__(self, *args, **kwargs):
#         super(ContracteForm, self).__init__(*args, **kwargs)
#         self.fields["dies_entrega"].widget = CheckboxSelectMultiple()
#         pk_lst = set()
#
#         date = datetime.date.today() + timedelta(hours=int(self.instance.format.productor.hores_limit))
#         for d in DiaEntrega.objects.filter(formats__format__id__exact=self.instance.format.id, node=self.instance.lloc_entrega, date__gt=date).order_by('date'):
#             stock_result = stock_check_cant(self.instance.format, d, self.instance.cantitat)
#             if stock_result:
#                 pk_lst.add(d.pk)
#
#         self.fields["dies_entrega"].queryset = DiaEntrega.objects.filter(pk__in=pk_lst)


class NodeProductorsForm(forms.ModelForm):

    class Meta:
        model = Node
        fields = ("productors", )

    def __init__(self, *args, **kwargs):
        super(NodeProductorsForm, self).__init__(*args, **kwargs)
        self.fields["productors"].widget = CheckboxSelectMultiple()
        self.fields["productors"].queryset = Productor.objects.all()

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ("voter", "positiu")
        exclude = ("entrega", )