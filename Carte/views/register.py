from django.contrib.auth import login
from django.shortcuts import render, redirect
from Carte.forms import CustomUserCreationForm

def register_view(request):
 if request.method == 'POST':
     form = CustomUserCreationForm(request.POST)
     if form.is_valid():
         user = form.save()
         login(request, user)
         return redirect('home')
 else:
     form = CustomUserCreationForm()
 return render(request, 'registration/register.html', {'form': form})