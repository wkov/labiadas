
from romani.models import UserProfile
from django.shortcuts import render

def UserDetailView(request, pk):

    user = User.objects.get(username=username)
    userp = UserProfile.objects.get(user=user)	
    return render(request, "romani/consumidors/perfil.html", {'userp': userp})
