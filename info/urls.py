from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('contato',views.contato, name='contato'),
    path('produtos',views.produtos, name='produtos'),
    path('logcarrinho', views.logcarrinho, name='logcarrinho'),
    path('logperfil', views.logperfil, name='logperfil'),
    path('logcarrinho', views.logcarrinho, name='logcarrinho'),
    path('logperfil', views.logperfil, name='logperfil'),
    path('addcarrinho/<int:id>', views.addcarrinho, name='addcarrinho'),
]
