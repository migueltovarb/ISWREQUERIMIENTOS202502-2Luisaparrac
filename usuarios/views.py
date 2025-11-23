from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginForm
from .models import Usuario
from .forms import UsuarioCreateForm, UsuarioEditForm
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from proyectos.models import Tarea, Proyecto
from django.db.models import Count, Q
from django.utils import timezone
import datetime

class CustomLoginView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = False

    def get_success_url(self):
        user = self.request.user

        if not user.is_authenticated:
            return reverse_lazy("usuarios:login")

        if user.rol == Usuario.Rol.ADMIN:
            return reverse_lazy("usuarios:dashboard_admin")

        elif user.rol == Usuario.Rol.JEFE:
            return reverse_lazy("usuarios:dashboard_jefe")

        else:
            return reverse_lazy("usuarios:dashboard_usuario")


@login_required
def dashboard_jefe(request):
    if request.user.rol != Usuario.Rol.JEFE:
        return render(request, "usuarios/no_autorizado.html")
    return render(request, "jefe/dashboard.html")


@login_required
def listar_equipo(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuarios/listar_equipo.html", {"usuarios": usuarios})


@login_required
def dashboard_admin(request):
    if request.user.rol != Usuario.Rol.ADMIN:
        return render(request, "usuarios/no_autorizado.html")
    return render(request, "admin/dashboard_admin.html")


@login_required
def dashboard_usuario(request):
    return render(request, "usuarios/dashboard_usuario.html")


@login_required
def listar_usuarios(request):
    if request.user.rol != Usuario.Rol.ADMIN:
        return render(request, "usuarios/no_autorizado.html")

    qs = Usuario.objects.all().order_by('-id')
    paginator = Paginator(qs, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'usuarios/listar_usuarios.html', {'page_obj': page_obj})


@login_required
def crear_usuario(request):
    if request.user.rol != Usuario.Rol.ADMIN:
        return render(request, "usuarios/no_autorizado.html")

    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente')
            return redirect('usuarios:listar_usuarios')
    else:
        form = UsuarioCreateForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


@login_required
def editar_usuario(request, id):
    if request.user.rol != Usuario.Rol.ADMIN:
        return render(request, "usuarios/no_autorizado.html")

    user = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Usuario actualizado')
                return redirect('usuarios:listar_usuarios')
            except Exception as e:
                # Catch unexpected save errors and surface to the form
                form.add_error(None, 'Error al guardar el usuario: %s' % str(e))
    else:
        form = UsuarioEditForm(instance=user)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'user_obj': user})


@login_required
def eliminar_usuario(request, id):
    if request.user.rol != Usuario.Rol.ADMIN:
        return render(request, "usuarios/no_autorizado.html")

    user = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado')
        return redirect('usuarios:listar_usuarios')
    return render(request, 'usuarios/confirmar_eliminar.html', {'user_obj': user})


@login_required
def reportes_general(request):
    if request.user.rol != Usuario.Rol.ADMIN:
        return render(request, "usuarios/no_autorizado.html")

    today = timezone.now().date()

    # Global counts
    total_completed = Tarea.objects.filter(estado=Tarea.Estado.COMPLETADA).count()
    total_in_progress = Tarea.objects.filter(estado=Tarea.Estado.EN_PROGRESO).count()
    total_pending = Tarea.objects.filter(estado=Tarea.Estado.PENDIENTE).count()
    total_delayed = Tarea.objects.filter(fecha_limite__lt=today).exclude(estado=Tarea.Estado.COMPLETADA).count()

    
    proyectos = Proyecto.objects.all()
    proyectos_data = []
    for p in proyectos:
        tareas = Tarea.objects.filter(proyecto=p)
        proyectos_data.append({
            'proyecto': p,
            'total': tareas.count(),
            'completed': tareas.filter(estado=Tarea.Estado.COMPLETADA).count(),
            'in_progress': tareas.filter(estado=Tarea.Estado.EN_PROGRESO).count(),
            'pending': tareas.filter(estado=Tarea.Estado.PENDIENTE).count(),
            'delayed': tareas.filter(fecha_limite__lt=today).exclude(estado=Tarea.Estado.COMPLETADA).count(),
        })

    week_end = today + datetime.timedelta(days=7)
    month_end = today + datetime.timedelta(days=30)

    date_groups = {
        'today': Tarea.objects.filter(fecha_limite=today).count(),
        'this_week': Tarea.objects.filter(fecha_limite__range=(today, week_end)).count(),
        'this_month': Tarea.objects.filter(fecha_limite__range=(today, month_end)).count(),
    }

    context = {
        'total_completed': total_completed,
        'total_in_progress': total_in_progress,
        'total_pending': total_pending,
        'total_delayed': total_delayed,
        'proyectos_data': proyectos_data,
        'date_groups': date_groups,
    }
   
    users = Usuario.objects.filter(tareas_asignadas__isnull=False).distinct()
    users_data = []
    for u in users:
        tareas_u = u.tareas_asignadas.all()
        total_u = tareas_u.count()
        completed_u = tareas_u.filter(estado=Tarea.Estado.COMPLETADA).count()
        in_progress_u = tareas_u.filter(estado=Tarea.Estado.EN_PROGRESO).count()
        pending_u = tareas_u.filter(estado=Tarea.Estado.PENDIENTE).count()
        delayed_u = tareas_u.filter(fecha_limite__lt=today).exclude(estado=Tarea.Estado.COMPLETADA).count()
        users_data.append({
            'user': u,
            'total': total_u,
            'completed': completed_u,
            'in_progress': in_progress_u,
            'pending': pending_u,
            'delayed': delayed_u,
        })

    context['users_data'] = users_data
    return render(request, 'admin/reportes_general.html', context)
    return render(request, 'admin/reportes_general.html', context)


@login_required
def reporte_usuario(request, id):
    if request.user.rol != Usuario.Rol.ADMIN:
        return render(request, "usuarios/no_autorizado.html")

    user = get_object_or_404(Usuario, id=id)
    tareas = user.tareas_asignadas.all()
    total = tareas.count()
    completed = tareas.filter(estado=Tarea.Estado.COMPLETADA).count()
    delayed = tareas.filter(fecha_limite__lt=timezone.now().date()).exclude(estado=Tarea.Estado.COMPLETADA).count()
    in_progress = tareas.filter(estado=Tarea.Estado.EN_PROGRESO).count()

    percent_complete = int((completed / total) * 100) if total > 0 else 0

    context = {
        'user_obj': user,
        'total': total,
        'completed': completed,
        'delayed': delayed,
        'in_progress': in_progress,
        'percent_complete': percent_complete,
        'tareas': tareas,
    }
    return render(request, 'admin/reporte_usuario.html', context)
    

# Create your views here.
