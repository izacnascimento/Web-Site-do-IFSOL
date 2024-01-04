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
    
def login (request):
    
    if request.method == "POST":
        email = request.POST['inputEmail4']
        senha = request.POST['inputPassword4']
        
        # if request.user.is_authenticated and request.user.is_superuser:
        #         # Se for um superusuário, redirecione para a página do superusuário
        #         return HttpResponseRedirect(reverse_lazy('superuser_management'))
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                if user.is_superuser:
                    return redirect('controle')
                else:
                    return redirect('index')
        return redirect('login')
        
    else:    
        data = {}
        data['msg'] = 'Email ou Senha inválidos!'
        data['class'] = 'alert-danger'
        return render (request, 'usuarios/login.html',data)
             
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