
from django import forms
from romani.models import UserProfile, Comanda, Productor, Producte, DiaEntrega, Node, TipusProducte, FranjaHoraria,Adjunt, Frequencia, DiaProduccio, Stock, DiaFormatStock, Vote
from django.contrib.auth.models import  User, Group
from django.forms.widgets import CheckboxSelectMultiple
from romani.widgets import SelectTimeWidget
import datetime
from datetime import timedelta


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email o Nom d'usuari"), max_length=254)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("Les 2 contrassenyes NO coincideixen."),
        }
    new_password1 = forms.CharField(label=("Nova contrasenya"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("Confirmar Nova contrasenya"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

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
        self.fields["format"].queryset = TipusProducte.objects.filter(productor=productor)
        self.fields["format"].label = "Producte"
        self.fields["client"].queryset = User.objects.filter(user_profile__lloc_entrega__in=productor.nodes.all())


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
        exclude = ("user","invitacions", "bio", "avatar")

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
        self.fields["hores_limit"].label = 'Temps límit per a fer comandes en Hores'
        # self.fields["responsable"].initial = user

class AdjuntForm(forms.ModelForm):

    class Meta:
        model = Adjunt
        fields = ("arxiu", "productor")

    def __init__(self, productor, *args, **kwargs):

        super(AdjuntForm, self).__init__(*args, **kwargs)
        self.fields["productor"].queryset = Productor.objects.filter(pk=productor.pk)
        self.fields["productor"].initial = productor


class DiaEntregaForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y', attrs={'id': 'datepicker'}),
                                 input_formats=('%d/%m/%Y',))

    class Meta:
        model = DiaEntrega
        fields = ("date", "franjes_horaries", "node")

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

    def __init__(self, *args, **kwargs):
        super(DiaProduccioForm, self).__init__(*args, **kwargs)
        self.fields["node"].label = "Cooperativa (OPCIONAL)"


class DiaFormatStockForm(forms.ModelForm):


    class Meta:
        model = DiaFormatStock
        fields = ("tipus_stock","format", "dia", "hores_limit")




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


class FranjaHorariaForm(forms.ModelForm):

    class Meta:
        model = FranjaHoraria
        fields = ("inici", "final", "node")

    def __init__(self, node, *args, **kwargs):
        super(FranjaHorariaForm, self).__init__(*args, **kwargs)
        self.fields["node"].queryset = Node.objects.filter(pk=node.pk)
        self.fields["node"].initial = node
        self.fields["inici"].widget=SelectTimeWidget()
        self.fields["final"].widget=SelectTimeWidget()

class NodeForm(forms.ModelForm):

    class Meta:
        model = Node
        fields = ("nom", "carrer", "numero", "pis", "poblacio", "codi_postal", "position", "text", "a_domicili", "responsable")

    def __init__(self, user, *args, **kwargs):
        super(NodeForm, self).__init__(*args, **kwargs)
        self.fields["responsable"].widget=CheckboxSelectMultiple()
        g = Group.objects.get(name='Nodes')
        self.fields["responsable"].queryset = g.user_set.all()
        # self.fields["frequencia"].queryset = Frequencia.objects.all()
        self.fields["position"].label = 'Coordenades'


class ProducteForm(forms.ModelForm):

    class Meta:
        model = Producte
        fields = ("nom",  "productor", "etiqueta", "foto", "text_curt", "descripcio", "keywords")
        # exclude = ("datahora",)

    def __init__(self, productor, *args, **kwargs):

        super(ProducteForm, self).__init__(*args, **kwargs)
        self.fields["productor"].queryset = Productor.objects.filter(pk=productor.pk)
        self.fields["productor"].initial = productor

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