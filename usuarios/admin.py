from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("email", "rol", "is_active", "is_staff")
    list_filter = ("rol", "is_staff", "is_active")
    search_fields = ("email",)

# Register your models here.
