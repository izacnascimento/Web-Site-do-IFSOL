from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from info.models import Usuario, Produtos, Carrinho
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['inputName']
        sobrenome = request.POST['inputSurname']
        email = request.POST['inputEmail4']
        senha = request.POST['inputPassword4']
        repetir_senha = request.POST['inputrepsenha']
        cpf = request.POST['inputCPF']
        telefone = request.POST['inputTelefone']
        tipo_publico = request.POST['inputpublico']
        endereco = request.POST['inputAddress']
        numero_casa = request.POST['inputnumero']
        complemento = request.POST['inputAddress2']
        cep = request.POST['inputZip']
        cidade = request.POST['inputCity']
        estado = request.POST['inputState']
        data = {}
        if senha != repetir_senha:
            data['msg'] = 'Senha e Confirma Senha diferentes!'
            data['class'] = 'alert-danger'
            return render(request, 'usuarios/cadastro.html', data)
        else:
            authuser = User.objects.create_user(username=nome, last_name=sobrenome, email=email, password=senha)
            user = Usuario.objects.create(chave=authuser, cpf=cpf, telefone=telefone, tipo_publico=tipo_publico, endereco=endereco, numero_casa=numero_casa, complemento=complemento, cep=cep, cidade=cidade, estado=estado)
            authuser.save()
            user.save()
            return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == "POST":
        email = request.POST['inputEmail4']
        senha = request.POST['inputPassword4']
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = authenticate(request, username=nome, password=senha)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Senha inválida!")
        else:
            messages.error(request, "Email não encontrado!")
        return redirect('login')
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')

def AlterarSenha(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            senha = request.POST['inputPassword4']
            repetir_senha = request.POST['inputrepsenha']
            data = {}
            if senha != repetir_senha:
                data['msg'] = 'Senha e Confirma Senha diferentes!'
                data['class'] = 'alert-danger'
                return render(request, 'usuarios/alterar_senha.html', data)
            else:
                novasenha = User.objects.get(pk=request.user.id)
                novasenha.set_password(senha)
                novasenha.save()
                return redirect('index')
        else:    
            return render(request, 'usuarios/alterar_senha.html')
    else:
        return render(request, 'index.html')

def cadastrarprodutos(request):
    if request.method == 'POST':
        nome = request.POST.get('nomeproduto')
        preco = request.POST.get('precoproduto')
        unidade_de_medida = request.POST.get('unidadeproduto')
        imagem = request.FILES.get('imagemproduto')
        data = {}
        if nome and preco and unidade_de_medida:
            if imagem:
                produto = Produtos.objects.create(nome=nome, preco=preco, unidade_de_medida=unidade_de_medida, imagem=imagem)
            else:
                produto = Produtos.objects.create(nome=nome, preco=preco, unidade_de_medida=unidade_de_medida)
            produto.save()
            data['msg'] = 'Produto cadastrado com Sucesso!'
            data['class'] = 'alert-success'
            return redirect('pgcadastrar')
        else:
            data['msg'] = 'Produto não cadastrado!'
            data['class'] = 'alert-danger'
    else:
        return render(request, 'usuarios/cadastrar_produtos.html')

def pgcadastrar(request):
    listagem_de_produtos = Produtos.objects.all()
    return render(request, 'produtos.html', {'listagem_de_produtos': listagem_de_produtos})

def detalhar_pedido(request, carrinho_id):
    carrinho = get_object_or_404(Carrinho, pk=carrinho_id)
    itens_carrinho = carrinho.itens.all()
    return render(request, 'usuarios/detalhar_pedido.html', {'carrinho': carrinho, 'itens_carrinho': itens_carrinho})

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produtos, id=produto_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nomeproduto', produto.nome)
        preco = request.POST.get('precoproduto', produto.preco)
        unidade_de_medida = request.POST.get('unidadeproduto', produto.unidade_de_medida)
        imagem = request.FILES.get('imagemproduto', produto.imagem)

        if nome and preco and unidade_de_medida:
            produto.nome = nome
            produto.preco = preco
            produto.unidade_de_medida = unidade_de_medida
            if imagem:
                produto.imagem = imagem
            produto.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('pgcadastrar')
        else:
            messages.error(request, 'Erro ao atualizar o produto. Verifique os dados.')

    return render(request, 'usuarios/editar_produto.html', {'produto': produto})

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produtos, id=produto_id)
    
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('pgcadastrar')
    
    return render(request, 'usuarios/excluir_produto.html', {'produto': produto})

def confirmar_compra(request, carrinho_id):
    carrinho = get_object_or_404(Carrinho, id=carrinho_id)

    if request.method == 'POST':
        # Verifica se o usuário confirmou ou rejeitou a compra
        if 'confirmar' in request.POST:
            # Confirma a compra
            carrinho.confirmado = True
            carrinho.save()
            messages.success(request, 'Compra confirmada com sucesso!')
        elif 'rejeitar' in request.POST:
            # Rejeita a compra
            carrinho.confirmado = False
            carrinho.save()
            messages.success(request, 'Compra rejeitada com sucesso!')
        
        # Redireciona para a página de controle após a ação
        return redirect('controle')
    
    # Renderiza a página de confirmação
    return render(request, 'usuarios/confirmar_compra.html', {'carrinho': carrinho})


def excluir_pedido(request, pedido_id):
    pedido = get_object_or_404(Carrinho, id=pedido_id)
    
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido excluído com sucesso!')
        return redirect('controle')
    
    return render(request, 'usuarios/excluir_pedido.html', {'pedido': pedido})

def listar_produtos(request):
    produtos = Produtos.objects.all()
    return render(request, 'produtos.html', {'listagem_de_produtos': produtos})




