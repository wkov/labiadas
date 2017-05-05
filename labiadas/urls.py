from django.conf.urls import include, url
from django.contrib import admin
from romani import views
from django.conf.urls.static import static

from django.conf import settings

from romani.models import EmailModelBackend

from django.contrib.auth.decorators import login_required as auth

from romani.views import nouUsuariView, DomiciliView, NodeSaveView, nodesNouUsuariView, NodeDetailView, FreqCalcView, ComandesListView, ProductesListView, NodesListView, NodesDatesListView, diaNodeEvents
from romani.views import UserProfileEditView, etiquetaView, MyRegistrationView, CoordenadesView, AllCoordenadesView, buskadorProducte, HistorialListView, ProducteUpdateView, NodeUpdateView
from romani.views import ComandaFormView, InfoFormView, ConvidarView, NodeCalcView, FranjaCalcView, AjudaView, NodeHorariView, ProductorsListView, ProductorUpdateView, DatesListView, NodeProductorsUpdateView
from romani.views import DiaEntregaCreateView, NodeComandesListView, diaEntregaEvents, LlocsListView, ContracteUpdateView, diaEntregaSelected, DiaEntregaProductorView, FranjaHorariaCreateView, AdjuntCreateView

from django.contrib.auth.views import login, logout_then_login

from django.views.generic import RedirectView, TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name="admin"),

    url(r"^login/$", login,{"template_name": "login.html"}, name="login"),
    url(r"^logout/$", logout_then_login,name="logout"),

    url(r"^accounts/", include("registration.backends.simple.urls")),
    url(r'^register/(?P<pk>\d+)$', MyRegistrationView.as_view(), {'backend': 'registration.backends.default.DefaultBackend'}, name='registration_register'),
    url(r'^register/closed/$', TemplateView.as_view(template_name='registration/registration_closed.html'),name='registration_disallowed'),


    url(r'^vista_productors/', auth(ProductorsListView.as_view()), name="productor_list"),
    url(r'^pro/(?P<pro>\d+)/vista_comandes/', auth(ComandesListView.as_view()), name='vista_comandes'),
    url(r'^pro/(?P<pk>\d+)/data_comandes/(?P<dataentrega>\d+)$', auth(views.DiaEntregaProductorView), name='data_comandes'),
    url(r'^pro/(?P<pro>\d+)/calEvents/$', auth(diaEntregaEvents), name="calEvents"),
    url(r'^pro/(?P<pro>\d+)/cal2Events/$', auth(diaEntregaSelected), name="cal2Events"),
    url(r'^pro/(?P<pro>\d+)/vista_productes/', auth(ProductesListView.as_view()), name='vista_productes'),
    url(r'^pro/(?P<pro>\d+)/vista_llocs/', auth(LlocsListView.as_view()), name='vista_llocs'),
    url(r'^pro/(?P<pro>\d+)/vista_dates/', auth(DatesListView.as_view()), name='vista_dates'),
    url(r'^pro/(?P<pro>\d+)/vista_historial/', auth(HistorialListView.as_view()), name='vista_historial'),
    url(r"^productor/update/(?P<pk>\d+)/$", auth(ProductorUpdateView.as_view()), name="productor_update"),
    url(r"^producte/update/(?P<pk>\d+)/$", auth(ProducteUpdateView.as_view()), name="producte_update"),
    url(r"^pro/(?P<pro>\d+)/adjunt/create/$", auth(AdjuntCreateView.as_view()), name="adjunt_create"),


    url(r'^vista_nodes/', auth(NodesListView.as_view()), name='vista_nodes'),
    url(r'^dis/(?P<dis>\d+)/node_comandes/(?P<pk>\d+)$', auth(NodeComandesListView.as_view()), name='node_comandes'),
    url(r'^dis/(?P<dis>\d+)/vista_nodesdates/', auth(NodesDatesListView.as_view()), name='vista_nodesdates'),
    url(r'^dis/(?P<dis>\d+)/Events/$', auth(diaNodeEvents), name="calNodeEvents"),
    # url(r'^dis/(?P<dis>\d+)/vista_nodesproductors/', auth(NodesProductorsListView.as_view()), name='vista_nodesproductors'),
    # url(r'^dis/(?P<dis>\d+)/vista_nodeshistorial/', auth(NodesHistorialListView.as_view()), name='vista_nodeshistorial'),
    url(r"^node/update/(?P<pk>\d+)/$", auth(NodeUpdateView.as_view()),
        name="node_update"),
    url(r"^node_productors/update/(?P<pk>\d+)/$", auth(NodeProductorsUpdateView.as_view()),
        name="nodeproductors_update"),
    url(r"^dis/(?P<dis>\d+)/diaentrega/create/$", auth(DiaEntregaCreateView.as_view()),
        name="diaentrega_create"),
    url(r"^dis/(?P<dis>\d+)/franjahoraria/create/$", auth(FranjaHorariaCreateView.as_view()),
        name="franjahoraria_create"),



    url(r"^contracte/update/(?P<pk>\d+)/$", auth(ContracteUpdateView.as_view()),
        name="contracte_update"),
    # url(r"^producte_llocentrega/update/(?P<pk>\d+)/$", auth(LlocsUpdateView.as_view()),
    #     name="producte_llocentrega_update"),
    # url(r"^producte_dates/update/(?P<pk>\d+)/$", auth(ProducteDatesUpdateView.as_view()),
    #     name="productedates_update"),

    url(r'^nou_usuari/', auth(views.nouUsuariView), name="nou_usuari"),
    url(r'^nodes_nou_usuari/', auth(views.nodesNouUsuariView), name="nodes_nou_usuari"), #ajax: retorna nodes pel select de nou_usuari amb la opcio inicial marcada segons l'usuari que ha convidat
    url(r'^busk/$', auth(views.buskadorProducte) , name='busk'),
    url(r'^node_detail/(?P<pk>\d+)$', auth(views.NodeDetailView) , name='node_detail'),
    url(r'^productor/(?P<pk>\d+)$', auth(views.productorView), name='productor'),
    url(r'^(?P<pk>\d+)$', auth(views.producteView), name='producte'),
    # url(r'^coope/', auth(views.coopeView), name="coope"), #MAIN VIEW
    url(r'^comandes/', auth(views.comandesView), name="comandes"),
    url(r'^entregas/', auth(views.entregasView), name="entregas"),
    url(r'^comandaDelete/(?P<pk>\d+)$', auth(views.comandaDelete), name="comandaDelete"),
    url(r'^contracteDelete/(?P<pk>\d+)$', auth(views.contracteDelete), name="contracteDelete"),
    url(r'^etiqueta/(?P<pk>\d+)/$', auth(views.etiquetaView),name='etiqueta'),#llistat de productes relacionats amb la etiqueta
    url(r'^ajuda/', auth(views.AjudaView), name="ajuda"),
    url(r'^domicili/$', auth(DomiciliView), name="domicili"), #ajax: retorna els detalls de localització del node seleccionat en <select>
    url(r'^horari/$', auth(NodeHorariView), name="horari"), #ajax: retorna els detalls de horari del node seleccionat en <select>
    url(r'^allcoordenades/$', auth(AllCoordenadesView), name="allcoordenades"), #ajax: retorna coordenades de tots els nodes al mapa
    url(r'^coordenades/$', auth(CoordenadesView), name="coordenades"), #ajax: portar coordenades al mapa
    url(r'^nodesave/$', auth(NodeSaveView), name="nodesave"), #ajax; guardar elecció de nou usuari al entrar per 1a vegada
    url(r'^nodecalc/$', auth(NodeCalcView), name="nodecalc"), #ajax: en comanda calcula els posibles dies de la setmana segons el node seleccionat
    url(r'^freqcalc/$', auth(FreqCalcView), name="freqcalc"), #ajax: en comanda calcula els posibles dies de la setmana segons el node seleccionat
    url(r'^franjacalc/$', auth(FranjaCalcView), name="franjacalc"),#ajax: en comanda calcula les franjes horaries segons el lloc i el dia seleccionats
    # url(r'^datacalc/$', auth(DataCalcView), name="datacalc"),  #ajax: calcula el dia concret (dd/mm/yyyy) segons el dia de la setmana (dilluns, dimarts,)  seleccionat
    url(r'^info/$', auth(InfoFormView.as_view()), name="info"), #genera el modal en que es confirma una comanda
    url(r'^comanda/$', auth(ComandaFormView.as_view()), name="comanda"), #confirma la comanda
    url(r'^convidar/$', auth(ConvidarView), name="convidar"),
    url(r'^messages/', include('django_messages.urls')),
    url('^inbox/notifications/', include('notifications.urls', namespace="notifications")),
    url(r"edit_profile/$", auth(UserProfileEditView.as_view()), name="edit_profile"),
    url(r'^$', auth(views.coopeView), name="coope"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
