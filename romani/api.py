from django.http import JsonResponse
from .models import Producte, UserProfile, Etiqueta, Node, TipusProducte, DiaFormatStock, Entrega, Comanda, Productor
from .models import FranjaHoraria, DiaEntrega
from .serializers import ProducteSerializer, UserProfileSerializer, EtiquetaSerializer, FormatSerializer, \
    ComandaSerializer, ProductorSerializer, NodeSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import datetime
from datetime import timedelta
from rest_framework.decorators import parser_classes
from django.db.models import Q

from django.contrib.auth.models import User

from rest_framework.parsers import JSONParser
from rest_framework.response import Response

@api_view(['POST'])
@parser_classes((JSONParser,))
def example_view(request):
    """
    A view that can accept POST requests with JSON content.
    """
    dict={}
    dict = request.data
    user = request.user
    up = UserProfile.objects.get(user=user)
    formats_dis, productes_dis = x_disponibles(up)
    formats = TipusProducte.objects.filter(pk__in=formats_dis).distinct()
    log = ""
    if 'first_name' in dict:
        user.first_name = dict['first_name']
        user.save()
        log = "OK"
        user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
        return Response({'log': log, 'user_profile': user_profile.data})
    elif 'email' in dict:
        user.email = dict['email']
        user.save()
        log = "OK"
        user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
        return Response({'log': log, 'user_profile': user_profile.data})
    elif 'last_name' in dict:
        user.last_name = dict['last_name']
        user.save()
        log = "OK"
        user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
        return Response({'log': log, 'user_profile': user_profile.data})
    elif 'username' in dict:
        try:
            other_user = User.objects.get(username=dict['username'])
            log = "KO"
            user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
            return Response({'log': log, 'user_profile': user_profile.data})

        except:
                user.username = dict['username']
                user.save()
                log = "OK"
                user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
                return Response({'log': log, 'user_profile': user_profile.data})
    elif 'phone_number' in dict:
        up.phone_number = dict['phone_number']
        up.save()
        log = "OK"
        user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
        return Response({'log': log, 'user_profile': user_profile.data})
    elif 'poblacio' in dict:
        up.poblacio = dict['poblacio']
        up.save()
        log = "OK"
        user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
        return Response({'log': log, 'user_profile': user_profile.data})
    elif 'direccio' in dict:
        up.direccio = dict['direccio']
        up.save()
        log = "OK"
        user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
        return Response({'log': log, 'user_profile': user_profile.data})
    elif 'lloc_entrega' in dict:
        lloc = dict['lloc_entrega']
        lloc_entrega = Node.objects.get(pk=lloc['pk'])
        up.lloc_entrega = lloc_entrega
        up.save()
        log = "OK"
        user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
        return Response({'log': log, 'user_profile': user_profile.data})
    elif 'preferits' in dict:
        try:
            is_favorite = up.preferits.get(pk=dict['preferits'])
            up.preferits.remove(is_favorite)
            log = "OK"
            user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
            return Response({'log': log, 'user_profile': user_profile.data})

        except:
                producte = Producte.objects.get(pk=dict['preferits'])
                up.preferits.add(producte)
                # user.save() ALBERTO COMMENT PARA MERGE
                log = "OK"
                user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
                return Response({'log': log, 'user_profile': user_profile.data})

    elif 'comanda' in dict:
        errors = {}
        com = dict['comanda']
        v = Comanda.objects.create(client=user, cantitat=com['cantitat'], format=com['format'], node=up.lloc_entrega, preu=com['preu'])
        for d in com['entregas']:
            dia = DiaEntrega.objects.get(pk=d)
            stock_result = v.format.stock_calc(dia, com.cantitat)
            if stock_result['result'] == True:
                franja_pk = request.POST.get(str(dia.pk))
                franja = FranjaHoraria.objects.get(pk=franja_pk)
                if stock_result['dia_prod'] == '':
                    e = Entrega.objects.create(dia_entrega=dia, comanda=v, franja_horaria=franja)
                else:
                    e = Entrega.objects.create(dia_entrega=dia, comanda=v, franja_horaria=franja,
                                               dia_produccio=stock_result['dia_prod'])
            else:
                log = "CHECK"
                errors[dia.pk] = {'dia': dia.date}
                return Response({'log': log, 'errors': errors})
        log = "OK"
        comanda = ComandaSerializer(v)
        return Response({'log': log, 'comanda': comanda.data})

    elif 'comanda_delete' in dict:
        com_del = dict['comanda_delete']
        try:
            v = Comanda.objects.delete(pk=com_del)
            log = "OK"
        except:
            log = "KO"
        return Response({'log': log})
    log = "KO"
    user_profile = UserProfileSerializer(up, many=False, context={'userp_pk': up.pk, 'formats_dis': formats})
    return Response({'log': log, 'user_profile': user_profile.data})

    # serializer = ProducteSerializer(p, many=True)
    # return JsonResponse(serializer.data, safe=False)

    # return Response({'received data': request.data})

# @csrf_exempt
def jwt_payload_handler(token, user=None, request=None):
    up = UserProfile.objects.get(user=user)
    return {
        'token': token,
        'user': UserProfileSerializer(up, context={'request': request}).data
    }

@api_view(['GET'])
def get_product_list(request):
    """
    List all restaurants
    """
    user_p = UserProfile.objects.filter(user=request.user)

    data = {}
    etiquetes = get_etiquetes(request, user_p.first())
    productes, productors, user_profile = get_productes(request, user_p.first())

    comandes, historial = get_comandes(request)
    nodes = get_nodes(request)
    data['etiquetes'] = etiquetes.data
    # data['formats'] = formats.data
    data['comandes'] = comandes.data
    data['historial'] = historial.data
    data['productes']=productes.data
    data['productors']=productors.data
    data['user_profile']=user_profile.data
    data['nodes']=nodes.data

    # productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega), reverse=True)
    # product_list = Producte.objects.filter(productor__pk='1')

    return JsonResponse(data, safe=False)


def get_etiquetes(request, user_p):

    today = datetime.date.today()

    dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt=today)

    etiquetes_pre = Etiqueta.objects.all()

    etiquetes = set()

    for e in etiquetes_pre:
        for p in e.producte_set.all():
            for f in p.formats.all():
                for p2 in f.dies_entrega.all():
                    if p2.dia in dies_node_entrega:
                        etiquetes.add(e.pk)
                        break


    etq = Etiqueta.objects.filter(pk__in=etiquetes).distinct()
    etiquetes_serialized = EtiquetaSerializer(etq, many=True)
    return etiquetes_serialized


def get_comandes(request):

    now = datetime.datetime.now()
    entregas = Entrega.objects.filter(comanda__client=request.user, dia_entrega__date__gte=now)
    com = Comanda.objects.filter(entregas__in=entregas).distinct()
    entregas_hist = Entrega.objects.filter(comanda__client=request.user).filter(Q(dia_entrega__date__lte=now)).order_by('-dia_entrega__date', 'franja_horaria__inici')
    hist = Comanda.objects.filter(entregas__in=entregas_hist).distinct()
    # comandes = sorted(com, key=lambda a: (a.prox_entrega().dia_entrega.date, a.prox_entrega().franja_horaria.inici))
    comanda_serialized=ComandaSerializer(com, many=True)
    hist_serialized=ComandaSerializer(hist, many=True)
    return comanda_serialized, hist_serialized


def x_disponibles(user_p):
    today = datetime.date.today()
    dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt=today)

    productes_disponibles = set()
    formats_disponibles = set()

    for d in dies_node_entrega:
        for t in TipusProducte.objects.filter(dies_entrega__dia=d):
            diaformatstock = DiaFormatStock.objects.get(dia=d, format=t)
            date = datetime.datetime.now() + timedelta(hours=diaformatstock.hores_limit)
            aux = d.franja_inici()
            daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
            if daytime > date:
                stock_result = t.stock_calc(d, 1)
                if stock_result['result'] == True:
                    productes_disponibles.add(t.producte.pk)
                    formats_disponibles.add(t.pk)

    return formats_disponibles, productes_disponibles



def get_productes(request, user_p):


    formats_dis, productes_dis = x_disponibles(user_p)
    productes = Producte.objects.filter(pk__in=productes_dis).distinct()
    formats = TipusProducte.objects.filter(pk__in=formats_dis).distinct()
    productors = Productor.objects.filter(producte__pk__in=productes_dis).distinct()
    producte_serialized = ProducteSerializer(productes, many=True, context={'userp_pk': user_p.pk, 'formats_dis': formats})
    # formats_serialized = FormatSerializer(formats, many=True)
    productors_serialized = ProductorSerializer(productors, many=True)
    user_profile = UserProfileSerializer(user_p, context={'userp_pk': user_p.pk, 'formats_dis': formats})


    return producte_serialized, productors_serialized, user_profile



def get_nodes(request):

    nodes = Node.objects.exclude(pk=1)
    nodes_serialized = NodeSerializer(nodes, many=True)

    return nodes_serialized

# @csrf_exempt
# def get_user(request):
#     """
#     List all restaurants
#     """
#     user = UserProfile.objects.filter(user=request.user)
#     serializer = UserSerializer(user, many=True)
#     return JsonResponse(serializer.data, safe=False)



# from rest_framework import views, serializers, status
# from rest_framework.response import Response
# class MessageSerializer(serializers.Serializer):
#     message = serializers.CharField()
# class EchoView(views.APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = MessageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(
#             serializer.data, status=status.HTTP_201_CREATED)
