from django.shortcuts import render, redirect, get_object_or_404
# permite crear formularios po defecto
# Para crear un usuario, Para autenticar un usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Para registrar los usuarios
# para crear una sesion(cookie), para cerrar una sesion, para comprobar que exista el usuario en la bd
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import createTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required #decorador permite proteger una funion


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
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
                    'error': 'Usuario Existente'
                })
        else:
            return render(request, 'signup.html', {
                'error': 'Las contraseñas no coinciden'
            })

@login_required
def task(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'task.html', {
        'task': task
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': createTaskForm
        })
    else:
        try:
            task = createTaskForm(request.POST)
            new_task = task.save(commit=False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            return redirect('task')

        except ValueError:
            return render(request, 'create_task.html', {
                'form': createTaskForm,
                'error': 'Por favo provea de datos validos'
            })

@login_required
def complete(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'task_complete.html', {
        'task': task
    })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        '''del modelo de tareas se utiliza <objets> para obtener un dato donde la clave primaria es igual al parametro <task_id>'''
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        return render(request, 'task_detail.html', {
            'task': task,
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = createTaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error':'ERROR DE ACTUALIZACIÓN'})

@login_required
def complete_task(request, task_id):
    task=get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method =='POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')

@login_required
def delete_task(request, task_id):
    task=get_object_or_404(Task,pk=task_id, user=request.user)
    if request.method =='POST':
        task.delete()
        return redirect('task')


def salir(request):
    # Se usa el método logout() que recibe un reques como parámetro
    logout(request)
    # S e retorna a la página principal
    return redirect('home')

def signin(request):
    # Si se usa el método GET se envia los datos de la interfaz signin
    if request.method == 'GET':
        return render(request, 'signin.html', {
        })
    # Si se usa el método POST se recuperan los datos
    else:
        # método que permite iniciar sesión recibe tres parámetros(request, username and password)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        # Si el usuario no existe
        if user is None:
            return render(request, 'signin.html', {
                'error': 'usuario y contaseña incorrectos'
            })
        # Si existe el usaurio en la bd, se carga la sesion del usuario y se redirecciona a la palntilla task
        else:
            login(request, user)
            return redirect('task')


