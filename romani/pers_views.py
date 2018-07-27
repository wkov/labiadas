
from romani.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.models import  User

def UserDetailView(request, pk):

    user = User.objects.get(pk=pk)
    userp = UserProfile.objects.get(user=user)	
    return render(request, "romani/consumidors/perfil.html", {'userp': userp})
