from rest_framework import serializers
from romani.models import Producte, TipusProducte


class ProducteSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)


    class Meta:
        model = Producte
        depth = 1
        fields = ('pk', 'nom', 'etiqueta', 'foto', 'productor', 'thumb', 'text_curt', 'formats')

