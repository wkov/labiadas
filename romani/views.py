from django.shortcuts import render, get_object_or_404
from romani.models import Producte, TipusProducte, Node, DiaEntrega, Frequencia, DiaProduccio
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from romani.models import UserProfile, Key
from romani.forms import UserProfileForm, InfoForm
# from romani.public_views import stock_calc
from django.http import HttpResponse

from django.utils import timezone
from notifications import notify
from django.contrib.auth.models import  User
import json
from django.contrib import messages
from registration.backends.simple.views import RegistrationView

from django import forms
from registration.forms import RegistrationForm
import datetime
from datetime import timedelta

# from romani.public_views import stock_calc
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from labiadas.settings import  DEFAULT_FROM_EMAIL
from django.views.generic import *
from romani.forms import PasswordResetRequestForm, SetPasswordForm
from django.contrib import messages
# from django.contrib.auth.models import User
from django.db.models.query_utils import Q



from django.views import View
from django.shortcuts import render


class Leaderboard(View):
    title = 'Leaderboard'
    template = 'react_base.html'
    component = 'leaderboard.js'

    def get(self, request):
        # gets passed to react via window.props
        props = {
            'users': [
                {'username': 'alice'},
                {'username': 'bob'},
            ]
        }

        context = {
            'title': self.title,
            'component': self.component,
            'props': props,
        }

        render(request, self.template, context)




class ResetPasswordRequestView(FormView):
    template_name = "registration/test_template.html"    #code for template is given below the view's code
    success_url = '/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
# This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):

    # A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).

        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:                 #uses the method written above
            # If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            associated_users= User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': 'https://lamassa.org',
                            'site_name': 'lamassa.org',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'https',
                            }
                        subject_template_name ='registration/password_reset_subj.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name ='registration/password_reset_mail.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Hem enviat un email a ' + data +". Si us plau, comprova el teu correu per a reiniciar la contrasenya.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No hi ha usuari associat a aquest email')
            return result
        else:
            # If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'https://lamassa.org', #or your domain
                        'site_name': 'lamassa.org',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                        }
                    subject_template_name='registration/password_reset_subj.txt'
                    email_template_name='registration/password_reset_mail.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Hem enviat un email a ' + data +". Si us plau, comprova el teu correu per a reiniciar la contrasenya.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'Aquest usuari no existeix.')
            return result
        messages.error(request, 'Dades incorrectes')
        return self.form_invalid(form)

from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, get_user_model, update_session_auth_hash)

class PasswordResetConfirmView(FormView):
    template_name = "registration/test_template.html"
    success_url = '/login/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'La contrasenya ha estat restablerta.')
                return self.form_valid(form)
            else:
                messages.error(request, 'El reinici de la contrasenya no ha funcionat.')
                return self.form_invalid(form)
        else:
            messages.error(request,'El enllaç utilitzat per cambiar la contrasenya ja no és vàlid.')
            return self.form_invalid(form)

class UserProfileRegistrationForm(RegistrationForm):
    first_name = forms.CharField(max_length=15, label='Nombre')
    last_name = forms.CharField(max_length=15, label='Apellido')
    email = forms.EmailField(help_text='', required=True, label='e-mail')

    class Meta:
        model = User
        fields = ("username", "email", 'first_name', 'last_name')




class MyRegistrationView(RegistrationView):

    form_class = UserProfileRegistrationForm


    def get_context_data(self, **kwargs):
        context = super(MyRegistrationView, self).get_context_data(**kwargs)
        key = Key.objects.get(key=self.kwargs['pk'])

        if key.key and not key.nou_usuari:
            return context



    def get_success_url(self, user):
        key = Key.objects.get(key=self.kwargs['pk'])
        key.nou_usuari = user
        key.save()
        return '/nou_usuari/'



def user_created(sender, user, request, **kwargs):
    """
    Called via signals when user registers. Creates different profiles and
    associations
    """
    user.first_name= request.POST.get('first_name')
    user.last_name=request.POST.get('last_name')
    user.save()


from registration.signals import user_registered
user_registered.connect(user_created)


def nouUsuariView(request):

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    u_key = Key.objects.get(nou_usuari=request.user)
    u = UserProfile.objects.get(user=u_key.usuari)
    s = u.lloc_entrega.get_frequencia()

    user_p.lloc_entrega = u.lloc_entrega
    user_p.save()

    return render(request, "nouUsuari.html", {'up': user_p, 'nodes': nodes, 'frequencia': s.nom})



def AjudaView(request):

    webmaster = User.objects.filter(pk="37").first()
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "ajuda.html",{'up': user_p, 'webmaster': webmaster})



import random

def generate_key(request):
    key = random.randint(1, 999999)
    v = Key.objects.create(key=key, usuari=request.user)
    return v.key

def registerView(request):
    return render(request, "nouUsuari.html")

def nodesNouUsuariView(request):

    u_key = Key.objects.get(nou_usuari=request.user)
    u = UserProfile.objects.get(user=u_key.usuari)
    json_res = []
    for i in Node.objects.all().exclude(pk=1):

        if i == u.lloc_entrega:
            json_obj = dict(
                        nom = i.nom,
                        carrer = i.carrer,
                        numero = i.numero,
                        pis = i.pis,
                        punt_lat = str(i.position.latitude),
                        punt_lng = str(i.position.longitude),
                        poblacio = i.poblacio,
                        pk = i.pk,
                        selected = "True",
                        a_domicili = i.a_domicili
                    )
        else:
            json_obj = dict(
                        nom = i.nom,
                        carrer = " ",
                        numero = " ",
                        pis = " ",
                        punt_lat = " ",
                        punt_lng = " ",
                        poblacio = i.poblacio,
                        pk = i.pk,
                        selected = "False",
                        a_domicili = " "
                    )


        json_res.append(json_obj)
    return HttpResponse(json.dumps(json_res), content_type='application/json')


from django.core.mail import send_mail
#funció exclusivament per a enviar invitacio a cela a un usuari que se li passa a la funció
def enviarInvitacio(email, nom, k):

    text = nom + " t'ha convidat a 'La Massa' xarxa de productes de proximitat: "+ "lamassa.org/register/" + str(k)
    send_mail("Convidat a 'La Massa'", text, 'lamassaxarxa@gmail.com', [email] ,fail_silently=True )

#en cas de que si estigui, enviar invitació al usuari
def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


def ConvidarView(request):

    up = UserProfile.objects.get(user = request.user)
    message_email = ""
    message = ""
    nodes = Node.objects.all()
    email = ""

    if request.POST:

        if up.invitacions > 0:

            email = request.POST.get('email')

            if email:
                #comprobem que els mails no estiguin donats de alta a la xarxa
                alta = User.objects.filter(email = email).first()
                if not alta:
                    if validateEmail(email):
                        try:
                            k = generate_key(request)
                            enviarInvitacio(email, up.user.get_full_name(), k)
                            up.invitacions = up.invitacions - 1
                            up.save()
                            key = Key.objects.get(key=k)
                            notify.send(key, recipient=up.user, verb="",
                                description=", has convidat un nou usuari. " , timestamp=timezone.now())
                            message_email = "S'ha enviat la sol·licitud al correu electrònic correctament"
                        except:
                           message_email = "No s'ha pogut enviar la sol·licitud al correu electrònic"
                    else:
                        message_email = "No s'ha pogut enviar la sol·licitud al correu electrònic"
                else:
                    message_email = "La direcció de correu electrònic ja té usuari a la xarxa"
            else:
                k = generate_key(request)
                up.invitacions = up.invitacions - 1
                up.save()
                key = Key.objects.get(key=k)
                notify.send(key, recipient=up.user, verb="",
                                description=", has generat una nova invitació " , timestamp=timezone.now())

                s = "http://lamassa.org/register/" + str(k)
                message = s

        else:
            message_email = "Ja has utilitzat totes les invitacions. De moment no pots convidar més gent. Gràcies"

    return render(request, "convidar.html", {'invitacions':up.invitacions, 'email':email, 'message':message, 'message_email': message_email, 'nodes': nodes})



def DomiciliView(request):

    if request.POST:

        # if 'lloc_entrega_perfil' in request.POST:
        #
        #     l = request.POST.get('lloc_entrega_perfil')
        #     node = get_object_or_404(Node, pk=l)
        #     up = UserProfile.objects.get(user=request.user)
        #     nf = node.get_frequencia()
        #
        #     if node.a_domicili == True:
        #         json_obj = dict(carrer = up.carrer, numero = up.numero, pis = up.pis, poblacio = node.poblacio, a_domicili = node.a_domicili,
        #                         frequencia = nf.nom)
        #     else:
        #         json_obj = dict(carrer = node.carrer, numero = node.numero, pis = node.pis, poblacio = node.poblacio, a_domicili = node.a_domicili,
        #                          frequencia = nf.nom )
        #
        #     return HttpResponse(json.dumps(json_obj), content_type='application/json')

        if 'lloc_entrega' in request.POST:

            l = request.POST.get('lloc_entrega')
            node = get_object_or_404(Node, pk=l)
            up = UserProfile.objects.get(user=request.user)
            nf = node.get_frequencia()
            # json_obj = []
            if node.a_domicili == True:
                json_obj = dict(carrer = up.carrer, numero = up.numero, pis = up.pis, poblacio = node.poblacio, a_domicili = node.a_domicili, frequencia=nf.nom)
            else:
                json_obj = dict(carrer = node.carrer, numero = node.numero, pis = node.pis, poblacio = node.poblacio, a_domicili = node.a_domicili, frequencia=nf.nom)

            return HttpResponse(json.dumps(json_obj), content_type='application/json')

        # if 'lloc_entrega_reg' in request.POST:
        #
        #     l = request.POST.get('lloc_entrega_reg')
        #     node = get_object_or_404(Node, pk=l)
        #     up = UserProfile.objects.get(user=request.user)
        #     nf = node.get_frequencia()
        #
        #     if node.a_domicili == True:
        #         json_obj = dict(poblacio = node.poblacio, a_domicili = node.a_domicili, frequencia = nf.nom)
        #     else:
        #         json_obj = dict(carrer = node.carrer, numero = node.numero, pis = node.pis, poblacio = node.poblacio, a_domicili = node.a_domicili,
        #                         frequencia = nf.nom )
        #
        #     return HttpResponse(json.dumps(json_obj), content_type='application/json')


def NodeHorariView(request):

    if request.POST:
        if 'lloc_entrega' in request.POST:
            l = request.POST.get('lloc_entrega')
        # elif 'lloc_entrega_reg' in request.POST:
        #         l = request.POST.get('lloc_entrega_reg')
            node = get_object_or_404(Node, pk=l)
    else:
        up = UserProfile.objects.filter(user = request.user).first()
        if up.lloc_entrega:
            node = up.lloc_entrega
        else:
            k = Key.objects.filter(nou_usuari = request.user).first()
            up2 = UserProfile.objects.filter(user = k.usuari).first()
            node = up2.lloc_entrega

    v_query = node.dies_entrega.filter(date__gt = datetime.datetime.today())

    v_query = v_query.order_by('date')

    v = v_query.first()

    if v:
        json_res = []
        d = v.date + timedelta(days=7)
        k = node.dies_entrega.filter(date__lt = d, date__gt = datetime.datetime.today()).order_by('date')
        for dia in k:
            json_res_aux = []
            for franja in dia.franjes_horaries.all():
                json_obj_aux = dict(
                    inici = str(franja.inici)[:5],
                    final = str(franja.final)[:5],
                    pk = franja.pk
                )
                json_res_aux.append(json_obj_aux)


            json_obj = dict(
                dia = str(dia.dia()),
                pk = dia.pk,
                franjes = json_res_aux)
            json_res.append(json_obj)

        return HttpResponse(json.dumps(json_res), content_type='application/json')

    return HttpResponse("Fail")



def NodeDetailView(request, pk):

    node = Node.objects.get(pk=pk)

    return render(request, "node_detail.html", {'node': node})



def CoordenadesView(request):

    if 'lloc_entrega' in request.POST:
        l = request.POST.get('lloc_entrega')
        node = get_object_or_404(Node, pk=l)
    # elif 'lloc_entrega_perfil' in request.POST:
    #     l = request.POST.get('lloc_entrega_perfil')
    #     node = get_object_or_404(Node, pk=l)
    # else:
    #     l = request.POST.get('lloc_entrega_perfil')
        if node:
            json_obj = dict(
                Lat = str(node.position.latitude),
                Lng = str(node.position.longitude)
            )

            return HttpResponse(json.dumps(json_obj), content_type='application/json')

    return HttpResponse("Fail")


def AllCoordenadesView(request):

        nodes = Node.objects.all()

        json_res = []

        for node in nodes:
            if node.position:
                json_obj = dict(
                Lat = str(node.position.latitude),
                Lng = str(node.position.longitude),
                nom = node.nom,
                a_domicili = str(node.a_domicili),
                text = node.text)
                json_res.append(json_obj)

        return HttpResponse(json.dumps(json_res), content_type='application/json')




def NodeSaveView(request):

    if request.POST:

        v = UserProfile.objects.get(user = request.user)

        if 'lloc_entrega' in request.POST:
            # if 'nom_complet' in request.POST:
            #     o = request.POST.get('nom_complet')
                l = request.POST.get('lloc_entrega')
                node = get_object_or_404(Node, pk=l)
                v.lloc_entrega = node

                if 'poblaciox' in request.POST:
                    v.poblacio = request.POST.get('poblaciox')

                if node.a_domicili == True:
                    if 'carrerx' in request.POST:
                        v.carrer = request.POST.get('carrerx')
                    if 'numerox' in request.POST:
                        v.numero = request.POST.get('numerox')
                    if 'pisx' in request.POST:
                        v.pis = request.POST.get('pisx')
                    # if 'punt_latx' in request.POST:
                    #     v.punt_lat = request.POST.get('punt_latx')
                    # if 'punt_lngx' in request.POST:
                    #     v.punt_lng = request.POST.get('punt_lngx')
                v.save()

                return HttpResponse(json.dumps("OK"), content_type='application/json')



def NodeCalcView(request):
    if request.POST:
        if 'lloc_entrega' in request.POST:
            l = request.POST.get('lloc_entrega')
            # g = request.POST.get('producte_pk')
            f = request.POST.get('format_pk')
            cant = request.POST.get('cantitat_t')
            node = get_object_or_404(Node, pk=l)
            # producte = Producte.objects.filter(pk=g).first()
            format = TipusProducte.objects.get(pk=f)
            json_res = []

            for dia in format.dies_entrega.order_by("dia__date").filter(dia__node=node,dia__date__gte=datetime.datetime.now()):
                aux = dia.dia.franja_inici()
                daytime = datetime.datetime(dia.dia.date.year, dia.dia.date.month, dia.dia.date.day, aux.inici.hour, aux.inici.minute)
                date = datetime.datetime.now() + timedelta(hours=dia.hores_limit)
                if daytime > date:
                    stock_result = format.stock_calc(dia.dia, cant)
                    if stock_result['result'] == True:
                        day_str = str(dia.dia.date.year) + "-" + str(dia.dia.date.month) + "-" + str(dia.dia.date.day)
                        a = datetime.datetime.strptime(day_str, '%Y-%m-%d').strftime('%d/%m/%Y')
                        json_obj = dict(
                            dia = dia.dia.dia(),
                            date = a,
                            pk = dia.dia.pk)
                        json_res.append(json_obj)
                if len(json_res) > 4:
                    break
            return HttpResponse(json.dumps(json_res), content_type='application/json')

def FreqCalcView(request):
    if request.POST:
        if 'lloc_entrega' in request.POST:
            l = request.POST.get('lloc_entrega')
            g = request.POST.get('producte_pk')
            node = get_object_or_404(Node, pk=l)
            producte = Producte.objects.filter(pk=g).first()
            json_res = []
            for f in node.frequencia.freq_list():
                if f in producte.frequencies.freq_list():
                    json_obj = dict(
                        nom = f.nom,
                        num = f.num
                    )
                    json_res.append(json_obj)

            return HttpResponse(json.dumps(json_res), content_type='application/json')

def FranjaCalcView(request):
    if request.POST:
        if 'dataentrega' in request.POST:
            l = request.POST.get('dataentrega')
            if l:
                dia = get_object_or_404(DiaEntrega, pk=l)
                json_res = []
                for franja in dia.franjes_horaries.all():
                    json_obj = dict(
                        inici = str(franja.inici)[:5],
                        final = str(franja.final)[:5],
                        pk = franja.pk
                    )
                    json_res.append(json_obj)
                return HttpResponse(json.dumps(json_res), content_type='application/json')
    return HttpResponse("NO")


class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

class InfoFormBaseView(FormView):
    form_class = InfoForm


    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        producte = get_object_or_404(Producte, pk=form.data["producte"])
        user = self.request.user
        format = get_object_or_404(TipusProducte, pk=form.data["format"])
        user_profile = UserProfile.objects.get(user = user)
        cantitat = form.data["cantitat"]
        preu_aux = format.preu
        preu = preu_aux * float(cantitat)
        ret = {"success": 1}
        ret["format"] = format.nom
        ret["format_pk"]= format.pk
        ret["preu"] = preu
        ret["producte"] = producte.nom
        ret["producte_pk"] = producte.pk
        ret["cantitat"] = cantitat
        ret["imatge"] = producte.thumb.url


        json_res = []
        jfreq = []

        # Carreguem els possibles nodes on l-usuari pot trobar el producte concret
        if format.en_stock(cantitat, user_profile.lloc_entrega):
            for i in format.nodes(cantitat).all():
                if i == user_profile.lloc_entrega:
                    # Guardem les frequencies del node per informar a l-usuari en el modal
                    for d in i.frequencia.freq_list():
                        if d in producte.frequencies.freq_list():
                            f_obj = dict(nom = d.nom,
                                         num = d.num
                                         )
                            jfreq.append(f_obj)
                    json_obj = dict(
                                nom = i.nom,
                                poblacio = i.poblacio,
                                pk = i.pk,
                                selected = "True"
                            )
                else:
                    json_obj = dict(
                                nom = i.nom,
                                poblacio = i.poblacio,
                                pk = i.pk,
                                selected = "False"
                            )
                json_res.append(json_obj)
        else:
            ret = {"success": 0}
            messages.error(self.request, (u"Disculpa, NO està disponible la cantitat sol·licitada"))

        ret["nodes"] = json_res
        ret["freqs"] = jfreq

        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)




class InfoFormView(JSONFormMixin, InfoFormBaseView):
    pass


class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super(UserProfileEditView, self).get_context_data(**kwargs)
        nodes = Node.objects.exclude(pk=1)
        context['nodes'] = nodes
        u = UserProfile.objects.get(user=self.request.user)
        s = u.lloc_entrega.get_frequencia()
        if s:
            context['frequencia'] = s.nom
        else:
            f = Frequencia.objects.get(num=0)
            context['frequencia'] = f.nom
        return context

    def form_valid(self, form):

        lloc = get_object_or_404(Node, pk=form.data["lloc_entrega"])

        if lloc.a_domicili == False:

            form.instance.carrer = ""
            form.instance.numero = ""
            form.instance.pis = ""
            form.instance.poblacio = ""

        return super(UserProfileEditView, self).form_valid(form)

    # def form_invalid(self, form):




    def get_success_url(self):
        notify.send(self.object, recipient= self.object.user, verb="Has modificat les teves dades ", action_object=self.object,
        description="" , timestamp=timezone.now())

        messages.success(self.request, (u"S'han desat les modificacions realitzades"))
        return reverse("coope")
