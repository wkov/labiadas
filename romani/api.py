from django.http import JsonResponse
from .models import Producte, UserProfile
from .serializers import ProducteSerializer
from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
# def jwt_payload_handler(token, user=None, request=None):
#     return {
#         'token': token,
#         'user': UserSerializer(user, context={'request': request}).data
#     }

@csrf_exempt
def get_product_list(request):
    """
    List all restaurants
    """
    product_list = Producte.objects.filter(productor__pk='1')
    serializer = ProducteSerializer(product_list, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def get_user(request):
    """
    List all restaurants
    """
    user = UserProfile.objects.filter(user=request.user)
    serializer = UserSerializer(user, many=True)
    return JsonResponse(serializer.data, safe=False)



from rest_framework import views, serializers, status
from rest_framework.response import Response
class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)