from django.urls import path
from .views import CustomLoginView, dashboard_jefe, listar_equipo, dashboard_admin, dashboard_usuario
from .views import listar_usuarios, crear_usuario, editar_usuario, eliminar_usuario
from .views import reportes_general, reporte_usuario
from django.contrib.auth.views import LogoutView

app_name = "usuarios"

urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="usuarios:login"), name="logout"),

    path("dashboard/jefe/", dashboard_jefe, name="dashboard_jefe"),
    path("dashboard/admin/", dashboard_admin, name="dashboard_admin"),
    path("dashboard/usuario/", dashboard_usuario, name="dashboard_usuario"),

    path("equipo/", listar_equipo, name="listar_equipo"),
    
    # Usuarios CRUD (admin)
    path("usuarios/listar/", listar_usuarios, name="listar_usuarios"),
    path("usuarios/crear/", crear_usuario, name="crear_usuario"),
    path("usuarios/editar/<int:id>/", editar_usuario, name="editar_usuario"),
    path("usuarios/eliminar/<int:id>/", eliminar_usuario, name="eliminar_usuario"),
    
    # Reportes (admin)
    path("reportes/", reportes_general, name="reportes_general"),
    path("reportes/usuario/<int:id>/", reporte_usuario, name="reporte_usuario"),
]
