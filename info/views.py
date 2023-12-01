from django.shortcuts import render, redirect
from .models import Produtos
from .models import Carrinho
from .models import ItemCarrinho
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from rest_framework import status

def index (request):
    return render (request, 'index.html')

def login (request):
    if request.method == "POST":
        email = request.POST['inputEmail4']
        senha = request.POST['inputPassword4']
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            
        return redirect('login')
    else:
        
        data = {}
        data['msg'] = 'Email ou Senha inválidos!'
        data['class'] = 'alert-danger'
        return render (request, 'login.html',data)

def contato (request):
    return render (request, 'contato.html')

def produtos (request):
    listagem_de_produtos = Produtos.objects.all()
    busca_de_produtos = request.GET.get('busca_de_produtos')
    if busca_de_produtos:
        listagem_de_produtos = listagem_de_produtos.filter(nome__icontains=busca_de_produtos)
    dados = {
        'listagem_de_produtos' : listagem_de_produtos
    }
    return render (request, 'produtos.html', dados)


def logcarrinho (request):
    if request.user.is_authenticated:  
        carrinho = request.user.carrinhos.filter(status = True).last()
        itens = carrinho.itens.all()
        return render (request, 'usuarios/logcarrinho.html', {'itens' : itens})
    else:
        return render (request, 'index.html')

def logperfil (request):
    
    if request.user.is_authenticated:
        pessoa = Usuario.objects.get(chave=request.user)
        
        if request.POST:
            telefone = request.POST['inputTelefone']
            endereço = request.POST['inputAddress']
            numero_casa = request.POST['inputnumero']
            complemento = request.POST['inputAddress2']
            cep = request.POST['inputZip']
            cidade = request.POST['inputCity']
            estado = request.POST['inputState']
            
            
            pessoa.telefone = telefone
            pessoa.endereco = endereço
            pessoa.numero_casa = numero_casa
            pessoa.complemento = complemento
            pessoa.cep = cep
            pessoa.cidade = cidade
            pessoa.estado = estado
            request.user.save()
            pessoa.save()
            
            return redirect ('index')
                
        else:
            return render (request, 'usuarios/logperfil.html')
        
    else:
        return render (request, 'index.html')

def addcarrinho (request, id):
    produto = Produtos.objects.get(id=id)
    carrinho =  request.user.carrinhos.filter(status = True).last()
    if carrinho is None:
        carrinho = Carrinho() 
        carrinho.usuario = request.user
        carrinho.status = True
        carrinho.save()

    p = carrinho.itens.filter(produto__id=id).first()

    if p is None:    
        ic = ItemCarrinho(carrinho = carrinho, produto = produto, quantidade = 0)
        ic.save()
        carrinho.itens.add(ic)
        carrinho.save()
    
    item = carrinho.itens.filter(produto__id= id).first()
    item.quantidade+= 1
    item.save()