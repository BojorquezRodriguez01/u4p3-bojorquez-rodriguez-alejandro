# core/views.py — CÓDIGO COMPLETO
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Servicio
from .forms import ServicioForm

# Vista de inicio
def inicio(request):
    info_bd = connection.settings_dict
    contexto = {
        'motor': info_bd['ENGINE'],
        'host': info_bd['HOST'],
    }
    return render(request, 'core/inicio.html', contexto)

# Listado filtrado solo por el usuario actual
@login_required
def servicios(request):
    consulta = request.GET.get('q', '').strip()
    lista_servicios = Servicio.objects.filter(propietario=request.user)
    if consulta:
        lista_servicios = lista_servicios.filter(
            Q(titulo__icontains=consulta)
            | Q(descripcion__icontains=consulta)
            | Q(categoria__icontains=consulta)
        )

    page_obj = Paginator(lista_servicios.order_by('id'), 10).get_page(
        request.GET.get('page')
    )
    return render(request, 'core/servicios.html', {
        'servicios': page_obj,
        'page_obj': page_obj,
        'consulta': consulta,
    })

# Crear un nuevo servicio asignando automáticamente el propietario
@login_required
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.propietario = request.user
            nuevo.save()
            return redirect('servicios')
    else:
        form = ServicioForm()
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Nuevo servicio'})

# Editar solo si el servicio pertenece al usuario
@login_required
def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Editar servicio'})

# Eliminar solo si el servicio pertenece al usuario
@login_required
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicios')
    return render(request, 'core/servicio_confirm_delete.html', {'servicio': servicio})

# Registro de nuevos usuarios
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario_nuevo = form.save()
            login(request, usuario_nuevo)
            messages.success(request, f'Cuenta creada. ¡Bienvenido, {usuario_nuevo.username}!')
            return redirect('servicios')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

# Inicio de sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Sesión iniciada correctamente.')
            return redirect('servicios')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Cierre de sesión
def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')