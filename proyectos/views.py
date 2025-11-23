from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .forms import TareaForm, ProyectoForm, ProyectoEditForm
from .models import Tarea
from usuarios.models import Usuario
from .forms import ProyectoForm
from .models import Proyecto
from django.core.paginator import Paginator
from django.contrib import messages

@login_required
def crear_tarea(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tareas:listar_tareas")
    else:
        form = TareaForm()
    
    return render(request, "proyectos/crear_tareas.html", {"form": form})

@login_required
def listar_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, "proyectos/listar_tareas.html", {"tareas": tareas})


@login_required
def listar_proyectos(request):
    proyectos = Proyecto.objects.all().order_by('-id')
    paginator = Paginator(proyectos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'proyectos/listar_proyectos.html', {'page_obj': page_obj})


@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tareas:listar_proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear_proyecto.html', {'form': form})


@login_required
def editar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)

    if request.method == 'POST':
        form = ProyectoEditForm(request.POST, instance=proyecto)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Proyecto actualizado correctamente')
                return redirect('tareas:listar_proyectos')
            except Exception as e:
                form.add_error(None, 'Error al guardar el proyecto: %s' % str(e))
    else:
        form = ProyectoEditForm(instance=proyecto)

    return render(request, 'proyectos/editar_proyecto.html', {'form': form, 'proyecto': proyecto})

@login_required
def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)

    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect("tareas:listar_tareas")
    else:
        form = TareaForm(instance=tarea)

    return render(request, "proyectos/editar_tarea.html", {"form": form, "tarea": tarea})

@login_required
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    tarea.delete()
    return redirect("tareas:listar_tareas")

def listar_equipo(request):
    usuarios = Usuario.objects.all().prefetch_related("tareas_asignadas")
    return render(request, "usuarios/listar_equipo.html", {
        "usuarios": usuarios
    })

@login_required
def editar_estado(request, id):
    tarea = get_object_or_404(Tarea, id=id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")

        if nuevo_estado in dict(Tarea.Estado.choices).keys():
            tarea.estado = nuevo_estado
            tarea.save()
            return redirect("usuarios:listar_equipo")

    return render(request, "proyectos/editar_estado.html", {
        "tarea": tarea,
        "estados": Tarea.Estado.choices
    })
# Create your views here.
