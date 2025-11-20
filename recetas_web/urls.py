from django.contrib import admin
from django.urls import path, include 
from django.conf import settings # Para manejar archivos estáticos
from django.conf.urls.static import static # Para manejar archivos multimedia (imágenes)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recetas.urls')), 
    path('', include('django.contrib.auth.urls')), 
    path('registro/', lambda request: None, name='registro'),
    path('perfil/mis-recetas/', lambda request: None, name='dashboard'), 
    path('accounts/', include('django.contrib.auth.urls')), 
    
]

# Configuración para servir archivos multimedia (imágenes) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
