from rest_framework import serializers
from romani.models import Producte, Etiqueta, Entrega, TipusProducte, UserProfile, Comanda, Productor, Node, DiaEntrega
from django.contrib.auth.models import User


class ProducteSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Producte
        depth = 0
        fields = "__all__"

class ProductorSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Productor
        depth = 0
        fields = "__all__"


class EtiquetaSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Etiqueta
        depth = 0
        fields = ('pk', 'nom', 'img')

class FormatSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = TipusProducte
        depth = 0
        fields = ('pk', 'nom', 'preu', 'productor', 'producte')


class UserProfileSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = UserProfile
        depth = 1
        fields = "__all__"
            # ('pk', 'nom', 'etiqueta', 'foto', 'productor', 'thumb', 'text_curt', 'formats')

class ComandaSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Comanda
        depth = 1
        fields = "__all__"

class EntregaSerializer(serializers.ModelSerializer):

    producte = serializers.SerializerMethodField('product')

    foto = serializers.SerializerMethodField('photo')

    def product(self, obj):
        return obj.comanda.format.producte.nom

    def photo(self, obj):
        return obj.comanda.format.producte.thumb.url

    class Meta:
        model = Entrega
        depth = 1
        fields = ('pk', 'dia_entrega', 'producte', 'comanda', 'data_comanda', 'dia_produccio', 'franja_horaria', 'foto')

class DiaEntregaSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiaEntrega
        depth = 1
        fields = "__all__"


class NodeSerializer(serializers.ModelSerializer):

    proxims_dies = serializers.SerializerMethodField('proxi_dies')


    def proxi_dies(self, obj):
        dies_serialized = DiaEntregaSerializer(obj.prox_dias(), many=True)
        return dies_serialized.data
    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Node
        depth = 1
        fields = ('pk','nom','position','carrer','numero','pis','poblacio','codi_postal','frequencia','responsable',
                  'a_domicili','text','productors','dies_entrega', 'proxims_dies')

