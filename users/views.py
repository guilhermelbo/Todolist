from hashlib import sha256
from django.shortcuts import redirect, render
from .models import User

# Create your views here.
def cadastro(request):
    #função que chama a tela de cadastro, caso o usuario esteja logado redireciona para a home
    if request.session.get('usuario'):
        return redirect('/')
    status = request.GET.get('status')
    return render(request, 'users/cadastro.html', {'status': status})

def login(request):
    #função que chama a tela de login, caso o usuario esteja logado redireciona para a home
    if request.session.get('usuario'):
        return redirect('/')
    status = request.GET.get('status')
    return render(request, 'users/login.html', {'status': status})

def valida_cadastro(request):
    #função que valida os dados e salvo o cadastro do usuario no banco de dados
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    #se usuario e email não estão vazios
    if usuario and email:
        #se usuario ou email tem apenas espaços em branco
        if len(usuario.strip()) == 0 or len(email.strip()) == 0:
            return redirect('/cadastro/?status=1')
        #se o tamanho da senha é menor que 8 digitos
        if len(senha) < 8:
            return redirect('/cadastro/?status=2')
        #se existe algum usuario com esse nome
        if User.objects.filter(name = usuario):
            return redirect('/cadastro/?status=3')
        #se existe algum usuario com esse email
        if User.objects.filter(email = email):
            return redirect('/cadastro/?status=4')

        try:
            #criptografa a senha com hash sha256
            senha = sha256(senha.encode()).hexdigest()
            #cria e registra o usuario
            user = User(name = usuario, email = email, password = senha)
            user.save()
        except:
            return redirect('/cadastro/?status=5')
    else:
        return redirect('/cadastro/?status=1')

    return redirect('/login/?status=2')

def valida_login(request):
    #função que valida os dados e faz o login do usuario
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    #se o usuario e a senha não estão vazios
    if usuario and senha:
        #criptografa a senha com hash sha256
        senha = sha256(senha.encode()).hexdigest()
        #busca na tabela usuario algum usuario com o nome e a senha que foram passados
        usuario = User.objects.filter(name = usuario).filter(password = senha)
        #se o usuario existir
        if usuario:
            #inicia uma sessão e redireciona para a home
            request.session['usuario'] = usuario[0].id
            return redirect('/') 

    return redirect('/login/?status=1')

def logout(request):
    #função que faz o logout do usuario limpando a session e redirecionando para a tela de login
    request.session.flush()
    return redirect('/login/')