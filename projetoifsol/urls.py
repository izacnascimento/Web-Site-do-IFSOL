from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from info.views import login

urlpatterns = [
    path('', include('info.urls')),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuariosAuth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)