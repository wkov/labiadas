from django.contrib import admin
from romani.models import Producte, Productor, TipusProducte, Comanda, Node, UserProfile, Adjunt, Etiqueta, DiaEntrega, FranjaHoraria, Key, Frequencia, DiaProduccio, Stock, DiaFormatStock, Vote, Entrega

class producteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'productor', 'descripcio', 'text_curt', 'karma_date', 'karma_value')
    search_fields = ['nom']
    list_filter = ['nom', 'productor']

class voteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'entrega')
    search_fields = ['voter', 'entrega']
    list_filter = ['voter', 'entrega']

class productorAdmin(admin.ModelAdmin):
    list_display = ('nom','text')
    search_fields = ['nom', 'text']
    list_filter = ['nom', 'responsable']

class tipusproducteAdmin(admin.ModelAdmin):
    # list_display = ('nom', 'producte_nom','preu','pk','stock')
    search_fields = ['nom','preu', 'productor']
    list_filter = ['nom','preu', 'productor']

class comandaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'data_comanda','format','cantitat','externa','client', 'frequencia')
    search_fields = ['format__producte', 'data_comanda','format','externa','client', 'frequencia']
    list_filter = ['format__producte','data_comanda','format','externa','client','frequencia']


class entregaAdmin(admin.ModelAdmin):
    list_display = ('dia_entrega','comanda','data_comanda', 'dia_produccio', 'franja_horaria')
    search_fields = ['comanda__format__producte', 'data_comanda','comanda__format','comanda__client']
    list_filter = ['comanda__format','data_comanda','comanda__externa','comanda__client',]

class userprofileAdmin(admin.ModelAdmin):
    list_display = ('user','bio','lloc_entrega')
    search_fields = ['user','bio','lloc_entrega']
    list_filter = ['user','bio','lloc_entrega']

class adjuntAdmin(admin.ModelAdmin):
    list_display = ('arxiu', 'productor')
    search_fields = ['arxiu', 'productor']
    list_filter = ['arxiu', 'productor']

class etiquetaAdmin(admin.ModelAdmin):
    search_fields = ['nom', 'img']
    list_filter = ['nom', 'img']

class diaFormatStockAdmin(admin.ModelAdmin):
    list_display = ('dia', 'tipus_stock', 'format')
    search_fields = ['dia', 'tipus_stock', 'format']
    list_filter = ['dia', 'tipus_stock', 'format']

class diaentregaAdmin(admin.ModelAdmin):
    # list_display = ('franjes_horaries', 'date', 'node')
    search_fields = ['franjes_horaries', 'date', 'node']
    list_filter =  ['franjes_horaries', 'date' , 'node']

class franjahorariaAdmin(admin.ModelAdmin):
    # list_display = ['inici','final']
    search_fields = ['inici','final']
    list_filter = ['inici','final']

class nodeAdmin(admin.ModelAdmin):
    list_display = ('nom','carrer','poblacio','codi_postal', 'a_domicili')
    search_fields = ['nom','carrer','poblacio','codi_postal','responsable','a_domicili']
    list_filter = ['nom','carrer','poblacio','codi_postal','responsable','a_domicili']

class keyAdmin(admin.ModelAdmin):
    list_display = ('key','usuari','nou_usuari', 'data')
    search_fields = ['key','usuari','nou_usuari', 'data']
    list_filter = ['key','usuari','nou_usuari', 'data']

class frequenciaAdmin(admin.ModelAdmin):
    list_display = ['nom','num']
    search_fields = ['nom','num']
    list_filter = ['nom','num']

class diaProduccioAdmin(admin.ModelAdmin):
    list_display = ['date','productor', 'node']
    search_fields = ['date','productor', 'node']
    list_filter = ['date','productor', 'node']

class stockAdmin(admin.ModelAdmin):
    list_display = ['dia_prod','format']
    search_fields = ['dia_prod','format']
    list_filter = ['dia_prod','format']

admin.site.register(DiaFormatStock, diaFormatStockAdmin)
admin.site.register(Stock, stockAdmin)
admin.site.register(DiaProduccio, diaProduccioAdmin)
admin.site.register(Producte, producteAdmin)
admin.site.register(Productor, productorAdmin)
admin.site.register(TipusProducte, tipusproducteAdmin)
admin.site.register(Comanda, comandaAdmin)
admin.site.register(Node, nodeAdmin)
admin.site.register(UserProfile, userprofileAdmin)
admin.site.register(Adjunt, adjuntAdmin)
admin.site.register(Etiqueta, etiquetaAdmin)
admin.site.register(DiaEntrega,  diaentregaAdmin)
admin.site.register(FranjaHoraria, franjahorariaAdmin)
admin.site.register(Entrega, entregaAdmin)
admin.site.register(Key, keyAdmin)
admin.site.register(Frequencia, frequenciaAdmin)
admin.site.register(Vote, voteAdmin)