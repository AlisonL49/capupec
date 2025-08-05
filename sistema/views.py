from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from usuarios.models import PerfilUsuario

def principal(request):
    return render(request, 'principal.html')

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verificar que tenga perfil de usuario
        try:
            if not hasattr(request.user, 'perfilusuario'):
                return redirect('acceso-denegado')
            
            # Verificar que tenga rol de administrador
            if request.user.perfilusuario.rol.rol_nombre.lower() != 'administrador':
                return redirect('acceso-denegado')
                
        except (AttributeError, PerfilUsuario.DoesNotExist):
            return redirect('acceso-denegado')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def socio_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Verificar que tenga perfil de usuario
        try:
            if not hasattr(request.user, 'perfilusuario'):
                return redirect('acceso-denegado')
            
            # Verificar que tenga rol de socio
            if request.user.perfilusuario.rol.rol_nombre.lower() != 'socio':
                return redirect('acceso-denegado')
                
        except (AttributeError, PerfilUsuario.DoesNotExist):
            return redirect('acceso-denegado')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')


def singup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('signin')
            
            except IntegrityError:
                return render(request, 'usuarios/signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'usuario/signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no son iguales'
        })

def login_view(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña incorrectos'
        })
    else:
        login(request, user)
        rol_nombre = getattr(getattr(user.perfilusuario, 'rol', None), 'rol_nombre', '').lower()

        if rol_nombre == 'administrador':
            return redirect('home')
        elif rol_nombre == 'socio':
            return redirect('dashboard')
        else:
            return redirect('login')
       
def signout(request):
    logout(request)
    return redirect ('login')


@login_required
@admin_required
def home(request):
    socios_count = PerfilUsuario.objects.filter(rol__rol_nombre__iexact='Socio').count()
    return render(request, 'home.html', {'categoria_actual': None, 'socios_count': socios_count})

def resultados_busqueda(request, queryset, search_fields):
    
    search_query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    
    if search_query:
        # Crear condiciones OR para cada campo de búsqueda
        conditions = Q()
        for field in search_fields:
            conditions |= Q(**{f"{field}__icontains": search_query})
        
        queryset = queryset.filter(conditions)
    
    if category:
        queryset = queryset.filter(categoria=category)
    
    return queryset, search_query, category