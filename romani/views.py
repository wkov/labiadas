from django.shortcuts import render, get_object_or_404
from .models import Producte, Productor, Comanda, Contracte, TipusProducte, Node, DiaEntrega, FranjaHoraria, Key, Convidat, Frequencia
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView
from .models import UserProfile, Etiqueta, Key
from .forms import UserProfileForm, ComandaForm, InfoForm
import datetime
from django.utils import timezone
from notifications import notify
from django.contrib.auth.models import  User
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

from registration.backends.simple.views import RegistrationView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from registration import signals
# Perque retorni a la pantalla principal despres de completar el registre sobreescribim la classe

from django import forms
from registration.forms import RegistrationForm
import datetime
from django.forms.extras.widgets import SelectDateWidget

class UserProfileRegistrationForm(RegistrationForm):
    first_name = forms.CharField(max_length=15, label='Nom')
    last_name = forms.CharField(max_length=15, label='Cognom')
    date_of_birth = forms.DateField(label='Data de naixement',
                                    widget=SelectDateWidget(
                                        years=[y for y in range(1900,
                                                                                    datetime.datetime.now().year-17)],
                                                            attrs=({'style': 'width: 33%; display: inline-block;'})
                                    ),
                                    )

    class Meta:
        model = User
        fields = ("username", "email", 'first_name', 'last_name',
                  'date_of_birth')




class MyRegistrationView(RegistrationView):

    form_class = UserProfileRegistrationForm


    def get_context_data(self, **kwargs):
        context = super(MyRegistrationView, self).get_context_data(**kwargs)
        key = Key.objects.get(key=self.kwargs['pk'])

        if key.key and not key.nou_usuari:
            return context





    # def register(self, request, form):
    #     # request.session
    #     new_user = form.save()
    #     username_field = getattr(new_user, 'USERNAME_FIELD', 'username')
    #     new_user = authenticate(
    #         username=getattr(new_user, username_field),
    #         password=form.cleaned_data['password1']
    #     )
    #
    #     login(request, new_user)
    #     signals.user_registered.send(sender=self.__class__,
    #                                  user=new_user,
    #                                  request=request)
    #     return new_user

    def get_success_url(self, request, new_user):
        key = Key.objects.get(key=self.kwargs['pk'])
        key.nou_usuari = new_user
        key.save()
        return "/nou_usuari/"



def user_created(sender, user, request, **kwargs):
    """
    Called via signals when user registers. Creates different profiles and
    associations
    """
    # form = UserProfileRegistrationForm(request.Post)
    # Update first and last name for user
    user.first_name= request.POST.get('first_name')
    user.last_name=request.POST.get('last_name')
    user.save()


from registration.signals import user_registered
user_registered.connect(user_created)




def buskadorProducte(request):

    searchString = request.POST.get('searchString', 0)
    #ToDo Afegir Cela al Buscador, Django no permet Ands i Ors, Construir query manualment

    etiquetes = Etiqueta.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()
    # if searchString:
    posts = Producte.objects.filter((Q(nom__icontains = searchString) | Q(descripcio__icontains = searchString) | Q(keywords__icontains = searchString)), nodes__id__exact=user_p.lloc_entrega_perfil.pk )

    return render(request, "buscador.html", {
        'posts': posts,
        'etiquetes': etiquetes, 'up': user_p})





def nouUsuariView(request):

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    u_key = Key.objects.get(nou_usuari=request.user)
    u = UserProfile.objects.get(user=u_key.usuari)
    s = u.lloc_entrega_perfil.get_frequencia()

    return render(request, "nouUsuari.html", {'up': user_p, 'nodes': nodes, 'frequencia': s.nom})


def coopeView(request):

    etiquetes = Etiqueta.objects.all()
    nodes = Node.objects.all()

    user_p = UserProfile.objects.filter(user=request.user).first()

    productes = Producte.objects.filter(nodes__id__exact=user_p.lloc_entrega_perfil.pk, esgotat=False)

    notif=[]
    if request.user.is_authenticated():
        notif = request.user.notifications.unread()

    return render(request, "productes.html", {'productes':productes,'notifications': notif, 'etiquetes': etiquetes, 'up': user_p, 'nodes': nodes})


def producteView(request,pk):

    producte = Producte.objects.filter(pk=pk).first()
    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()
    return render(request, "producte.html",{'producte': producte, 'nodes': nodes, 'up': user_p})

def etiquetaView(request,pk):

    etiquetes = Etiqueta.objects.all()
    etiqueta = Etiqueta.objects.filter(pk=pk).first()

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    productes = Producte.objects.filter(etiqueta=etiqueta, nodes__id__exact=user_p.lloc_entrega_perfil.pk, esgotat=False)

    return render(request, "productes.html",{'productes': productes, 'etiquetes': etiquetes, 'nodes': nodes, 'up': user_p})


def productorView(request,pk):

    productor = Productor.objects.filter(pk=pk).first()
    productes = Producte.objects.filter(productor=productor)
    return render(request, "productor.html",{'productor': productor, 'productes': productes})

def comandesView(request):

    now = datetime.datetime.now()
    comandes = Comanda.objects.filter(client=request.user).filter(Q(data_entrega__gte=now)|Q(data_entrega__isnull=True)).order_by('-data_comanda')
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__gte=now)|Q(data_fi__isnull=True)).order_by('-data_comanda')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "comandes.html",{'comandes': comandes, 'nodes': nodes,'contractes':contractes, 'up': user_p })


def entregasView(request):

    now = datetime.datetime.now()
    entregas = Comanda.objects.filter(client=request.user).filter(Q(data_entrega__lte=now)).order_by('-data_comanda')
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__lte=now) & Q(data_fi__isnull=False)).order_by('-data_fi')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()

    return render(request, "entregas.html",{'comandes': entregas, 'contractes': contractes, 'nodes': nodes, 'up': user_p})

def comandaDelete(request, pk):

    comandaDel = Comanda.objects.filter(pk=pk).first()

    time = timedelta(hours=48)
    tt = comandaDel.data_entrega - time
    if datetime.datetime.date(datetime.datetime.now()) < tt.date():
        notify.send(comandaDel.producte, recipient = request.user,  verb="Has tret ",
            description="de la cistella" , url=comandaDel.producte.adjunt.url, timestamp=timezone.now())
        comandaDel.delete()
    else:
        messages.error(request, (u"Falten menys de 48h, no podem treure el producte de la cistella"))

    comandes = Comanda.objects.filter(client=request.user).filter(Q(data_entrega__gte=datetime.datetime.now())|Q(data_entrega__isnull=True)).order_by('-data_comanda')
    now = datetime.datetime.now()
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__gte=now)|Q(data_fi__isnull=True)).order_by('-data_comanda')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()



    return render(request, "comandes.html",{'comandes': comandes, 'contractes': contractes, 'nodes': nodes, 'up': user_p})

def contracteDelete(request, pk):

    contracteDel = Contracte.objects.filter(pk=pk).first()

    notify.send(contracteDel.producte, recipient = request.user,  verb="Has tret ",
          description="de la cistella" , url=contracteDel.producte.adjunt.url, timestamp=timezone.now())

    contracteDel.data_fi = datetime.datetime.now()
    contracteDel.save()

    comandes = Comanda.objects.filter(client=request.user).filter(Q(data_entrega__gte=datetime.datetime.now())|Q(data_entrega__isnull=True)).order_by('-data_comanda')
    now = datetime.datetime.now()
    contractes = Contracte.objects.filter(client=request.user).filter(Q(data_comanda__gte=now)|Q(data_fi__isnull=True)).order_by('-data_comanda')

    nodes = Node.objects.all()
    user_p = UserProfile.objects.filter(user=request.user).first()


    return render(request, "comandes.html",{'comandes': comandes, 'contractes': contractes, 'nodes': nodes, 'up': user_p})




def AjudaView(request):

    user_p = UserProfile.objects.filter(user=request.user).first()
    nodes = Node.objects.all()

    return render(request, "ajuda.html",{'up': user_p, 'nodes': nodes})



from django.http import HttpResponse

from django.views.generic.edit import FormView
from .models import Comanda
from .forms import ComandaForm

class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

class ComandaFormBaseView(FormView):
    form_class = ComandaForm


    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        producte = get_object_or_404(Producte, pk=form.data["producte_pk"])
        user = self.request.user
        format = get_object_or_404(TipusProducte, pk=form.data["format_pk"])
        user_profile = UserProfile.objects.filter(user = user).first()
        cantitat = form.data["cantitat_t"]
        preu_aux = format.preu
        preu = preu_aux * float(cantitat)
        data = form.data["dataentrega"]
        frequencia = form.data["frequencia"]
        freq_txt = Frequencia.objects.filter(num=frequencia).first().nom
        data_entrega = DiaEntrega.objects.get(pk=data)
        data_entrega_txt = data_entrega.dia()
        data_entrega_num = data_entrega.dia_num()
        franja_pk = form.data["franjes"]
        franja = FranjaHoraria.objects.get(pk=franja_pk)

        format.stock = format.stock - int(cantitat)
        format.save()

        lloc = form.data["lloc_entrega"]
        lloc_obj = get_object_or_404(Node, pk = lloc)
        user_profile.lloc_entrega_perfil = lloc_obj
        # Aqui esta hardcodejat els llocs que son "a domicili", s'ha d'introduir el pk en el if de qualsevol node nou "a domicili"
        if (lloc_obj.a_domicili == True):

            user_profile.carrer = form.data["carrer"]
            user_profile.numero = form.data["numero"]
            user_profile.pis = form.data["pis"]
            user_profile.poblacio = form.data["poblacio"]
        user_profile.save()



        if frequencia == '0':
            v = Comanda.objects.create(client=user, producte=producte, cantitat=cantitat, format=format, data_entrega= data_entrega.date , data_entrega_txt=data_entrega_txt, franja_horaria=franja, lloc_entrega=user_profile.lloc_entrega_perfil, preu=preu)
        else:
            v = Contracte.objects.create(client=user, producte=producte, cantitat=cantitat, format=format, primera_entrega=data_entrega.date ,data_entrega=data_entrega_num, data_entrega_txt=data_entrega_txt, franja_horaria=franja, lloc_entrega=user_profile.lloc_entrega_perfil, preu=preu, freq_txt=freq_txt, frequencia=frequencia)


        ret = {"success": 1}
        notify.send(producte, recipient= user, verb="Has afegit ", action_object=v,
                  description="a la cistella" , timestamp=timezone.now())

        messages.success(self.request, (u"Comanda realitzada correctament"))


        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)



class ComandaFormView(JSONFormMixin, ComandaFormBaseView):
    pass

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
    for i in Node.objects.all():

        if i == u.lloc_entrega_perfil:
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

    text = nom + " t'ha convidat a la xarxa de productes de proximitat del Baix Vallès "+ "http://127.0.0.1:8000/register/" + str(k)
    send_mail("Convidat a la xarxa d'autogestio", text, 'RUSC@example.com', [email] ,fail_silently=True )

#en cas de que si estigui, enviar invitació al usuari
def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


# def buskadorProducte(request):
#
#     searchString = request.POST.get('searchString', 0)
#     #ToDo Afegir Cela al Buscador, Django no permet Ands i Ors, Construir query manualment
#     posts = Producte.objects.filter(Q(nom__icontains = searchString) | Q(descripcio__icontains = searchString) )
#
#     return render(request, "buscador.html", {'posts': posts})







def ConvidarView(request):

    up = UserProfile.objects.get(user = request.user)
    message_email = ""
    message = ""
    if request.POST:

        # a = request
        #
        email = request.POST.get('email')

        # ret = {}
        if email:
            #comprobem que els mails no estiguin donats de alta a la xarxa
            alta = User.objects.filter(email = email).first()
            if not alta:
                if validateEmail(email):
                    try:
                        k = generate_key(request)
                        enviarInvitacio(email, up.user.username, k)
                        up.invitacions = up.invitacions - 1

                        conv = Convidat.objects.create(mail = email)
                        conv.save()

                        up.convidats.add(conv)

                        up.save()

                        notify.send(up, recipient= up.user, verb="Has convidat un nou usuari ", action_object=up,
                            description="a la xarxa" , timestamp=timezone.now())
                        message_email = "S'ha enviat la sol·licitud al correu electrònic correctament"
                    # up = UserProfile.objects.get(user = request.user)
                    except:
                       message_email = "No s'ha pogut enviar la sol·licitud al correu electrònic"
                else:
                    # return HttpResponse(json.dumps(ret), content_type='application/json')
                    message_email = "No s'ha pogut enviar la sol·licitud al correu electrònic"
                # return HttpResponse(json.dumps(ret), content_type='application/json')
            else:
                message_email = "La direcció de correu electrònic ja té usuari a la xarxa"
        # cantitat = request.POST.get('cantitat')
        # lloc_entrega = request.POST.get('lloc_entrega')
        else:
            k = generate_key(request)
            up.invitacions = up.invitacions - 1
            up.save()
            s = "http://127.0.0.1:8000/register/" + str(k)
            message = s
            # return HttpResponse(json.dumps(ret))
    # response = HttpResponse(json.dumps(ret), content_type='application/json')
    # return response
    # return JsonResponse(ret)

    return render(request, "convidar.html", {'invitacions':up.invitacions, 'message':message, 'message_email': message_email})



def DomiciliView(request):



    if request.POST:

        if 'lloc_entrega_perfil' in request.POST:

            l = request.POST.get('lloc_entrega_perfil')
            node = get_object_or_404(Node, pk=l)
            up = UserProfile.objects.get(user=request.user)
            nf = node.get_frequencia()

            if node.a_domicili == True:
                json_obj = dict(carrer = up.carrer, numero = up.numero, pis = up.pis, poblacio = node.poblacio, a_domicili = node.a_domicili,
                                geopuntx_lat = up.punt_lat, geopuntx_lng = up.punt_lng, frequencia = nf.nom)
            else:
                json_obj = dict(carrer = node.carrer, numero = node.numero, pis = node.pis, poblacio = node.poblacio, a_domicili = node.a_domicili,
                                geopuntx_lat = str(node.position.latitude), geopuntx_lng = str(node.position.longitude), frequencia = nf.nom )

            return HttpResponse(json.dumps(json_obj), content_type='application/json')

        if 'lloc_entrega' in request.POST:

            l = request.POST.get('lloc_entrega')
            node = get_object_or_404(Node, pk=l)
            up = UserProfile.objects.get(user=request.user)
            # json_obj = []
            if node.a_domicili == True:
                json_obj = dict(carrer = up.carrer, numero = up.numero, pis = up.pis, poblacio = node.poblacio, a_domicili = node.a_domicili)
            else:
                json_obj = dict(carrer = node.carrer, numero = node.numero, pis = node.pis, poblacio = node.poblacio, a_domicili = node.a_domicili)

            return HttpResponse(json.dumps(json_obj), content_type='application/json')

        if 'lloc_entrega_reg' in request.POST:

            l = request.POST.get('lloc_entrega_reg')
            node = get_object_or_404(Node, pk=l)
            up = UserProfile.objects.get(user=request.user)
            nf = node.get_frequencia()

            if node.a_domicili == True:
                json_obj = dict(poblacio = node.poblacio, a_domicili = node.a_domicili, frequencia = nf.nom)
            else:
                json_obj = dict(carrer = node.carrer, numero = node.numero, pis = node.pis, poblacio = node.poblacio, a_domicili = node.a_domicili,
                                geopuntx_lat = str(node.position.latitude), geopuntx_lng = str(node.position.longitude), frequencia = nf.nom )

            return HttpResponse(json.dumps(json_obj), content_type='application/json')


def NodeHorariView(request):

    if request.POST:

        if 'lloc_entrega_perfil' in request.POST:

                l = request.POST.get('lloc_entrega_perfil')
                node = get_object_or_404(Node, pk=l)

                v = node.dies_entrega.filter(date__gt = datetime.datetime.today()).first()

                if v:

                    json_res = []
                    d = v.date + timedelta(days=7)
                    k = node.dies_entrega.filter(date__lt = d, date__gt = datetime.datetime.today()).order_by('date')
                    for dia in k:
                        json_res_aux = []
                        for franja in dia.franjes_horaries.all():
                            json_obj_aux = dict(
                                inici = franja.inici,
                                final = franja.final,
                                pk = franja.pk
                            )
                            json_res_aux.append(json_obj_aux)


                        json_obj = dict(
                            dia = str(dia.dia()),
                            pk = dia.pk,
                            franjes = json_res_aux)
                        json_res.append(json_obj)

                    return HttpResponse(json.dumps(json_res), content_type='application/json')

        if 'lloc_entrega_reg' in request.POST:

                l = request.POST.get('lloc_entrega_reg')
                node = get_object_or_404(Node, pk=l)

                v = node.dies_entrega.filter(date__gt = datetime.datetime.today()).first()

                if v:

                    json_res = []
                    d = v.date + timedelta(days=7)
                    k = node.dies_entrega.filter(date__lt = d, date__gt = datetime.datetime.today()).order_by('date')
                    for dia in k:
                        json_res_aux = []
                        for franja in dia.franjes_horaries.all():
                            json_obj_aux = dict(
                                inici = franja.inici,
                                final = franja.final,
                                pk = franja.pk
                            )
                            json_res_aux.append(json_obj_aux)


                        json_obj = dict(
                            dia = str(dia.dia()),
                            pk = dia.pk,
                            franjes = json_res_aux)
                        json_res.append(json_obj)

                    return HttpResponse(json.dumps(json_res), content_type='application/json')


    else:
        up = UserProfile.objects.filter(user = request.user).first()

        if up.lloc_entrega_perfil:
            node = up.lloc_entrega_perfil
        else:
            k = Key.objects.filter(nou_usuari = request.user).first()
            up2 = UserProfile.objects.filter(user = k.usuari).first()
            node = up2.lloc_entrega_perfil

        v = node.dies_entrega.filter(date__gt = datetime.datetime.today()).first()

        if v:
            json_res = []
            d = v.date + timedelta(days=7)
            k = node.dies_entrega.filter(date__lt = d, date__gt = datetime.datetime.today()).order_by('date')
            for dia in k:
                json_res_aux = []
                for franja in dia.franjes_horaries.all():
                    json_obj_aux = dict(
                        inici = franja.inici,
                        final = franja.final,
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

    if 'lloc_entrega_reg' in request.POST:
        l = request.POST.get('lloc_entrega_reg')
        node = get_object_or_404(Node, pk=l)
    elif 'lloc_entrega_perfil' in request.POST:
        l = request.POST.get('lloc_entrega_perfil')
        node = get_object_or_404(Node, pk=l)
    else:
        l = request.POST.get('lloc_entrega_perfil')



    json_obj = dict(
        Lat = str(node.position.latitude),
        Lng = str(node.position.longitude)
    )

    return HttpResponse(json.dumps(json_obj), content_type='application/json')

def AllCoordenadesView(request):



        nodes = Node.objects.all()

        json_res = []

        for node in nodes:

            # if node.a_domicili == False:
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

        if 'lloc_entrega_reg' in request.POST:
            # if 'nom_complet' in request.POST:
            #     o = request.POST.get('nom_complet')
                l = request.POST.get('lloc_entrega_reg')
                node = get_object_or_404(Node, pk=l)
                v.lloc_entrega_perfil = node

                if 'poblaciox' in request.POST:
                    v.poblacio = request.POST.get('poblaciox')

                if node.a_domicili == True:
                    if 'carrerx' in request.POST:
                        v.carrer = request.POST.get('carrerx')
                    if 'numerox' in request.POST:
                        v.numero = request.POST.get('numerox')
                    if 'pisx' in request.POST:
                        v.pis = request.POST.get('pisx')
                    if 'punt_latx' in request.POST:
                        v.punt_lat = request.POST.get('punt_latx')
                    if 'punt_lngx' in request.POST:
                        v.punt_lng = request.POST.get('punt_lngx')
                # if o != "":
                #     v.nom_complet = o
                v.save()



                return HttpResponse(json.dumps("OK"), content_type='application/json')

from datetime import timedelta

def NodeCalcView(request):
    if request.POST:
        if 'lloc_entrega' in request.POST:
            l = request.POST.get('lloc_entrega')
            g = request.POST.get('producte_pk')
            node = get_object_or_404(Node, pk=l)
            producte = Producte.objects.filter(pk=g).first()
            json_res = []
            date = datetime.date.today() + timedelta(hours=48)
            for dia in node.dies_entrega.filter(date__gt =date)[0:5]:
                if dia in producte.dies_entrega.all():
                    a = datetime.datetime.strptime(str(dia.date.date()), '%Y-%m-%d').strftime('%d/%m/%Y')
                    json_obj = dict(
                        dia = dia.dia(),
                        date = a,
                        pk = dia.pk)
                    json_res.append(json_obj)
            return HttpResponse(json.dumps(json_res), content_type='application/json')

def FreqCalcView(request):
    if request.POST:
        if 'lloc_entrega' in request.POST:
            l = request.POST.get('lloc_entrega')
            g = request.POST.get('producte_pk')
            node = get_object_or_404(Node, pk=l)
            producte = Producte.objects.filter(pk=g).first()
            json_res = []
            for f in node.frequencies.all():
                if f in producte.frequencies.all():
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
                        inici = franja.inici,
                        final = franja.final,
                        pk = franja.pk
                    )
                    json_res.append(json_obj)
                return HttpResponse(json.dumps(json_res), content_type='application/json')
    return HttpResponse("NO")




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
        user_profile = UserProfile.objects.filter(user = user).first()
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
        ret["imatge"] = producte.adjunt.url


        json_res = []
        jfreq = []
        # Carreguem els possibles nodes on l-usuari pot trobar el producte concret
        for i in producte.nodes.all():
            if i == user_profile.lloc_entrega_perfil:
                # Guardem les frequencies del node per informar a l-usuari en el modal
                for d in i.frequencies.all():
                    if d in producte.frequencies.all():
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

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super(UserProfileEditView, self).get_context_data(**kwargs)
        nodes = Node.objects.all()
        context['nodes'] = nodes
        now = datetime.datetime.now()
        comandes = Comanda.objects.filter(client=self.request.user).filter(Q(data_entrega__gte=now)|Q(data_entrega__isnull=True)).order_by('-data_comanda')
        contractes = Contracte.objects.filter(client=self.request.user).filter(Q(data_comanda__gte=now)|Q(data_fi__isnull=True)).order_by('-data_comanda')
        context['comandes'] = comandes
        context['contractes']  = contractes
        u = UserProfile.objects.get(user=self.request.user)
        s = u.lloc_entrega_perfil.get_frequencia()
        if s:
            context['frequencia'] = s.nom
        else:
            f = Frequencia.objects.get(num=0)
            context['frequencia'] = f.nom
        return context


    def get_success_url(self):
        notify.send(self.object, recipient= self.object.user, verb="Has modificat les teves dades ", action_object=self.object,
        description="" , timestamp=timezone.now())

        messages.success(self.request, (u"S'han desat les modificacions realitzades"))
        return reverse("coope")
