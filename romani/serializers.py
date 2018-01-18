from rest_framework import serializers
from romani.models import Producte, UserProfile


class ProducteSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)


    class Meta:
        model = Producte
        depth = 1
        fields = ('pk', 'nom', 'etiqueta', 'foto', 'productor', 'thumb', 'text_curt', 'formats')



class UserSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)


    class Meta:
        model = User
        depth = 1
        fields = "__all__"
            # ('pk', 'nom', 'etiqueta', 'foto', 'productor', 'thumb', 'text_curt', 'formats')
