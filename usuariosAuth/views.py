from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from info.models import Usuario
from info.models import Produtos
from info.models import Carrinho
from info.models import ItemCarrinho
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def cadastro (request):
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
            return render (request,'usuarios/cadastro.html',data)
        else:
            authuser = User.objects.create_user(username=nome, last_name=sobrenome, email=email,password=senha)
            user = Usuario.objects.create(chave=authuser, cpf=cpf, telefone=telefone, tipo_publico=tipo_publico, endereco=endereco, numero_casa=numero_casa, complemento=complemento, cep=cep, cidade=cidade, estado=estado)
            authuser.save()
            user.save()
            return redirect ('login')
    
    else:
        return render (request, 'usuarios/cadastro.html')

def login(request):
    if request.method == "POST":
        email = request.POST['inputEmail4']
        senha = request.POST['inputPassword4']

        # Verifique se o usuário com o email existe
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            
            # Tente autenticar o usuário com o nome de usuário e senha
            user = authenticate(request, username=nome, password=senha)
            
            if user is not None:
                auth_login(request, user)
                return redirect('index')  # Redireciona para a página inicial.
            else:
                messages.error(request, "Senha inválida!")
        else:
            messages.error(request, "Email não encontrado!")
        
        return redirect('login')  # Redireciona de volta para a página de login

    return render(request, 'usuarios/login.html')
             
def logout (request):
    auth.logout(request)
    return render (request, 'index.html')

def AlterarSenha (request):

    if request.user.is_authenticated:
        if request.method == "POST":
            senha = request.POST['inputPassword4']
            repetir_senha = request.POST['inputrepsenha']
            data = {}
        
            if senha != repetir_senha:
                data['msg'] = 'Senha e Confirma Senha diferentes!'
                data['class'] = 'alert-danger'
                return render (request, 'usuarios/alterar_senha.html', data)
            
            else:
                novasenha = User.objects.get(pk=request.user.id)
                novasenha.set_password(senha)
                novasenha.save()
                
                return redirect('index')
            
        else:    
            return render (request, 'usuarios/alterar_senha.html')
        
        
    else:
        return render (request, 'index.html')
  
def cadastrarprodutos (request):
    if request.method == 'POST':
       
        nome = request.POST.get('nomeproduto')
        preco = request.POST.get('precoproduto')
        unidade_de_medida = request.POST.get('unidadeproduto')
        imagem = request.FILES.get('imagemproduto')
        data = {}
        
        # Verifica se os valores foram recebidos corretamente
        if nome and preco and unidade_de_medida:
            if imagem:
                produto = Produtos.objects.create(nome=nome, preco=preco, unidade_de_medida=unidade_de_medida, imagem=imagem)
            else:
                produto = Produtos.objects.create(nome=nome, preco=preco, unidade_de_medida=unidade_de_medida)
            # Faça a operação com os valores
            prod = Produtos.objects.filter(nome=nome, preco=preco, unidade_de_medida=unidade_de_medida, imagem=imagem)
            produto.save()
            data['msg'] = 'Produto cadastrado com Sucesso!'
            data['class'] = 'alert-success'
            return render (request, 'usuarios/cadastrar_produtos.html', data)
        else:
            data['msg'] = 'Produto não cadastrado!'
            data['class'] = 'alert-danger'
    
    else:
        return render (request, 'usuarios/cadastrar_produtos.html')  

    
def pgcadastrar (request):
        listagem_de_produtos = Produtos.objects.all()
        return render (request, 'usuarios/cadastrar_produtos.html', {'listagem_de_produtos':listagem_de_produtos})

def detalhar_pedido(request, carrinho_id):
    carrinho = get_object_or_404(Carrinho, pk=carrinho_id)
    itens_carrinho = carrinho.itens.all()
    
    # Agora você tem acesso aos itens do carrinho para este usuário
    # e pode passá-los para o seu template para exibição
    
    return render(request, 'usuarios/detalhar_pedido.html', {'carrinho': carrinho, 'itens_carrinho': itens_carrinho})

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('listar_produtos')
        else:
            messages.error(request, 'Erro ao atualizar o produto. Verifique os dados.')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})

def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('listar_produtos')
    return render(request, 'confirmar_exclusao.html', {'produto': produto})



# @login_required
# def confirmar_compra(request, carrinho_id):
#     if request.user.is_superuser:
#         carrinho = get_object_or_404(Carrinho, pk=carrinho_id)
#         carrinho.confirmado = True
#         carrinho.save()
#         return redirect('pagina_de_confirmacao')  # Redirecione para a página de confirmação ou outra página desejada após a confirmação
#     else:
#         # Se o usuário não for um superusuário, talvez você queira redirecioná-lo para outra página ou exibir uma mensagem de erro
#         return redirect('pagina_de_erro')