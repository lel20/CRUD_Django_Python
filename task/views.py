from django.shortcuts import render, redirect
# permite crear formularios po defecto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Para crear un usuario, Para autenticar un usuario
from django.contrib.auth.models import User  # Para registrar los usuarios
from django.contrib.auth import login,logout,authenticate # para crear una sesion(cookie), para cerrar una sesion, para comprobar que exista el usuario en la bd
from django.http import HttpResponse
from .forms import createTaskForm
from .models import Task


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
                # login(request, user)
                return redirect('signin')
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
    task=Task.objects.filter(user= request.user)
    return render(request, 'task.html',{
        'task': task
    })

def salir(request):
    #Se usa el método logout() que recibe un reques como parámetro
    logout(request)
    #S e retorna a la página principal
    return redirect('home')
def signin(request):
    # Si se usa el método GET se envia los datos de la interfaz signin
    if request.method=='GET':
         return render(request, 'signin.html',{
        'form':AuthenticationForm
        })
    # Si se usa el método POST se recuperan los datos
    else:
        #método que permite iniciar sesión recibe tres parámetros(request, username and password)
        user=authenticate(request,username=request.POST['username'], password=request.POST['password'])
        #Si el usuario no existe 
        if user is None:
            return render(request, 'signin.html',{
                'form':AuthenticationForm,
                'error':'usuario y contaseña incorrectos'
            })
        #Si existe el usaurio en la bd, se carga la sesion del usuario y se redirecciona a la palntilla task
        else:
            login(request, user)
            return redirect('task')
def create_task(request):
    if request.method == 'GET':
        return render (request, 'create_task.html',{
            'form':createTaskForm
        }) 
    else: 
        try:
            task= createTaskForm(request.POST)
            new_task=task.save(commit=False) 
            new_task.user=request.user 
            print(new_task)
            new_task.save()
            return redirect('task')

        except ValueError:
            return render (request, 'create_task.html',{
            'form':createTaskForm,
            'error':'Por favo provea de datos validos'
        }) 
        
