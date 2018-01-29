from django.http import JsonResponse
from .models import Producte, UserProfile
from .serializers import ProducteSerializer, UserProfileSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# @csrf_exempt
def jwt_payload_handler(token, user=None, request=None):
    up = UserProfile.objects.get(user=user)
    return {
        'token': token,
        'user': UserProfileSerializer(up, context={'request': request}).data
    }

@api_view(['POST'])
def get_product_list(request):
    """
    List all restaurants
    """
    # user_p = UserProfile.objects.filter(user=request.user).first()
    #
    # today = datetime.date.today()
    #
    # dies_node_entrega = user_p.lloc_entrega.dies_entrega.filter(date__gt=today)
    #
    # etiquetes_pre = Etiqueta.objects.all()
    #
    # etiquetes = set()
    #
    # for e in etiquetes_pre:
    #     for p in e.producte_set.all():
    #         for f in p.formats.all():
    #             for p2 in f.dies_entrega.all():
    #                 if p2.dia in dies_node_entrega:
    #                     etiquetes.add(e)
    #                     break
    #
    # nodes = Node.objects.all()
    #
    # prod_aux = set()
    # formats_aux = set()
    #
    # for d in dies_node_entrega:
    #     for t in TipusProducte.objects.filter(dies_entrega__dia=d):
    #         diaformatstock = DiaFormatStock.objects.get(dia=d, format=t)
    #         date = datetime.datetime.now() + timedelta(hours=diaformatstock.hores_limit)
    #         aux = d.franja_inici()
    #         daytime = datetime.datetime(d.date.year, d.date.month, d.date.day, aux.inici.hour, aux.inici.minute)
    #         if daytime > date:
    #             stock_result = t.stock_calc(d, 1)
    #             if stock_result['result'] == True:
    #                 prod_aux.add(t.producte.pk)
    #                 formats_aux.add(t)
    # p = Producte.objects.filter(pk__in=prod_aux).distinct()
    #
    # productes = sorted(p, key=lambda a: a.karma(node=user_p.lloc_entrega), reverse=True)



    product_list = Producte.objects.filter(productor__pk='1')
    serializer = ProducteSerializer(product_list, many=True)
    return JsonResponse(serializer.data, safe=False)

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