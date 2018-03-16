from distutils.command.config import config
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from geoposition.fields import GeopositionField
import datetime, random
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from datetime import timedelta
from PIL import Image
import os
from django.template.defaultfilters import filesizeformat
import magic
from django.core.files import File
# from romani.public_views import stock_calc

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
        content_type = magic.from_buffer(fieldfile_obj.file.read(), mime=True)
        if content_type != 'image/jpeg':
            # params = { 'content_type': content_type }
            raise ValidationError("La foto ha de ser en format d'imatge")


    arxiu = models.FileField(upload_to='documents/%Y/%m/%d', null=True, validators=[validate_file])
    productor = models.ForeignKey(Productor, related_name='adjunts')


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
    numero = models.CharField(max_length=10, blank=True, null=True)
    pis = models.CharField(max_length=15, blank=True, null=True)
    poblacio = models.CharField(max_length=40, blank=False, null=False)
    codi_postal = models.CharField(max_length=5, blank=True, null=True)
    frequencia = models.ForeignKey(Frequencia)
    responsable = models.ManyToManyField(User, blank=False)
    a_domicili = models.NullBooleanField()
    text = models.TextField(max_length=1000)
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

    # def franja(self):
    #     return self.franja_inici().inici

    # def next(self, productor):
    #     next_d_tab = DiaEntrega.objects.filter(date__gte=self.date, node__productors=productor).exclude(pk=diaentrega.pk).first()
    #     sorted_results = sorted(next_d_tab, key= lambda t: t.thing_date())



class Etiqueta(models.Model):
    nom = models.CharField(max_length=15)
    img = models.FileField(upload_to='etiquetes')

    def __str__(self):
        return self.nom


class Producte(models.Model):

    def validate_file(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        # filetype = fieldfile_obj.file.content_typè
        megabyte_limit = 2.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        content_type = magic.from_buffer(fieldfile_obj.file.read(), mime=True)
        if content_type != 'image/jpeg':
            # params = { 'content_type': content_type }
            raise ValidationError("La foto ha de ser en format d'imatge")

    nom = models.CharField(max_length=20)
    etiqueta = models.ForeignKey(Etiqueta)
    text_curt = models.TextField(blank=False, max_length=75)
    descripcio = models.TextField(blank=True, default="")
    datahora = models.DateTimeField(auto_now_add=True)
    foto = models.FileField(upload_to='productes/%Y/%m/%d', null=True, validators=[validate_file])
    thumb = models.FileField(blank=True, null=True)
    productor = models.ForeignKey(Productor)
    keywords = models.TextField(blank=True, verbose_name='Paraules Clau')
    frequencies = models.ForeignKey(Frequencia)
    # karma_date = models.DateTimeField(blank=True, null=True)
    # karma_value = models.IntegerField(blank=True, null=True)

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
        next_day = self.next_day_sec(node)
        if next_day['result'] == True:
            karma_value = com +  rnd + self.positive_votes() - self.negative_votes() - next_day['next_day']
        else:
            karma_value = com +  rnd + self.positive_votes() - self.negative_votes()
        # self.save()
        return karma_value

    def next_day_sec(self, node):
        list = []
        for f in self.formats.all():
            for s in f.dies_entrega.filter(dia__date__gte=datetime.datetime.now(), dia__node=node).order_by('dia__date'):
                date = datetime.datetime.now() + timedelta(hours=s.hores_limit)
                aux = s.dia.franja_inici()
                daytime = datetime.datetime(s.dia.date.year, s.dia.date.month, s.dia.date.day, aux.inici.hour, aux.inici.minute)

                if daytime > date:
                    res = s.format.stock_calc(s.dia, 1)
                    if res['result'] == True:
                        list.append(daytime)
                        break
        if list:
            list.sort(key=lambda r: r)
            b = list[0]
            a = datetime.datetime.now()
            c = b - a
            dict = {'result': True, 'next_day': c.total_seconds()}
            return dict
        else:
            dict = {'result': False}
            return dict

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Producte, self).save()
        size = 250, 250
        image = Image.open(self.foto.path)
        image.thumbnail(size)
        image.save(self.foto.path + ".jpeg")
        self.thumb.name = self.foto.name + ".jpeg"
        super(Producte, self).save()
        # quality = (20 / int(os.stat(self.thumb.path).st_size))*100
        # if quality < 100:
        #     image = Image.open(self.thumb.path)
        #     image.save(self.thumb.path, optimize=True, quality=quality)

        # image.save("media/productes/temp/" + self.nom + ".jpeg")
        # image = image.resize((250,250),Image.ANTIALIAS)
        # image.save(self.thumb.path,quality=20,optimize=True)



# class TipusProducteManager(models.Manager):
#     def get_by_natural_key(self, nom, preu):
#         return self.get(nom=nom, preu=preu)


class TipusProducte(models.Model):

    # objects = TipusProducteManager()

    nom = models.CharField(max_length=20)
    preu = models.FloatField(default=0.0)
    productor = models.ForeignKey(Productor)
    producte = models.ForeignKey(Producte, related_name='formats', blank=True, null=True)

    # def natural_key(self):
    #     return (self.nom, self.preu)
    #
    # class Meta:
    #     unique_together = (('nom', 'preu'),)

    # def __unicode__(self):
    #     return '%d: %s' % (self.nom, self.preu)

    def __str__(self):
        return "%s %s" % (self.producte, self.nom)

    def en_stock(self, cantitat, lloc_entrega):
        diesformat = self.dies_entrega.filter(dia__date__gte=datetime.datetime.now(), dia__node=lloc_entrega)
        for d in diesformat:
            date = datetime.datetime.now() + timedelta(hours=d.hores_limit)
            aux = d.dia.franja_inici()
            daytime = datetime.datetime(d.dia.date.year, d.dia.date.month, d.dia.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                 if d.tipus_stock == '0':
                        # Límit per stock...
                        try:
                            stocks = Stock.objects.filter((Q(dia_prod__node=d.dia.node)|Q(dia_prod__node=None)), dia_prod__date__lte=d.dia.date, dia_prod__caducitat__gte=d.dia.date, format=self).order_by('-dia_prod__node','dia_prod__caducitat','dia_prod__date')
                            for s in stocks:
                                # accedim al dia de producció en que es genera el estoc
                                diaproduccio = s.dia_prod
                                s = stocks.get(dia_prod=diaproduccio)
                                num = int(s.stock()) - int(cantitat)
                                if num >= 0:
                                   #  I si encara hi ha estoc disponible,confirmem existències
                                    return True
                        except:
                            # Si ni tan sols 'ha creat el estoc...
                            pass
                 elif d.tipus_stock == '2':
                        # Si el estoc és sense límit, aleshores confirmem que hi ha existències
                        return True
        return False

    def dies_entrega_futurs(self, cantitat):
        d_lst = []
        diesformat = self.dies_entrega.filter(dia__date__gte=datetime.datetime.now())
        for d in diesformat:
            date = datetime.datetime.now() + timedelta(hours=d.hores_limit)
            aux = d.dia.franja_inici()
            daytime = datetime.datetime(d.dia.date.year, d.dia.date.month, d.dia.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                 if d.tipus_stock == '0':
                        # Límit per stock...
                        try:
                            stocks = Stock.objects.filter((Q(dia_prod__node=d.dia.node)|Q(dia_prod__node=None)), dia_prod__date__lte=d.dia.date, dia_prod__caducitat__gte=d.dia.date, format=self).order_by('-dia_prod__node','dia_prod__caducitat','dia_prod__date')
                            for s in stocks:
                                # accedim al dia de producció en que es genera el estoc
                                diaproduccio = s.dia_prod
                                s = stocks.get(dia_prod=diaproduccio)
                                num = int(s.stock()) - int(cantitat)
                                if num >= 0:
                                   #  I si encara hi ha estoc disponible,confirmem existències
                                    d_lst.append(d.dia.pk)
                                    break
                        except:
                            # Si ni tan sols 'ha creat el estoc...
                            pass

                 elif d.tipus_stock == '2':
                        # Si el estoc és sense límit, aleshores confirmem que hi ha existències
                        d_lst.append(d.dia.pk)
        return DiaEntrega.objects.filter(pk__in = d_lst)

    def nodes(self, cantitat):
        return Node.objects.filter(dies_entrega__in=self.dies_entrega_futurs(cantitat)).distinct()

    def stock_calc(self, dia, cantitat):
         d = self.dies_entrega.get(dia=dia)
         # Segons el tipus d'stock..(pot ser "Limit per stock" o "Sense Límit")
         if d.tipus_stock == '0':
                # Límit per stock...
                try:
                    stocks = Stock.objects.filter((Q(dia_prod__node=dia.node)|Q(dia_prod__node=None)), dia_prod__date__lte=dia.date, dia_prod__caducitat__gte=dia.date, format=self).order_by('-dia_prod__node','dia_prod__caducitat','dia_prod__date')
                    for s in stocks:
                        # accedim al dia de producció en que es genera el estoc
                        diaproduccio = s.dia_prod
                        s = self.stocks.get(dia_prod=diaproduccio)
                        num = int(s.stock()) - int(cantitat)
                        if num >= 0:
                           #  I si encara hi ha estoc disponible,confirmem existències
                           dict = {'result': True, 'dia_prod': diaproduccio}
                           return dict
                    # Si tots els estocs shan esgotat.Confirmem que no hi ha existències.
                    dict = {'result': False, 'dia_prod': ''}
                    return dict

                except:
                    # Si ni tan sols 'ha creat el estoc. Confirmem que no hi ha existències
                    dict = {'result': False, 'dia_prod': ''}
                    return dict

         elif d.tipus_stock == '2':
                # Si el estoc és sense límit, aleshores confirmem que hi ha existències
                dict = {'result': True, 'dia_prod': ''}
                return dict

class DiaFormatStock(models.Model):
    TIPUS_STOCK = (
        ('0', 'Limit per stock'),
        ('2', 'Sense Limit')
    )


    dia = models.ForeignKey(DiaEntrega, related_name='formats')
    tipus_stock = models.CharField(max_length=10, choices=TIPUS_STOCK, default='2')
    format = models.ForeignKey(TipusProducte, related_name='dies_entrega')
    hores_limit = models.IntegerField()



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

    def __str__(self):
        return "%s %s" % (self.dia_entrega.date, self.franja_horaria)



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
        return "%s" % (self.usuari.username)


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

    carrer = models.CharField(max_length=50, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    pis = models.CharField(max_length=15, blank=True, null=True)
    poblacio = models.CharField(max_length=40, blank=True, null=True)

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
    text = models.TextField(blank=True)

    def __unicode__(self):
        return "%s voted %s" % (self.voter.username, self.link.title)

from django.core.mail import send_mail


def create_profile(sender, instance, created, **kwargs):
    if created:
        node = Node.objects.get(pk=1)
        # Aqui encara no podem mirar el key per esbrinar el lloc_entrega de l'usuari que l'ha convidat,de moment assignem node 1 i a MyRegistrationView succes_url modifiquem la taula Key,
        # despres al procesar nou_usuari en nodes_nou_usuari ja es calcula el node de l'usuari que convida i se li proposa en pantalla
        text = "El registre s'ha completat amb èxit. Benvingut a La Massa. Visita la web i descobreix tots els productes que tens al teu abast:  https://www.lamassa.org/   Gràcies!"
        # try:
        send_mail("Benvingut a La Massa", text, 'lamassaxarxa@gmail.com', [instance.email] ,fail_silently=True )

        profile, created = UserProfile.objects.get_or_create(user=instance, carrer="", numero="", poblacio="", pis="", lloc_entrega=node )




from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)




