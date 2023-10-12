from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from info.models import Usuario

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
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('index')
        return redirect('login')
        
    else:    
        
        return render (request, 'usuarios/login.html')
             
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
    
    
