from django.shortcuts import render, redirect
# permite crear formularios po defecto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Para registrar los usuarios
from django.contrib.auth import login # para crear una cokkie
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Se usa la clase User y de todos sus metodos se utiliza el metodo create_user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            # Registrar usuarios
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error':'Usuario Existente'
                })

        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })

def task(request):
    return render(request, 'task.html')