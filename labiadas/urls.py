from django.conf.urls import include, url
from django.contrib import admin
from romani import views
from django.conf.urls.static import static

from django.conf import settings

from romani.models import EmailModelBackend

from django.contrib.auth.decorators import login_required as auth

from romani.public_views import buskadorProducte, etiquetaView, ComandaFormView, producteView, productorView, diesEntregaView
from romani.public_views import coopeView, etiquetaView, comandesView, entregasView, comandaDelete, VoteFormView, cistellaView
from romani.public_views import historialView, entregaDelete
from romani.node_views import NodesListView, NodesDatesListView, diaNodeEvents, NodeUpdateView, NodeProductorsUpdateView, FranjaHorariaCreateView, DiaEntregaCreateView
from romani.node_views import DiaEntregaUpdateView, NodeComandesListView, export_comandes_xls, NodeCreateView
from romani.node_views import diaNodeDisEvents, nodeProductorView
from romani.productor_views import ComandesListView, ProductesListView, HistorialListView, ProducteUpdateView, AdjuntCreateView, TipusProducteCreateView, TipusProducteUpdateView, ProducteCreateView
from romani.productor_views import ProductorUpdateView, DatesListView, diaEntregaEvents, diaEntregaSelected, DiaEntregaProductorView, ProductorCreateView, diaProdEvents
from romani.productor_views import distriCalendarEvents, distriCalendarSelected, ProductorsCalListView, ProductorsHistListView, DiaEntregaDistribuidorView, DiaProduccioCreateView, historialProView
from romani.productor_views import DiaProduccioUpdateView, ComandaCreateView, dis_export_comandes_xls, pro_export_comandes_xls, adjuntDelete, adjuntsProductor, CoopsListView
from romani.productor_views import producteDelete, productorGraphView, graphProductorView, DiaProduccioPaCreateView, DiaProduccioPaUpdateView, comandesProView, comandesDisView, historialDisView
from romani.productor_views import NodeProDetailView, diesEntregaProView, formatDelete
from romani.views import nouUsuariView, DomiciliView, NodeSaveView, nodesNouUsuariView, NodeDetailView, FreqCalcView
from romani.views import UserProfileEditView, MyRegistrationView, CoordenadesView, AllCoordenadesView, ResetPasswordRequestView, PasswordResetConfirmView
from romani.views import InfoFormView, ConvidarView, NodeCalcView, FranjaCalcView, AjudaView, NodeHorariView
from romani.views import numcomandesView, numproductorView, usercornerView
from romani.pers_views import UserDetailView
from romani import api
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
# from romani.api_views import CustomObtainAuthToken

from django.contrib.auth.views import LoginView, LogoutView

from django.views.generic import RedirectView, TemplateView

from rest_framework.schemas import get_schema_view

from machina import urls as machina_urls

admin.autodiscover()

urlpatterns = [

    url(r"^login/$", LoginView.as_view(), {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    # url(r"^accounts/", include("django_registration.backends.simple.urls")),
    url(r'^register/(?P<pk>\d+)$', MyRegistrationView.as_view(), {'backend': 'django_registration.backends.default.DefaultBackend'}, name='django_registration_register'),
    url(r'^register/closed/$', TemplateView.as_view(template_name='django_registration/registration_closed.html'),name='django_registration_disallowed'),
    url(r'^account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    url(r'^account/reset_password', ResetPasswordRequestView.as_view(), name="reset_password"),

    # url(r'^forum/', include('forum.urls')),

    url(r'^admin/', admin.site.urls, name="admin"),


    url(r'^dis/export/xls/(?P<pk>\d+)/$', auth(dis_export_comandes_xls), name='dis_export_comandes_xls'),
    url(r'^vista_productors/', auth(comandesDisView), name="productor_list"),
    url(r'^distri_cal/', auth(ProductorsCalListView.as_view()), name="productor_cal_list"),
    url(r'^distri_hist/', auth(historialDisView), name="productor_hist_list"),
    url(r'^pro/distri_dia/(?P<dataentrega>\d+)$', auth(DiaEntregaDistribuidorView), name='distri_data_comandes'),
    url(r'^pro/distriEvents/$', auth(distriCalendarEvents), name="distriEvents"),
    url(r'^pro/distriSelected/$', auth(distriCalendarSelected), name="distriSelected"),
    url(r'^pro/coops/', auth(CoopsListView.as_view()), name='productorCoops'),
    url(r"^productor/create/$", auth(ProductorCreateView.as_view()), name="productor_create"),

    url(r'^pro/(?P<pro>\d+)/export/xls/(?P<pk>\d+)/$', auth(pro_export_comandes_xls), name='pro_export_comandes_xls'),
    url(r'^pro/(?P<pro>\d+)/vista_comandes/', auth(comandesProView), name='vista_comandes'),
    url(r'^pro/(?P<pk>\d+)/data_comandes/(?P<dataentrega>\d+)$', auth(DiaEntregaProductorView), name='data_comandes'),
    url(r'^pro/(?P<pro>\d+)/calEvents/$', auth(diaEntregaEvents), name="calEvents"),
    url(r'^pro/(?P<pro>\d+)/cal2Events/$', auth(diaEntregaSelected), name="cal2Events"),
    url(r'^pro/(?P<pro>\d+)/calProdEvents/$', auth(diaProdEvents), name="calProdEvents"),
    url(r'^pro/(?P<pro>\d+)/vista_productes/', auth(ProductesListView.as_view()), name='vista_productes'),
    url(r'^pro/(?P<pro>\d+)/vista_dates/', auth(DatesListView.as_view()), name='vista_dates'),
    url(r'^pro/(?P<pro>\d+)/vista_historial/', auth(historialProView), name='vista_historial'),
    url(r"^productor/update/(?P<pk>\d+)/$", auth(ProductorUpdateView.as_view()), name="productor_update"),
    url(r"^producte/update/(?P<pk>\d+)/$", auth(ProducteUpdateView.as_view()), name="producte_update"),
    url(r"^format/update/(?P<pk>\d+)/$", auth(TipusProducteUpdateView.as_view()), name="format_update"),
    url(r"^pro/(?P<pro>\d+)/adjunt/create/$", auth(AdjuntCreateView.as_view()), name="adjunt_create"),
    url(r"^pro/(?P<pro>\d+)/adjunts/$", auth(adjuntsProductor), name="adjuntsProductor"),
    url(r'^adjuntDelete/(?P<pk>\d+)$', auth(adjuntDelete), name="adjuntDelete"),
    url(r"^pro/(?P<pro>\d+)/format/create/$", auth(TipusProducteCreateView.as_view()), name="format_create"),
    url(r"^pro/(?P<pro>\d+)/producte/create/$", auth(ProducteCreateView.as_view()), name="producte_create"),
    url(r"^pro/(?P<pro>\d+)/diaproduccio/$", auth(DiaProduccioCreateView), name="diaproduccio_create"),
    url(r"^pro/(?P<pro>\d+)/diaproduccio_update/(?P<pk>\d+)$", auth(DiaProduccioUpdateView), name="diaproduccio_update"),
    url(r"^pro/(?P<pro>\d+)/diaproducciopa/$", auth(DiaProduccioPaCreateView), name="diaproducciopa_create"),
    url(r"^pro/(?P<pro>\d+)/diaproducciopa_update/(?P<pk>\d+)$", auth(DiaProduccioPaUpdateView), name="diaproducciopa_update"),
    url(r"^pro/(?P<pro>\d+)/comanda/create/$", auth(ComandaCreateView.as_view()), name="comanda_create"),
    url(r'^producteDelete/(?P<pk>\d+)$', auth(producteDelete), name="producteDelete"),
    url(r'^formatDelete/(?P<pk>\d+)$', auth(formatDelete), name="formatDelete"),
    url(r'^pro/(?P<pro>\d+)/graph.png', auth(productorGraphView), name="graph"),
    url(r'^pro/(?P<pro>\d+)/stats', auth(graphProductorView), name="stats"),
    url(r'^pro/node_detail/(?P<pk>\d+)$', auth(NodeProDetailView), name='node_pro_detail'),
    url(r'^pro/dies_entrega/(?P<pk>\d+)$', auth(diesEntregaProView), name="diesEntregaPro"),



    url(r'^export/xls/(?P<pk>\d+)/$', auth(export_comandes_xls), name='export_comandes_xls'),
    url(r'^vista_nodes/', auth(NodesListView.as_view()), name='vista_nodes'),
    url(r'^dis/(?P<dis>\d+)/node_comandes/(?P<pk>\d+)$', auth(NodeComandesListView.as_view()), name='node_comandes'),
    url(r'^dis/(?P<dis>\d+)/vista_nodesdates/', auth(NodesDatesListView.as_view()), name='vista_nodesdates'),
    url(r'^dis/(?P<dis>\d+)/Events/$', auth(diaNodeEvents), name="calNodeEvents"),
    url(r'^disNode/Events/$', auth(diaNodeDisEvents), name="calDisNodeEvents"),
    url(r"^node/update/(?P<pk>\d+)/$", auth(NodeUpdateView.as_view()),
        name="node_update"),
    url(r"^node_productors/update/(?P<pk>\d+)/$", auth(NodeProductorsUpdateView.as_view()),
        name="nodeproductors_update"),
    url(r"^diaentrega/update/(?P<pk>\d+)/$", auth(DiaEntregaUpdateView.as_view()),
        name="diaentrega_update"),
    url(r"^dis/(?P<dis>\d+)/diaentrega/create/$", auth(DiaEntregaCreateView.as_view()),
        name="diaentrega_create"),
    url(r"^dis/(?P<dis>\d+)/franjahoraria/create/$", auth(FranjaHorariaCreateView.as_view()),
        name="franjahoraria_create"),
    url(r"^node/create/$", auth(NodeCreateView.as_view()), name="node_create"),
    url(r"^node/productor/(?P<pk>\d+)/$", auth(nodeProductorView), name="node_productor"),


    # url(r"^contracte/update/(?P<pk>\d+)/$", auth(ContracteUpdateView.as_view()),
    #     name="contracte_update"),
    # url(r"^contracte/(?P<pk>\d+)/$", auth(ContracteDetailView.as_view()),
    #     name="contracte_detail"),


    url(r'api/list', auth(api.get_product_list), name='get_product_list'),
    url(r'api/example', auth(api.example_view), name='example_view'),
    # url(r'api/user', api.get_user, name='get_user'),
    url(r'^api/$', auth(get_schema_view())),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'api/auth/list', auth(api.get_product_list), name='get_product_list'),
    url(r'api/auth/example', api.example_view, name='example_view'),
    # url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    # url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
    # url(r'^api/echo/$', api.EchoView.as_view()),
    # url(r'^authenticate/', CustomObtainAuthToken.as_view()),
    url(r'^api/auth/token/obtain/$', obtain_jwt_token),
    url(r'^api/auth/token/refresh/$', refresh_jwt_token),



    url(r'^vote/$', auth(VoteFormView.as_view()), name="vote"),



    url(r'^messages/', include('django_messages.urls')),

    url(r'^forum/', include(machina_urls)),



    url(r'^nou_usuari/', auth(views.nouUsuariView), name="nou_usuari"),
    url(r'^nodes_nou_usuari/', auth(views.nodesNouUsuariView), name="nodes_nou_usuari"), #ajax: retorna nodes pel select de nou_usuari amb la opcio inicial marcada segons l'usuari que ha convidat
    url(r'^busk/$', auth(buskadorProducte) , name='busk'),
    url(r'^node_detail/(?P<pk>\d+)$', auth(views.NodeDetailView) , name='node_detail'),
    url(r'^productor/(?P<pk>\d+)$', auth(productorView), name='productor'),
    url(r'^(?P<pk>\d+)$', auth(producteView), name='producte'),
    # url(r'^coope/', auth(views.coopeView), name="coope"), #MAIN VIEW
    url(r'^comandes', auth(cistellaView), name="comandes"),
    url(r'^entregas/', auth(historialView), name="entregas"),
    url(r'^comandaDelete/(?P<pk>\d+)$', auth(entregaDelete), name="entregaDelete"),
    # url(r'^contracteDelete/(?P<pk>\d+)$', auth(contracteDelete), name="contracteDelete"),
    url(r'^etiqueta/(?P<pk>\d+)/$', auth(etiquetaView),name='etiqueta'),#llistat de productes relacionats amb la etiqueta
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
    url(r'^numcomandes/$', auth(numcomandesView), name="numcomandes"),
    url(r'^numcomandespro/$', auth(numproductorView), name="numcomandespro"),
    url(r'^usercorner/$', auth(usercornerView), name="usercorner"),
    url(r'^info/$', auth(InfoFormView.as_view()), name="info"), #genera el modal en que es confirma una comanda
    url(r'^comanda/$', auth(ComandaFormView.as_view()), name="comanda"), #confirma la comanda
    url(r'^dies_entrega/(?P<pk>\d+)/(?P<pro>\d+)$', auth(diesEntregaView), name="diesEntrega"),
    url(r'^convidar/$', auth(ConvidarView), name="convidar"),
    # url('^inbox/notifications/', include('notifications.urls', namespace="notifications")),
    url(r"edit_profile/$", auth(UserProfileEditView.as_view()), name="edit_profile"),
    url(r'^perfil/(?P<pk>\d+)$', auth(UserDetailView), name='perfil'),
    url(r'^$', auth(coopeView), name="coope"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
