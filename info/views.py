from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Produtos
from .models import Usuario
from .models import Carrinho
from .models import ItemCarrinho
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from rest_framework import status
# from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render

# @staff_member_required
# def superuser_management(request):
#     # Lógica para gerenciar os dados
#     # ...

#     return render(request, 'usuarios/superuser.html')

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
        carrinho =  request.user.carrinhos.filter(status = True).last()
        itens = carrinho.itens.all()
        total = 0
        for i in itens:
            total += i.produto.preco * i.quantidade
        return render (request, 'usuarios/logcarrinho.html', {'itens': itens, 'total': total,})
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
        ic = ItemCarrinho(carrinho = carrinho, produto = produto, quantidade = 0, subtotal = 0)
        ic.save()
        carrinho.itens.add(ic)
        carrinho.save()
    
    item = carrinho.itens.filter(produto__id= id).first()
    item.quantidade+= 1
    item.subtotal = item.quantidade * item.produto.preco 
    item.save()

def atualizar_quantidade(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(ItemCarrinho, pk=item_id)

        nova_quantidade_str = request.GET.get('nova_quantidade')
        if nova_quantidade_str is not None:
            try:
                nova_quantidade = int(nova_quantidade_str)
                if nova_quantidade >= 0:  # Verifica se a quantidade é um número positivo
                    item.quantidade = nova_quantidade
                    item.subtotal = nova_quantidade * item.produto.preco
                    item.save()

                    subtotal = item.produto.preco * nova_quantidade   
                    return JsonResponse({'message': 'Quantidade atualizada com sucesso.', 'subtotal': subtotal})
                else:
                    return JsonResponse({'error': 'A quantidade deve ser um número positivo.'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Valor inválido para quantidade.'}, status=400)
        else:
            return JsonResponse({'error': 'Campo nova_quantidade ausente na requisição.'}, status=400)

    return JsonResponse({}, status=400)

def apagar_item_carrinho(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(ItemCarrinho, pk=item_id)
        item.delete()
        return JsonResponse({'message': 'Item apagado com sucesso.'})

    return JsonResponse({}, status=400)

def atualizar_subtotal(request, item_id):
    item = ItemCarrinho.objects.get(pk=item_id)
    item.quantidade = quantidade
    subtotal = item.produto.preco * quantidade
        
    return subtotal