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