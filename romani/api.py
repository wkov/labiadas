from django.http import JsonResponse
from .models import Producte, UserProfile
from .serializers import ProducteSerializer, UserProfileSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@csrf_exempt
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

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
    serializer = UserProfileSerializer(user, many=True)
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