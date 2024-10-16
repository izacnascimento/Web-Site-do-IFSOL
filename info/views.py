from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Produtos
from .models import Usuario
from .models import Carrinho
from .models import ItemCarrinho
from django.http import JsonResponse

def superuser (request):
    carrinhos_confirmados = Carrinho.objects.filter(confirmado=True)
    lista = Carrinho.objects.filter(ativo=False,confirmado=False)
    return render (request, 'usuarios/superuser.html', {'lista':lista,'carrinhos_confirmados': carrinhos_confirmados})

def index (request):
    return render (request, 'index.html')

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
        carrinho =  request.user.carrinhos.filter(ativo = True).last()
        hist =  request.user.carrinhos.filter(ativo = False)

        if carrinho is None:
            carrinho = Carrinho(usuario = request.user)
            carrinho.save()
        itens = carrinho.itens.all()
        total = 0
        for i in itens:
            total += i.produto.preco * i.quantidade
        return render (request, 'usuarios/logcarrinho.html', {'itens': itens, 'total': total, 'carrinho':carrinho, 'hist':hist})
    else:
        return render (request, 'index.html')

@login_required
def logperfil(request):
    if request.user.is_authenticated:
        # Tente buscar o usuário com o "get_object_or_404"
        try:
            pessoa = Usuario.objects.get(chave=request.user)

            if request.method == 'POST':
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
                
                pessoa.save()  # Salvar as alterações feitas
                return redirect('index')

            else:
                return render(request, 'usuarios/logperfil.html', {'pessoa': pessoa})

        except Usuario.DoesNotExist:
            # Aqui você pode redirecionar para uma página de erro ou criar o usuário
            # Caso deseje redirecionar para uma página de registro, você pode fazer assim:
            return redirect('login')  # Substitua pelo nome da view de registro
    
    else:
        return redirect('index')  # Redirecionar não autenticados para a página inicial


@login_required
def addcarrinho (request, id):
    produto = Produtos.objects.get(id=id)
    carrinho =  request.user.carrinhos.filter(ativo = True).last()
    if carrinho is None:
        carrinho = Carrinho() 
        carrinho.usuario = request.user
        carrinho.ativo = True
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
    if request.method == 'DELETE':
        item = ItemCarrinho.objects.filter(pk=item_id).first()
        if item:
            item.delete()
            return JsonResponse({'success': True})  # Retorna um JSON de sucesso
        return JsonResponse({'success': False, 'error': 'Item não encontrado.'}, status=404)

    return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)

def exclui_produto(request, item_id):
    if request.method == 'GET':
        produto = get_object_or_404(Produtos, pk=item_id)
        produto.delete()
        # return redirect('pgcadastrar')  # Redireciona para a página correta após a exclusão
    return redirect('pgcadastrar') 

def atualizar_subtotal(request, item_id):
    # Obtém o item do carrinho usando o item_id
    item = ItemCarrinho.objects.get(pk=item_id)

    # Recupera a quantidade da requisição (supondo que ela seja enviada via GET ou POST)
    quantidade_str = request.GET.get('quantidade') or request.POST.get('quantidade')

    # Verifica se a quantidade foi fornecida
    if quantidade_str:
        try:
            # Converte a quantidade para inteiro
            quantidade = int(quantidade_str)

            # Verifica se a quantidade é positiva
            if quantidade >= 0:
                # Atualiza a quantidade e o subtotal do item
                item.quantidade = quantidade
                item.subtotal = item.produto.preco * quantidade
                item.save()  # Salva as alterações no banco de dados
                
                # Retorna o subtotal diretamente
                subtotal = item.subtotal
                return subtotal
            else:
                return JsonResponse({'error': 'A quantidade deve ser um número positivo.'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Valor inválido para quantidade.'}, status=400)
    else:
        return JsonResponse({'error': 'Quantidade não fornecida.'}, status=400)


def finalizar_carrinho (request, id):
    carrinho = Carrinho.objects.get(id=id)
    if carrinho is not None:
        carrinho.ativo = False
        carrinho.save()
    return redirect ('logcarrinho')

@login_required
def confirmar_compra(request, carrinho_id):
    if request.user.is_superuser:  # Verifica se o usuário é superusuário
        # Obtém o carrinho ativo ou retorna 404 se não existir
        carrinho = get_object_or_404(Carrinho, pk=carrinho_id, ativo=True)
        
        # Marcar o carrinho como confirmado e inativo
        carrinho.confirmado = True
        carrinho.ativo = False  # Torna o carrinho inativo após a confirmação
        carrinho.save()  # Salva as alterações

        return redirect('controle')  # Redireciona para a página de controle após a confirmação
    else:
        return redirect('controle')  # Redireciona se o usuário não for superusuário


@login_required
def excluir_item_carrinho(request, carrinho_id, produto_id):
    carrinho = get_object_or_404(Carrinho, id=carrinho_id)
    produto = get_object_or_404(Produtos, id=produto_id)

    if request.method == 'POST':
        item = carrinho.itens.filter(produto=produto).first()
        if item:
            item.delete()
    return redirect('logcarrinho')

