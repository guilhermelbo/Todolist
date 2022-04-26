from hashlib import sha256
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import User

# Create your views here.
def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'users/cadastro.html', {'status': status})

def login(request):
    status = request.GET.get('status')
    return render(request, 'users/login.html', {'status': status})

def valida_cadastro(request):
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    if len(usuario.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/cadastro/?status=2')
    
    if User.objects.filter(name = usuario):
        return redirect('/cadastro/?status=3')

    if User.objects.filter(email = email):
        return redirect('/cadastro/?status=4')

    try:
        senha = sha256(senha.encode()).hexdigest()
        user = User(name = usuario, email = email, password = senha)
        user.save()
    except:
        return redirect('/cadastro/?status=5')

    return redirect('/')

def valida_login(request):
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()

    usuario = User.objects.filter(name = usuario).filter(password = senha)
    
    if usuario:
        request.session['usuario'] = usuario[0].id
        return redirect('/')
    
    return redirect('/login/?status=1')