from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Usuarios app maneja login y dashboards
    path('', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),

    # Proyectos (exposed bajo /tareas/)
    path('tareas/', include(('proyectos.urls', 'tareas'), namespace='tareas')),
]