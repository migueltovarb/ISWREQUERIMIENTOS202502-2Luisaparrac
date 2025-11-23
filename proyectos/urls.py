from django.urls import path
from .views import crear_tarea, listar_tareas, editar_tarea, eliminar_tarea, editar_estado, listar_proyectos, crear_proyecto, editar_proyecto

app_name = "tareas"

urlpatterns = [
    path("crear/", crear_tarea, name="crear_tarea"),
    path("", listar_tareas, name="listar_tareas"),
    path("editar/<int:id>/", editar_tarea, name="editar_tarea"),
    path("eliminar/<int:id>/", eliminar_tarea, name="eliminar_tarea"),
    path("estado/<int:id>/", editar_estado, name="editar_estado"),
    path("proyectos/", listar_proyectos, name="listar_proyectos"),
    path("proyectos/crear/", crear_proyecto, name="crear_proyecto"),
    path("proyectos/editar/<int:id>/", editar_proyecto, name="editar_proyecto"),
]