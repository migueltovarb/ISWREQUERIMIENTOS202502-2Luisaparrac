"""Add fecha_inicio, fecha_fin and jefe to Proyecto

Generated manually to match current `proyectos.models.Proyecto`.
"""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("proyectos", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='fecha_inicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fecha_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='jefe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proyectos_jefe', to=settings.AUTH_USER_MODEL),
        ),
    ]
