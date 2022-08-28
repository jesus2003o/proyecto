from math import perm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import UsuarioForm, ProductoForm, CustomUserCreateForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

def home(request):
    Productos = Producto.objects.all()
    data ={
       'productos' : Productos 
    }
    return render(request, 'app/home.html', data)

def usuario(request):
    data = {
        'form': UsuarioForm()
    }

    if request.method == 'POST':
        formulario = UsuarioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "usario guardado"
        else:
            data["form"] = formulario
    
    return render(request, 'app/usuario.html', data)

def galeria(request):
    return render(request, 'app/galeria.html')

@permission_required('app.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formualrio = ProductoForm(data=request.POST, files=request.FILES)
        if formualrio.is_valid():
            formualrio.save()
            messages.success(request, "modificado correctamente")
            data["mensaje"] = "Guarado Correctamente"
        else: 
            data["form"] = formualrio
    
    return render(request, 'app/producto/agregar.html', data)

@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity' : productos,
        'paginator': paginator
    }
    return render(request, 'app/producto/listar.html', data)

@permission_required('app.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)
    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario= ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_productos")
        data["form"] = formulario

    return render(request, 'app/producto/modificar.html', data)

@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "eliminado correctamente")
    return redirect(to="listar_productos")

def registro(request):
    data = {
        'form': CustomUserCreateForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreateForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)