from rest_framework import serializers
from romani.models import Producte, TipusProducte


class ProducteSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)


    class Meta:
        model = Producte
        depth = 1
        fields = ('pk', 'nom', 'etiqueta', 'foto', 'productor', 'thumb', 'text_curt', 'formats')


class FormatSerializer(serializers.ModelSerializer):

    # formats_nom = serializers.RelatedField(source='formats', read_only=True)
    # formats = serializers.StringRelatedField(many=True)


    class Meta:
        model = TipusProducte
        depth = 1
        fields = ('pk')

 #
 # nom = models.CharField(max_length=20)
 #    etiqueta = models.ForeignKey(Etiqueta)
 #    text_curt = models.TextField(blank=False, max_length=75)
 #    descripcio = models.TextField(blank=True, default="")
 #    datahora = models.DateTimeField(auto_now_add=True)
 #    foto = models.FileField(upload_to='productes/%Y/%m/%d', null=True, validators=[validate_file])
 #    thumb = models.FileField(blank=True, null=True)
 #    productor = models.ForeignKey(Productor)
 #    keywords = models.TextField(blank=True, verbose_name='Paraules Clau')
 #    frequencies = models.ForeignKey(Frequencia)