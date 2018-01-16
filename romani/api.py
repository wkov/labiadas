from django.http import JsonResponse
from .models import Producte
from .serializers import ProducteSerializer
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def get_product_list(request):
    """
    List all restaurants
    """
    product_list = Producte.objects.filter(productor__pk='1')
    serializer = ProducteSerializer(product_list, many=True)
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