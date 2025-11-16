from django.contrib import admin 
from django.urls import path 
from vehiclesapp.views import create_view
from vehiclesapp.views import list_view
from vehiclesapp.views import update_view
from vehiclesapp.views import delete_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', list_view),
    path('create/', create_view),
    path('update/<int:id>/', update_view),
    path('delete/<int:id>/', delete_view),
    
]