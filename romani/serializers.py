from rest_framework import serializers
from romani.models import Producte, Etiqueta, TipusProducte, UserProfile, Comanda, Productor, Node, DiaEntrega, FranjaHoraria
from django.contrib.auth.models import User


class ProducteSerializer(serializers.ModelSerializer):
    punts_karma = serializers.SerializerMethodField('puntuacio')
    formats_dis = serializers.SerializerMethodField('formats_disponibles')
    # dies_stocks = serializers.SerializerMethodField('d_s_futurs')
    #
    def puntuacio(self, obj):
        userp_pk = self.context.get("userp_pk")
        up =UserProfile.objects.get(pk=userp_pk)
        karma = obj.karma(up.lloc_entrega)
        return karma

    def formats_disponibles(self, obj):
        formats_disponibles = self.context.get("formats_dis")
        lst = []
        for f in formats_disponibles:
            if f.producte == obj:
                lst.append(f.pk)
        formats = TipusProducte.objects.filter(pk__in=lst)
        formats_dis_serialized = FormatSerializer(formats, many=True)
        return formats_dis_serialized.data


    # def d_s_futurs(self, obj):
    #     return obj.dies_stocks_futurs()

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Producte
        depth = 1
        fields = ('nom', 'etiqueta', 'text_curt', 'descripcio', 'datahora', 'foto', 'thumb', 'productor', 'keywords',
                  'frequencies', 'estrelles', 'punts_karma', 'formats_dis')

class ProductorSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Productor
        depth = 1
        fields = ('nom', 'responsable', 'text', 'hores_limit', 'adjunts')


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
        depth = 1
        fields = ('pk', 'nom', 'preu', 'productor', 'producte', 'dies_stocks_futurs')


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


class DiaEntregaSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiaEntrega
        depth = 1
        fields = "__all__"


class FranjaHorariaSerializer(serializers.ModelSerializer):

    class Meta:
        model = FranjaHoraria
        depth = 0
        fields = ('inici', 'final')


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

