
from romani.models import UserProfile
from django.shortcuts import render

def UserDetailView(request, pk):

    userp = UserProfile.objects.get(pk=pk)

    return render(request, "romani/consumidors/perfil.html", {'userp': userp})