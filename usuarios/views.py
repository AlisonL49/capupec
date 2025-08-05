from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from operativo.views import obtener_saldo_usuario_por_id
from .models import PerfilUsuario, Roles, EstadoCivil
from .forms import UsuarioForm
from sistema.views import admin_required


@admin_required
def crear_usuario(request):
    roles = Roles.objects.all()
    estado_civil = EstadoCivil.objects.all()

    search_query = request.GET.get('q', '').strip()
    perfiles = PerfilUsuario.objects.select_related('user')

    if search_query:
        perfiles = perfiles.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(cedula__icontains=search_query) 
        )

    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit':
            socio_id = request.POST.get('socio_id')
            try:
                perfil = PerfilUsuario.objects.get(id=socio_id)
                user = perfil.user
                form = UsuarioForm(request.POST, instance=perfil)
                if form.is_valid():
                    user.first_name = request.POST.get('first_name', user.first_name)
                    user.last_name = request.POST.get('last_name', user.last_name)
                    user.email = request.POST.get('email', user.email)
                    user.save()
                    perfil = form.save(commit=False)
                    perfil.user = user
                    perfil.save()
                    messages.success(request, "Socio actualizado exitosamente.")
                    return redirect('crear_usuario')
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f" {field} {error}")
            except PerfilUsuario.DoesNotExist:
                messages.error(request, "El socio no existe.")
                return redirect('crear_usuario')
        
        elif action == 'delete':
            socio_id = request.POST.get('socio_id')
            try:
                perfil = PerfilUsuario.objects.get(id=socio_id)
                socio_name = f"{perfil.user.first_name} {perfil.user.last_name}"
                user = perfil.user
                perfil.delete()
                user.delete()
                messages.success(request, f"Socio {socio_name} eliminado exitosamente.")
                return redirect('crear_usuario')
            except PerfilUsuario.DoesNotExist:
                messages.error(request, "El socio no existe.")
                return redirect('crear_usuario')
        
        else:
            # Crear nuevo socio
            form = UsuarioForm(request.POST)
            if form.is_valid():
                cedula = form.cleaned_data['cedula']
                first_name = request.POST.get('first_name', '')
                last_name = request.POST.get('last_name', '')
                email = request.POST.get('email', '')
                # Crear usuario base
                user = User.objects.create_user(
                    username=cedula,
                    password=cedula,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                # Crear perfil
                perfil = form.save(commit=False)
                perfil.user = user
                perfil.save()
                messages.success(request, "Socio creado exitosamente.")
                return redirect('crear_usuario')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f" {field} {error}")
    else:
            form = UsuarioForm()
            
    return render(request, 'operativo/socios.html', {
        'titulo': 'Operativo',
        'categoria_actual': 'operativo',
        "form": form,
        'estado_civil': estado_civil,
        'roles': roles,
        'perfiles': perfiles,
        'search_query': search_query,
        
    })


def buscar_usuarios(request):
    q = request.GET.get('q', '').strip()
    usuarios = PerfilUsuario.objects.select_related('user')

    if q:
        usuarios = usuarios.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) 
        ).values( 'user__id', 'user__first_name', 'user__last_name','cedula', 'nombramiento', 'lugar_trabajo', 'user__date_joined')
        
        resultados = []
        for u in usuarios:
            saldo = obtener_saldo_usuario_por_id(u['user__id'])  
            resultados.append({
                'id': u['user__id'],  # ID del perfil, no del usuario
                'nombre': f"{u['user__first_name']} {u['user__last_name']}",
                'cedula': u['cedula'],
                'nombramiento': u['nombramiento'],
                'lugarTrabajo': u['lugar_trabajo'],  # Corregido el nombre del campo
                'fechaApertura': u['user__date_joined'].strftime('%Y-%m-%d'),
                'saldo': saldo,
            })
    else:
        resultados = []
    return JsonResponse(resultados, safe=False)



