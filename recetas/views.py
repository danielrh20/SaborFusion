from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Receta, Calificacion
from django.contrib.auth.mixins import LoginRequiredMixin # Para restringir acceso
from django.contrib.auth.decorators import login_required # Para la nueva vista
from django.contrib import messages # type: ignore # Para enviar mensajes al usuario
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.db.models import Q, Count, Max
from django.contrib.auth import login

# 1. Vista para Listar todas las Recetas (HOME)
class RecetaListView(ListView):
    model = Receta
    template_name = 'recetas/home.html' 
    context_object_name = 'recetas' 
    ordering = ['-fecha_creacion'] 
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | 
                Q(descripcion__icontains=query) | 
                Q(ingredientes__icontains=query) 
            ).distinct() 
        
        # Lógica de Filtrado por Categoría (GET 'categoria')
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categorias_disponibles'] = Receta.CATEGORIA_CHOICES
        return context    
    
# 2. Vista para Mostrar el Detalle de una Receta
class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'recetas/receta_detalle.html' 

# 3. Vista para Crear una Nueva Receta (Requiere Login)
class RecetaCreateView(LoginRequiredMixin, CreateView):
    model = Receta
    template_name = 'recetas/receta_form.html'
    fields = [
        'titulo', 
        'descripcion', 
        'ingredientes', 
        'pasos', 
        'imagen', 
        'categoria', 
        'dificultad',
        'tiempo_preparacion', 
        'porciones'
    ]
    success_url = '/' # Redirige al inicio después de subirla.
    def form_valid(self, form):
        form.instance.autor = self.request.user 
        return super().form_valid(form)
    
# 4. Vista para calificar una receta (Requiere Login)
@login_required
def calificar_receta(request, receta_id):
    # Asegura que solo procesamos solicitudes POST (cuando el usuario envía el formulario)
    if request.method == 'POST':
        # 1. Obtiene la receta o devuelve un error 404
        receta = get_object_or_404(Receta, pk=receta_id)
        
        # 2. Obtiene la puntuación del formulario (debe ser un número)
        puntuacion = request.POST.get('puntuacion')
        
        if puntuacion:
            try:
                puntuacion = int(puntuacion)
                if 1 <= puntuacion <= 5:
                    # 3. Intenta crear o actualizar la calificación
                    Calificacion.objects.update_or_create(
                        receta=receta,
                        usuario=request.user,
                        defaults={'puntuacion': puntuacion} # Si ya existe, actualiza la puntuación
                    )
                    messages.success(request, f'¡Receta calificada con {puntuacion} estrellas!')
                else:
                    messages.error(request, 'La puntuación debe ser entre 1 y 5.')
            except ValueError:
                messages.error(request, 'La puntuación enviada no es válida.')
        
        # 4. Redirige de vuelta a la página de detalle de la receta
        return redirect('receta-detalle', pk=receta_id)
    
# 5. Vista para el Registro de Usuario
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Puedes iniciar sesión automáticamente aquí si lo deseas, pero por ahora solo redirigimos a login
            messages.success(request, 'Cuenta creada exitosamente. ¡Por favor, inicia sesión!')
            return redirect('login') 
    else:
        form = UserCreationForm()
        
    return render(request, 'recetas/registro.html', {'form': form})

# 6. Dashboard del Usuario (ListView filtrada)
class DashboardView(LoginRequiredMixin, ListView):
    model = Receta
    template_name = 'recetas/dashboard_base.html'
    context_object_name = 'mis_recetas'
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        # Filtra las recetas para mostrar SÓLO las del usuario actual
        return Receta.objects.filter(autor=self.request.user)

class RegistroUsuario(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
    
# 7. Nueva Vista para la página Acerca de
def acerca_de(request):
    """Renderiza la página Acerca de."""
    # Nota: El template que creamos fue 'acerca_de.html'.
    # Si estás siguiendo las convenciones de Django, debería estar en 'recetas/acerca_de.html'.
    return render(request, 'recetas/acerca_de.html', {})


def lista_categorias(request):
    """
    Vista para mostrar una lista de todas las categorías,
    incluyendo el número de recetas y la imagen de la receta más reciente.
    """
    # 1. Obtener todas las categorías únicas y contar las recetas.
    categorias_con_conteo = Receta.objects.values('categoria').annotate(
        num_recetas=Count('categoria')
    ).order_by('categoria')

    # 2. Obtener la imagen de la receta más reciente para cada categoría.
    #    Obtenemos todas las recetas, ordenadas por fecha descendente.
    recetas_por_categoria = Receta.objects.order_by('categoria', '-fecha_creacion').distinct('categoria')

    # 3. Crear un diccionario de mapeo {categoria: url_imagen}
    imagen_mapeo = {
        receta.categoria: receta.imagen.url
        for receta in recetas_por_categoria
    }
    
    # 4. Combinar los datos.
    for item in categorias_con_conteo:
        # Añadir la URL de la imagen al diccionario de la categoría
        item['imagen_url'] = imagen_mapeo.get(item['categoria'], None)
        
    context = {
        'categorias': categorias_con_conteo,
        'page_title': 'Categorías de Recetas'
    }
    return render(request, 'recetas/categorias.html', context)
    
    # 8. Nueva Vista para "Todas las Recetas" (Página principal del menú)
class TodasLasRecetasListView(RecetaListView):
    """
    Hereda de RecetaListView. Sobrescribe el template y la paginación.
    - Usa 'recetas/todas_las_recetas.html' para el diseño de listado completo.
    - Muestra 8 recetas por página (en lugar de las 4 del home/destacadas).
    """
    template_name = 'recetas/todas_las_recetas.html' # ⬅️ Nuevo Template
    paginate_by = 8 # ⬅️ 8 recetas por página