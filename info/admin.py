from django.contrib import admin
from .models import Usuario
from .models import Produtos

admin.site.register(Usuario)
admin.site.register(Produtos)