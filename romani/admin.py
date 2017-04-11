from django.contrib import admin
from .models import Producte, Productor, TipusProducte, Comanda, Contracte, Node, UserProfile, Adjunt, Etiqueta, DiaEntrega, FranjaHoraria, Key, Frequencia

class producteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'productor', 'descripcio', 'entradilla', 'karma_date', 'karma_value')
    search_fields = ['nom']
    list_filter = ['nom', 'productor']


class productorAdmin(admin.ModelAdmin):
    list_display = ('nom','cuerpo')
    search_fields = ['nom']
    list_filter = ['nom']

class tipusproducteAdmin(admin.ModelAdmin):
    # list_display = ('nom', 'producte_nom','preu','pk','stock')
    search_fields = ['nom','preu', 'producte']
    list_filter = ['nom','preu', 'producte']

class comandaAdmin(admin.ModelAdmin):
    list_display = ('producte','data_comanda','format','cancelat','client','data_entrega','lloc_entrega','entregat')
    search_fields = ['producte','data_comanda','format','cancelat','client','data_entrega','lloc_entrega','entregat']
    list_filter = ['producte','data_comanda','format','cancelat','client','data_entrega','lloc_entrega','entregat']

class contracteAdmin(admin.ModelAdmin):
    list_display = ('producte','data_comanda','format', 'client','data_entrega','lloc_entrega' )
    search_fields = ['producte','data_comanda','format', 'client','data_entrega','lloc_entrega' ]
    list_filter = ['producte','data_comanda','format', 'client','data_entrega','lloc_entrega' ]

class userprofileAdmin(admin.ModelAdmin):
    list_display = ('user','bio','lloc_entrega_perfil')
    search_fields = ['user','bio','lloc_entrega_perfil']
    list_filter = ['user','bio','lloc_entrega_perfil']

class adjuntAdmin(admin.ModelAdmin):
    search_fields = ['arxiu']
    list_filter = ['arxiu']

class etiquetaAdmin(admin.ModelAdmin):
    search_fields = ['nom', 'img']
    list_filter = ['nom', 'img']


class diaentregaAdmin(admin.ModelAdmin):
    # list_display = ('franjes_horaries', 'date', 'node')
    search_fields = ['franjes_horaries', 'date', 'node']
    list_filter =  ['franjes_horaries', 'date' , 'node']

class franjahorariaAdmin(admin.ModelAdmin):
    # list_display = ['inici','final']
    search_fields = ['inici','final']
    list_filter = ['inici','final']

class nodeAdmin(admin.ModelAdmin):
    list_display = ('nom','carrer','poblacio','codi_postal','responsable', 'a_domicili')
    search_fields = ['nom','carrer','poblacio','codi_postal','responsable','dies_entrega','a_domicili']
    list_filter = ['nom','carrer','poblacio','codi_postal','responsable','dies_entrega', 'a_domicili']

class keyAdmin(admin.ModelAdmin):
    list_display = ('key','usuari','nou_usuari', 'data')
    search_fields = ['key','usuari','nou_usuari', 'data']
    list_filter = ['key','usuari','nou_usuari', 'data']

class frequenciaAdmin(admin.ModelAdmin):
    list_display = ['nom','num']
    search_fields = ['nom','num']
    list_filter = ['nom','num']




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
admin.site.register(Contracte, contracteAdmin)
admin.site.register(Key, keyAdmin)
admin.site.register(Frequencia, frequenciaAdmin)