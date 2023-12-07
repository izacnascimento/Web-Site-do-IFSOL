from django.urls import path
from . import views
# from .views import superuser_management

urlpatterns = [
    path('', views.index, name='index'),
    path('contato',views.contato, name='contato'),
    path('produtos',views.produtos, name='produtos'),
    path('logcarrinho', views.logcarrinho, name='logcarrinho'),
    path('logperfil', views.logperfil, name='logperfil'),
    path('addcarrinho/<int:id>', views.addcarrinho, name='addcarrinho'),
    path('atualizar_quantidade/<int:item_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),
    path('apagar_item_carrinho/<int:item_id>/', views.apagar_item_carrinho, name='apagar_item_carrinho'),    
    path('atualizar_subtotal/<int:item_id>/', views.atualizar_subtotal, name='atualizar_subtotal'),
]