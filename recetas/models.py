from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Modelo principal para la Receta
class Receta(models.Model):
    DIFICULTAD_CHOICES = [
        ('FACIL', 'Fácil'),
        ('MEDIO', 'Medio'),
        ('DIFICIL', 'Difícil'),
    ]
    CATEGORIA_CHOICES = [
        ('Pasta', 'Pasta'),
        ('Ensalada', 'Ensalada'),
        ('Postre', 'Postre'),
        ('Plato Principal', 'Plato Principal'),
        ('Desayuno', 'Desayuno'),
        ('Vegetariana', 'Vegetariana'),
        # Añade más categorías según necesites
    ]

    autor = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    ingredientes = models.TextField(
        help_text="Lista los ingredientes separados por líneas o puntos."
    )
    pasos = models.TextField(
        help_text="Explica los pasos de preparación de forma detallada."
    )
    imagen = models.ImageField(upload_to='recetas_pics/', default='recetas_pics/default.png') # Añade default si quieres una imagen por defecto

    # Nuevos campos
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='Plato Principal')
    
    dificultad = models.CharField(
        max_length=10, 
        choices=DIFICULTAD_CHOICES, 
        default='FACIL',
        help_text="Nivel de complejidad de la receta."
    )
    tiempo_preparacion = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: '30 min', '1 hora'")
    porciones = models.IntegerField(blank=True, null=True, help_text="Número de personas para las que rinde la receta")

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def promedio_calificacion(self):
        calificaciones = self.calificacion_set.aggregate(models.Avg('puntuacion'))
        return calificaciones['puntuacion__avg'] if calificaciones['puntuacion__avg'] is not None else 0
    
    def get_absolute_url(self):
        return reverse('receta-detalle', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.titulo
    
# Modelo para la Calificación (el sistema de 1 a 5 estrellas)
class Calificacion(models.Model):
    # Relaciona la calificación a la Receta
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    # Relaciona la calificación al Usuario que calificó
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Puntuación de 1 a 5
    puntuacion = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    
    class Meta:
        # Esto asegura que un usuario solo puede calificar una receta una vez
        unique_together = ('receta', 'usuario')

    def __str__(self):
        return f'{self.receta.titulo} - {self.puntuacion} estrellas por {self.usuario.username}'
