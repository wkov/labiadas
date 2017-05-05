from django import forms
# from .models import Comanda
from romani.models import UserProfile, Comanda, Productor, Producte, DiaEntrega, Node, TipusProducte, FranjaHoraria, Contracte, Adjunt
from django.contrib.auth.models import  User
from django.forms.widgets import CheckboxSelectMultiple
from romani.widgets import SelectTimeWidget
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

    # adjunts = forms.MultipleChoiceField()

    class Meta:
        model = Productor
        fields = ("nom", "cuerpo")
        # exclude = ("")

    # def __init__(self, productor, *args, **kwargs):
    #     super(ProductorForm, self).__init__(*args, **kwargs)
    #     self.fields["adjunts"].queryset = Adjunt.objects.filter(productor=productor)
    #     self.fields["adjunts"].widget = CheckboxSelectMultiple()

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

        # self.fields["date"].input_formats = '%m-%d-%Y'

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


class ProductorDiaEntregaForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     # pro_pk = kwargs.pop('pro', None)
    #     super(ProductorDiaEntregaForm, self).__init__(*args, **kwargs)
    #     try:
    #         # productor = Productor.objects.get(pk=pro_pk)
    #         # self.fields["productes"].widget = CheckboxSelectMultiple()
    #         # productor = self.instance
    #         self.fields["productes"].queryset = Producte.objects.filter(productor=self.)
    #     except User.DoesNotExist:
    #         pass

    productes = forms.MultipleChoiceField(widget=CheckboxSelectMultiple())

    # class Meta:
    #     model = Productor
    #     # fields = ("date",  )
    #     exclude = ("all", )

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


# class ProducteDatesForm(forms.ModelForm):
#
#     class Meta:
#         model = Producte
#         fields = ("nom", "dies_entrega", "frequencies" )
#         # exclude = ("productor", "karma_value", "datahora", "karma_date")
#
#     def __init__(self, *args, **kwargs):
#
#         super(ProducteDatesForm, self).__init__(*args, **kwargs)
#
#         self.fields["dies_entrega"].widget = CheckboxSelectMultiple()
#         self.fields["dies_entrega"].queryset = DiaEntrega.objects.filter(date__gte=datetime.datetime.now(), node__productors__id__exact=self.instance.productor.id)