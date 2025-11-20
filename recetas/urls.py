from django.urls import path
from . import views 
from .views import RegistroUsuario, TodasLasRecetasListView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # HOME: Muestra el listado de todas las recetas
    path('', views.RecetaListView.as_view(), name='home'), 

    path('recetas/', views.TodasLasRecetasListView.as_view(), name='todas-recetas'),
    
    # DETALLE: Muestra una receta específica por su ID (pk)
    path('receta/<int:pk>/', views.RecetaDetailView.as_view(), name='receta-detalle'),
    
    # CREAR: Formulario para que el usuario suba una nueva receta
    path('receta/nueva/', views.RecetaCreateView.as_view(), name='receta-crear'),
    path('receta/<int:receta_id>/calificar/', views.calificar_receta, name='calificar-receta'),
    path('registro/', views.RegistroUsuario.as_view(), name='registro'), 
    path('perfil/mis-recetas/', views.DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    
    
    
    
    # Pendientes: Actualizar (Editar) y Borrar (Eliminar)
    # path('receta/<int:pk>/editar/', views.RecetaUpdateView.as_view(), name='receta-editar'),
    # path('receta/<int:pk>/borrar/', views.RecetaDeleteView.as_view(), name='receta-borrar'),
]