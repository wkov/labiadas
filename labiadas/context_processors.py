
from romani.models import UserProfile, Productor

# Utilitzat permanentment en el user_menu.html per a mostrar les notificacions en detall quan l'usuari clica l'icona
def notifications_user(request):
    if not request.user.is_authenticated():
        return ''
    if request.user.is_anonymous():
        return ''
    ret = request.user.notifications.filter(unread=True)
    return { 'notifications_user' : ret}

# Utilitzat permanentment en la capçalera de la web per a decidir el títol que veu l'usuari
def node_user(request):
    if not request.user.is_authenticated():
        return { 'node_user' : 'la massa'}
    if request.user.is_anonymous():
        return { 'node_user' : 'la massa'}

    up = UserProfile.objects.get(user=request.user)
    pro = Productor.objects.filter(responsable=request.user)

    if pro:
        return { 'node_user' : 'la massa'}
    else:
        return { 'node_user' : up.lloc_entrega.nom}

# Utilitzat permanentment en el user_menu.html per a visualitzar una miniatura de l'avatar de l'usuari
def foto_user(request):
    if not request.user.is_authenticated():
        return { 'foto_user' : ''}
    if request.user.is_anonymous():
        return { 'foto_user' : ''}
    up = UserProfile.objects.get(user=request.user)
    try:
        return { 'foto_user' : up.avatar.url}
    except:
        return { 'foto_user' : ''}