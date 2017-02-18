
from romani.models import UserProfile

def notifications_user(request):
    if not request.user.is_authenticated():
        return ''

    if request.user.is_anonymous():
        return ''

    ret = request.user.notifications.filter(unread=True)

    return { 'notifications_user' : ret}

