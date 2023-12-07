from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    chave = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=15)
    telefone = models.CharField(max_length=16)
    tipo_publico = models.CharField(max_length=20)
    endereco = models.CharField(max_length=100)
    numero_casa = models.CharField(max_length=50)
    complemento = models.CharField(max_length=50)
    cep = models.CharField(max_length=11)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    tipo_usuario = models.IntegerField(default=0)

class Produtos(models.Model):
    nome = models.CharField(max_length=20)
    preco = models.DecimalField(decimal_places=2, max_digits=20)
    unidade_de_medida = models.CharField(max_length=20)
    estoque = models.CharField(max_length=20)
    imagem = models.ImageField(upload_to='cars', blank=True)

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carrinhos')
    status = models.BooleanField()

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(decimal_places=2, max_digits=20)