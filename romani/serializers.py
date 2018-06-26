from rest_framework import serializers
from romani.models import Producte, Etiqueta, TipusProducte, UserProfile, Comanda, Productor, Node, DiaEntrega, FranjaHoraria, Entrega
from django.contrib.auth.models import User


class ProducteSerializer(serializers.ModelSerializer):
    punts_karma = serializers.SerializerMethodField('puntuacio')
    formats_dis = serializers.SerializerMethodField('formats_disponibles')
    productora = serializers.SerializerMethodField('productor')
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

    def productor(self, obj):
        productor_serialized = ProductorSerializer(obj.productor, many=False)
        return productor_serialized.data
    # def d_s_futurs(self, obj):
    #     return obj.dies_stocks_futurs()

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Producte
        depth = 1
        fields = ('pk','nom', 'etiqueta', 'text_curt', 'descripcio', 'datahora', 'foto', 'thumb', 'productora', 'keywords',
                  'frequencies', 'estrelles', 'punts_karma', 'formats_dis')

class ProductorSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = Productor
        depth = 1
        fields = ('pk', 'nom', 'responsable', 'text', 'hores_limit', 'adjunts')


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
        fields = ('pk', 'nom', 'preu', 'dies_stocks_futurs')


class UserProfileSerializer(serializers.ModelSerializer):

    def userp_pk(self):
        return self.context.get("userp_pk")

    def formats(self):
        return self.context.get("formats_dis")

    preferits = ProducteSerializer(many=True, context={'userp_pk': userp_pk, 'formats_dis': formats})


    # preferits = ProducteSerializer(many=True)
    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)
    class Meta:
        model = UserProfile
        depth = 2
        fields = ('user', 'bio', 'invitacions', 'phone_number', 'avatar', 'carrer',
                  'numero', 'pis', 'direccio', 'poblacio', 'preferits', 'lloc_entrega')


class ComandaSerializer(serializers.ModelSerializer):

    producte = serializers.SerializerMethodField('product')


    def product(self, obj):
        return obj.format.producte.nom

    class Meta:
        model = Comanda
        depth = 2
        fields = ('pk', 'entregas', 'format', 'producte', 'cantitat', 'data_comanda', 'client', 'node', 'preu', 'frequencia')


class EntregaSerializer(serializers.ModelSerializer):

    # producte = serializers.SerializerMethodField('product')

    class Meta:
        model = Entrega
        depth = 1
        fields = ('pk', 'dia_entrega', 'comanda', 'data_comanda', 'dia_produccio', 'franja_horaria')


class DiaEntregaSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiaEntrega
        depth = 1
        fields = "__all__"


# class FranjaHorariaSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = FranjaHoraria
#         depth = 0
#         fields = ('inici', 'final')


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
                  'a_domicili','text','proxims_dies')

