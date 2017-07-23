
from romani.models import UserProfile, Productor

def notifications_user(request):
    if not request.user.is_authenticated():
        return ''

    if request.user.is_anonymous():
        return ''

    ret = request.user.notifications.filter(unread=True)

    return { 'notifications_user' : ret}


def node_user(request):
    if not request.user.is_authenticated():
        return { 'node_user' : 'la massa'}

    if request.user.is_anonymous():
        return { 'node_user' : 'la massa'}

    up = UserProfile.objects.get(user=request.user)

    try:
        pro = Productor.objects.filter(responsable=request.user)
        return { 'node_user' : 'la massa'}
    except:
        return { 'node_user' : up.lloc_entrega_perfil.nom}


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