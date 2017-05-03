from django import forms
# from .models import Comanda
from romani.models import UserProfile, Comanda, Productor, Producte, DiaEntrega, Node, TipusProducte, FranjaHoraria, Contracte
from django.contrib.auth.models import  User
from django.forms.widgets import CheckboxSelectMultiple
import datetime


class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        exclude = ("entregat","cancelat","data_comanda","data_entrega", "lloc_entrega", "franja_horaria", "client", "preu", "format", "producte", "cantitat", "primera_entrega", "data_entrega_txt")



class InfoForm(forms.ModelForm):
   class Meta:
        model = Comanda
        exclude = ("entregat","cancelat","data_comanda", "franja_horaria", "lloc_entrega", "client","preu", "format", "data_entrega_txt")


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
        exclude = ("user","invitacions", "bio","convidats")

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



class ProductorForm(forms.ModelForm):

    class Meta:
        model = Productor
        fields = ("nom", "cuerpo", "adjunt")
        # exclude = ("")

class DiaEntregaForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y', attrs={'id': 'datepicker'}),
                                 input_formats=('%d/%m/%Y',))
    # date = forms.DateField(input_formats='%d/%m/%Y')

    class Meta:
        model = DiaEntrega
        fields = ("date", "franjes_horaries", "node")
    #     # exclude = ("")
    #     widgets = {'date': forms.DateInput(format = '%d/%m/%Y', attrs={'id': 'datepicker'})}

    def __init__(self, nodes, *args, **kwargs):

        super(DiaEntregaForm, self).__init__(*args, **kwargs)
        self.fields["node"].queryset = nodes
        self.fields["franjes_horaries"].widget = CheckboxSelectMultiple()
        self.fields["franjes_horaries"].queryset = FranjaHoraria.objects.filter(dia__node__in=nodes).order_by('inici', 'final').distinct()

        # self.fields["date"].input_formats = '%m-%d-%Y'

class NodeForm(forms.ModelForm):

    class Meta:
        model = Node
        fields = ("nom", "carrer", "numero", "pis", "poblacio", "codi_postal", "a_domicili", "text", "frequencies")
        # exclude = ("")


class ProducteForm(forms.ModelForm):

    class Meta:
        model = Producte
        # fields = ("nom", "cuerpo", "adjunt", "responsable")
        exclude = ("productor", "karma_value", "datahora", "karma_date", "frequencies", "dies_entrega", "nodes")

    def __init__(self, *args, **kwargs):

        super(ProducteForm, self).__init__(*args, **kwargs)

        # self.fields["nodes"].widget = CheckboxSelectMultiple()
        # self.fields["nodes"].queryset = Node.objects.filter(productors__id__exact=self.instance.productor.id)
        self.fields["formats"].widget = CheckboxSelectMultiple()
        self.fields["formats"].queryset = TipusProducte.objects.filter(productor=self.instance.productor)


# class LlocsForm(forms.ModelForm):
#
#     class Meta:
#         model = Producte
#         fields = ("nodes", )
#         # exclude = ("productor", "karma_value", "datahora", "karma_date", "frequencies", "dies_entrega")
#
#     def __init__(self, *args, **kwargs):
#
#         super(LlocsForm, self).__init__(*args, **kwargs)
#
#         self.fields["nodes"].widget = CheckboxSelectMultiple()
#         self.fields["nodes"].queryset = Node.objects.filter(productors__id__exact=self.instance.productor.id)

class ContracteForm(forms.ModelForm):

    class Meta:
        model = Contracte
        fields = ("dies_entrega", )

    def __init__(self, *args, **kwargs):

        super(ContracteForm, self).__init__(*args, **kwargs)

        self.fields["dies_entrega"].widget = CheckboxSelectMultiple()
        self.fields["dies_entrega"].queryset = DiaEntrega.objects.filter(productes__id__exact=self.instance.producte.id, node=self.instance.lloc_entrega, date__gt=datetime.datetime.today()).order_by('date')

class NodeProductorsForm(forms.ModelForm):

    class Meta:
        model = Node
        fields = ("productors", )

    def __init__(self, *args, **kwargs):

        super(NodeProductorsForm, self).__init__(*args, **kwargs)

        self.fields["productors"].widget = CheckboxSelectMultiple()
        self.fields["productors"].queryset = Productor.objects.all()


class ProductorDiaEntregaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # pro_pk = kwargs.pop('pro', None)
        super(ProductorDiaEntregaForm, self).__init__(*args, **kwargs)
        try:
            # productor = Productor.objects.get(pk=pro_pk)
            # self.fields["productes"].widget = CheckboxSelectMultiple()
            # productor = self.instance
            self.fields["productes"].queryset = Producte.objects.filter(productor=self.instance)
        except User.DoesNotExist:
            pass

    productes = forms.CheckboxSelectMultiple()

    class Meta:
        model = Productor
        # fields = ("date",  )
        exclude = ("all", )

    # def save(self, *args, **kwargs):
    #   """
    #   Update the primary email address on the related User object as well.
    #   """
    #   u = self.instance.user
    #   # u.email = self.cleaned_data['email']
    #   # u.username = self.cleaned_data['username']
    #   u.first_name = self.cleaned_data['first_name']
    #   u.last_name = self.cleaned_data['last_name']
    #   u.save()
    #   profile = super(UserProfileForm, self).save(*args,**kwargs)
    #   return profile


class ProducteDatesForm(forms.ModelForm):

    class Meta:
        model = Producte
        fields = ("nom", "dies_entrega", "frequencies" )
        # exclude = ("productor", "karma_value", "datahora", "karma_date")

    def __init__(self, *args, **kwargs):

        super(ProducteDatesForm, self).__init__(*args, **kwargs)

        self.fields["dies_entrega"].widget = CheckboxSelectMultiple()
        self.fields["dies_entrega"].queryset = DiaEntrega.objects.filter(date__gte=datetime.datetime.now(), node__productors__id__exact=self.instance.productor.id)