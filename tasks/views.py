from django.shortcuts import render
from django.http import JsonResponse
from .models import Task
from users.models import User
import json

from users.views import login


# Create your views here.
def home(request):
    #função responsável por chamar a home do site e passar as informações que ela precisa como contexto
    logged = False
    tasks = ''
    #recebe a sessão do usuario caso exista
    user_id = request.session.get('usuario')
    #se existir a sessão
    if user_id:
        logged = True
        #o resultado do filtro é o usuario com sessão aberta
        user = User.objects.filter(id=user_id)[0]
        #o resultado do filtro são as tarefas do usuario com ordem invertida
        tasks = Task.objects.filter(user_id=user).order_by('-id')
    return render(request, 'tasks/home.html', {'logged':logged, 'tasks': tasks})

def new_task(request):
    #função que cria uma nova tarefa
    user_id = request.session.get('usuario')
    result = validate_request(request, user_id)
    #se a request for válida
    if type(result) is dict:
        #o resultado do filtro é o usuario com sessão aberta
        user = User.objects.filter(id=user_id)[0]
        #cria uma nova tarefa no banco de dados
        task = Task(description=result['task'], completed=False, user_id=user)
        task.save()
        return JsonResponse({'success': 'created task'},status=201)
    return result

def update_task(request):
    #função que atualiza uma tarefa
    user_id = request.session.get('usuario')
    result = validate_request(request, user_id)
    #se a request for válida
    if type(result) is dict:
        #o resultado do filtro é o usuario com sessão aberta
        user = User.objects.filter(id=user_id)[0]
        #busca todas as tarefas do usuario
        tasks = Task.objects.filter(user_id=user)
        try:
            #calcula qual é o index da tarefa no banco de dados
            index = len(tasks)-1-result['index']
            #verifica se existe a chave description no corpo da request, caso exista significa que é uma alteração no texto da tarefa
            if 'description' in result:
                tasks[index].description = result['description']
            #senão, será uma alteração no campo completed, que armazena se a tarefa está completa ou não
            elif 'completed' in result and result['completed'] == 'true':
                tasks[index].completed = True
            tasks[index].save()
        except:
            return JsonResponse({'failed': 'task does not exists'}, status=406)
        return JsonResponse({'success': 'changed task'},status=202)
    return result

def delete_task(request):
    #função que deleta uma tarefa
    user_id = request.session.get('usuario')
    result = validate_request(request, user_id)
    #se a request for válida
    if type(result) is dict:
        #o resultado do filtro é o usuario com sessão aberta
        user = User.objects.filter(id=user_id)[0]
        #busca todas as tarefas do usuario
        tasks = Task.objects.filter(user_id=user)
        try:
            #calcula qual é o index da tarefa no banco de dados
            index = len(tasks)-1-result['index']
            #deleta a tarefa
            tasks[index].delete()
        except:
            return JsonResponse({'failed': 'task does not exists'}, status=406)
        return JsonResponse({'success': 'deleted task'},status=202)
    return result

def validate_request(request, user_id):
    #função que verifica se o usuario está logado e a request é um json, se os dois forem verdadeiros o retorno é um json com os dados enviados na requisição
    if not user_id:
        return JsonResponse({'Unauthorized': 'User is not authenticated'}, status=401)
    try:
        return json.load(request)
    except:
        return JsonResponse({'Precondition': 'request data must be json format'}, status=412)