from django.contrib import admin
from .models import Usuario, Produtos

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'telefone', 'tipo_usuario')

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque')