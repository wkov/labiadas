from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from geoposition.fields import GeopositionField
import datetime, random

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from datetime import timedelta


class Productor(models.Model):

    nom = models.CharField(max_length=20)
    responsable = models.ManyToManyField(User)
    text = models.TextField(blank=True)
    hores_limit = models.IntegerField(default=48)

    def __str__(self):
        return self.nom

    def comandes_count(self):
        now=datetime.datetime.now()
        cm = Entrega.objects.filter(comanda__format__producte__productor=self).filter(dia_entrega__date__gte=now).count()
        return cm



class Adjunt(models.Model):

    def validate_file(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


    arxiu = models.FileField(upload_to='documents/%Y/%m/%d', null=True, validators=[validate_file])
    productor = models.ForeignKey(Productor)


    def __str__(self):
        return self.arxiu.url


class Frequencia(models.Model):
    num = models.IntegerField()
    nom = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.nom)

    def freq_list(self):

        if self.num == 1:  #cada setmana
            return Frequencia.objects.filter(num__in = [1, 2, 3, 4, 5, 6])
        if self.num == 2:  #cada 2 setmanes
            return Frequencia.objects.filter(num__in = [2, 4, 5, 6])
        if self.num == 3:  #cada 3 setmanes
            return Frequencia.objects.filter(num__in = [3, 5, 6])
        if self.num == 4:  #cada 4 setmanes
            return Frequencia.objects.filter(num__in = [4, 5, 6])
        if self.num == 5:  #més d'una vegada
            return Frequencia.objects.filter(num__in = [5, 6])
        if self.num == 6:  #una sola vegada
            return Frequencia.objects.filter(num = 6)



class Node(models.Model):

    nom = models.CharField(max_length=20)
    position = GeopositionField(null=False, blank=False)
    carrer = models.CharField(max_length=50, blank=True, null=True)
    numero = models.CharField(max_length=5, blank=True, null=True)
    pis = models.CharField(max_length=15, blank=True, null=True)
    poblacio = models.CharField(max_length=40, blank=False, null=False)
    codi_postal = models.CharField(max_length=5, blank=True, null=True)
    responsable = models.ManyToManyField(User, null=False, blank=False)
    a_domicili = models.NullBooleanField()
    text = models.TextField(max_length=1000)
    frequencia = models.ForeignKey(Frequencia)
    productors = models.ManyToManyField(Productor, blank=True, related_name='nodes')
    # privat = models.NullBooleanField()

    def __str__(self):
        return "%s, %s" % (self.nom, self.poblacio)

    def prox_dias(self):
        return self.dies_entrega.filter(date__gte=datetime.datetime.now()).order_by('date')[0:6]

    def get_frequencia(self):
        return self.frequencia.freq_list().order_by('num').first()



class FranjaHoraria(models.Model):

    inici = models.TimeField()
    final = models.TimeField()

    node = models.ForeignKey(Node)

    def __str__(self):
        return "%s-%s" % (self.inici, self.final)


class DiaEntrega(models.Model):

    franjes_horaries = models.ManyToManyField(FranjaHoraria,  related_name="dia")
    date = models.DateField()
    node = models.ForeignKey(Node, related_name="dies_entrega")

    def __str__(self):
        a = datetime.datetime.strptime(str(self.date), '%Y-%m-%d').strftime('%d/%m/%Y')
        s = str(self.franja_inici())
        return " %s %s %s" % (self.node, str(a), str(s))

    def dia_num(self):
        return self.date.weekday()

    def dia(self):
        if self.date.strftime("%A") == "Monday":
            return "Dilluns"
        if self.date.strftime("%A") == "Tuesday":
            return "Dimarts"
        if self.date.strftime("%A") == "Wednesday":
            return "Dimecres"
        if self.date.strftime("%A") == "Thursday":
            return "Dijous"
        if self.date.strftime("%A") == "Friday":
            return "Divendres"
        if self.date.strftime("%A") == "Saturday":
            return "Dissabte"
        if self.date.strftime("%A") == "Sunday":
            return "Diumenge"

    def franja_inici(self):
        return self.franjes_horaries.order_by("inici").first()



class Etiqueta(models.Model):
    nom = models.CharField(max_length=15)
    img = models.FileField(upload_to='etiquetes')

    def __str__(self):
        return self.nom


class Producte(models.Model):

    def validate_file(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    nom = models.CharField(max_length=20)
    etiqueta = models.ForeignKey(Etiqueta)
    text_curt = models.TextField(blank=False, max_length=75)
    descripcio = models.TextField(blank=True, default="")
    datahora = models.DateTimeField(auto_now_add=True)
    foto = models.FileField(upload_to='documents/%Y/%m/%d', null=True, validators=[validate_file])
    productor = models.ForeignKey(Productor)
    keywords = models.TextField(blank=True)
    frequencies = models.ForeignKey(Frequencia)
    karma_date = models.DateTimeField(blank=True, null=True)
    karma_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nom

    def positive_votes(self):
        return Vote.objects.filter(entrega__comanda__format__producte=self).filter(positiu=True).count()

    def negative_votes(self):
        return Vote.objects.filter(entrega__comanda__format__producte=self).filter(positiu=False).count()

    def karma(self, node):
        com = 0
        for f in self.formats.all():
            com = com + f.comanda_set.filter(entregas__dia_entrega__node=node).count()
        rnd = random.randint(0, 5)
        self.karma_value = com +  rnd + self.positive_votes() - self.negative_votes()
        self.save()
        return self.karma_value



class TipusProducte(models.Model):

    nom = models.CharField(max_length=20)
    preu = models.FloatField(default=0.0)
    productor = models.ForeignKey(Productor)
    producte = models.ForeignKey(Producte, related_name='formats', blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.producte, self.nom)

    def in_stock(self):
        try:
            date = datetime.date.today() + timedelta(hours=self.productor.hores_limit)
            diesformat = self.dies_entrega.filter(dia__date__gte=date)
            for d in diesformat:
                if d.tipus_stock == '0':
                    try:
                        diaproduccio = DiaProduccio.objects.filter(date__lte=d.dia.date, productor=self.productor).order_by('-date').first()
                        if diaproduccio:
                           s = self.stocks.get(dia_prod=diaproduccio)
                           if s.stock() > 0:
                               return True
                    except:
                        pass

                elif d.tipus_stock == '2':
                    return True
        except:
            return False

    def dies_entrega_futurs(self):
        date = datetime.datetime.today() + timedelta(hours=self.productor.hores_limit)
        return DiaEntrega.objects.filter(date__gt=date, formats__format=self)

    def nodes(self):
        return Node.objects.filter(dies_entrega__in=self.dies_entrega_futurs()).distinct()

class DiaFormatStock(models.Model):
    TIPUS_STOCK = (
        ('0', 'Limit per stock'),
        ('2', 'Sense Limit')
    )


    dia = models.ForeignKey(DiaEntrega, related_name='formats')
    tipus_stock = models.CharField(max_length=10, choices=TIPUS_STOCK, default='2')
    format = models.ForeignKey(TipusProducte, related_name='dies_entrega')

    # def stock_check(self):
    #      d = self.format.dies_entrega.get(dia=self.dia)
    #      if d.tipus_stock == '0':
    #             try:
    #                 diaproduccio = DiaProduccio.objects.filter(date__lte=d.dia.date, productor=self.format.productor).order_by('-date').first()
    #                 if diaproduccio:
    #                    s = self.format.stocks.get(dia_prod=diaproduccio)
    #                    if s.stock() > 0:
    #                        return True
    #                    else:
    #                        return False
    #             except:
    #                 return False
    #
    #      elif d.tipus_stock == '2':
    #             return True



class DiaProduccio(models.Model):
    date = models.DateField()
    caducitat = models.DateField()
    productor = models.ForeignKey(Productor)
    node = models.ForeignKey(Node, blank=True, null=True)

    def __str__(self):
        return str(self.date)

class Stock(models.Model):

    dia_prod = models.ForeignKey(DiaProduccio, related_name='stocks')
    format = models.ForeignKey(TipusProducte, related_name='stocks')
    stock_ini = models.IntegerField()

    def stock(self):
        cant = 0
        entregas = Entrega.objects.filter(comanda__format=self.format, dia_produccio=self.dia_prod)
        for e in entregas:
            cant = e.comanda.cantitat + cant
        if cant > 0:
            return self.stock_ini-cant
        else:
            return self.stock_ini


class Comanda(models.Model):

    format = models.ForeignKey(TipusProducte)
    cantitat = models.PositiveIntegerField(blank=False)
    data_comanda = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(User)
    node = models.ForeignKey(Node)
    externa = models.NullBooleanField(blank=True)
    preu = models.FloatField(default=0.0)
    frequencia = models.ForeignKey(Frequencia)

    def __str__(self):
        return self.format.producte.nom

    def get_absolute_url(self):
        return reverse('comandes')

    def prox_entrega(self):
        return self.entregas.filter(dia_entrega__date__gte=datetime.datetime.today()).order_by('dia_entrega__date').first()




class Entrega(models.Model):

    dia_entrega = models.ForeignKey(DiaEntrega, related_name='entregas') #inclou el node
    comanda = models.ForeignKey(Comanda, related_name='entregas')
    data_comanda = models.DateTimeField(auto_now_add=True)

    dia_produccio = models.ForeignKey(DiaProduccio, related_name='entregas', blank=True, null=True) #Per el cas en que el estoc depèn d'un dia de producció concret
    franja_horaria = models.ForeignKey(FranjaHoraria, blank=True, null=True) #Per el cas en que és "a domicili!" obligat



#per a loguejarse amb el email
class EmailModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None



class Key(models.Model):
    key = models.CharField(max_length=6)
    usuari = models.ForeignKey(User)
    nou_usuari = models.ForeignKey(User, related_name='key_nou_usuari', null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.key, self.usuari.username, self.nou_usuari, self.data.date())


class UserProfile(models.Model):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    user = models.OneToOneField(User, unique=True, related_name='user_profile')
    bio = models.TextField(null=True, blank=True)
    lloc_entrega = models.ForeignKey(Node, blank=True, null=True)
    invitacions = models.IntegerField(default=4, blank=True, null=True)
    avatar = models.FileField(upload_to='profiles/%Y/%m/%d', validators=[validate_image], blank=True, null=True)

    carrer = models.CharField(max_length=30, blank=True, null=True)
    numero = models.CharField(max_length=5, blank=True, null=True)
    pis = models.CharField(max_length=10, blank=True, null=True)
    poblacio = models.CharField(max_length=30, blank=True, null=True)

    #
    # punt_lat = models.CharField(max_length=25, null=True, blank=True)
    # punt_lng = models.CharField(max_length=25, null=True, blank=True)

    def __unicode__(self):
        return  self.user.first_name

    def __str__(self):
        return self.user.first_name

    def comandes_cistella(self):  #per informar a l'usuari des del left_menu del num de comandes vigents que té a la cistella
        now = datetime.datetime.now()
        return Comanda.objects.filter(client=self.user).filter(entregas__dia_entrega__date__gte=now)


    def pro_entregas(self):  #per informar a l'usuari distribuidor en el boto en el left menu, del total d'entregues que sumen els seus productors
        now = datetime.datetime.now()
        return Entrega.objects.filter(comanda__format__producte__productor__responsable=self.user).filter(dia_entrega__date__gte=now)


class Vote(models.Model):
    voter = models.ForeignKey(User)
    entrega = models.ForeignKey(Entrega, related_name='vote')
    positiu = models.BooleanField()

    def __unicode__(self):
        return "%s voted %s" % (self.voter.username, self.link.title)

from django.core.mail import send_mail


def create_profile(sender, instance, created, **kwargs):
    if created:
        node = Node.objects.get(pk=1)
        # Aqui encara no podem mirar el key per esbrinar el lloc_entrega de l'usuari que l'ha convidat,de moment assignem node 1 i a MyRegistrationView succes_url modifiquem la taula Key,
        # despres al procesar nou_usuari en nodes_nou_usuari ja es calcula el node de l'usuari que convida i se li proposa en pantalla
        text = "El registre s'ha completat amb èxit. Benvingut a La Massa. Visita la web i descobreix tots els productes que tens al teu abast:  http://www.lamassa.org/   Gràcies!"
        # try:
        send_mail("Benvingut a La Massa", text, 'lamassaxarxa@gmail.com', [instance.email] ,fail_silently=True )

        profile, created = UserProfile.objects.get_or_create(user=instance, carrer="", numero="", poblacio="", pis="", lloc_entrega=node )




from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)



