from django.contrib import admin

from django.contrib import admin
from .models import Receta, Calificacion

# Registra la Receta
@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion', 'promedio_calificacion')
    search_fields = ('titulo', 'autor__username')

# Registra la Calificación
@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('receta', 'usuario', 'puntuacion')
    list_filter = ('puntuacion',)
