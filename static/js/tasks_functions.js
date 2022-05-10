var task_opened = false

function show_field_task(){
    //função que mostra os campos quando o botão de adicionar tarefa for clicado
    //se não tem uma tarefa aberta
    if (!task_opened) {
        task_opened = true
        show_textarea()
        show_buttons()
    }
}

function show_textarea(){
    //função que mostra o textarea na tela e puxa o foco para ela
    var textarea = document.getElementById('textarea_new_task')
    textarea.style.display = 'inline'
    textarea.focus()
}

function show_buttons(){
    //função que mostra os botões de aprovar e cancelar a tarefa
    var approve_button = document.getElementById('approve_btn_new_task')
    var cancel_button = document.getElementById('cancel_btn_new_task')
    approve_button.style.display = 'inline' 
    cancel_button.style.display = 'inline' 
}

async function save_task(element){
    //função que passa para o servidor uma nova tarefa para ser registrada 
    var task_message = element.value
    //se a mensagem da tarefa não for vazia
    if(task_message.trim() != ''){
        //cria o json que será mandando para o servidor
        var data = {
            'task': task_message
        }
        //chama a função  assincrona de se comunicar com o servidor, se a resposta for true é pq o servidor registrou a tarefa e retornou o esperado
        if(await send_task(data, 'POST', '/new_task/')){
            task_opened = false

            //clona os nodes do dom e passam para outra div
            var row_new_task = document.getElementById('row_new_task')
            var div_tasks = document.getElementById('tasks')
            var row = row_new_task.cloneNode(true)
            row.removeAttribute('id')
            
            var textarea = row.getElementsByTagName('textarea')[0]
            var approve_btn = row.getElementsByTagName('button')[0]
            var cancel_btn = row.getElementsByTagName('button')[1]
            
            textarea.removeAttribute('id')
            textarea.removeAttribute('onblur')
            textarea.addEventListener('blur', update_task)

            approve_btn.removeAttribute('id')
            cancel_btn.removeAttribute('id')

            div_tasks.insertBefore(row, div_tasks.firstChild)
            hide_new_task()
        }
    }
}

function hide_new_task(){
    //esconde os campos da nova tarefa
    var textarea_new_task = document.getElementById('textarea_new_task')
    var approve_btn_new_task = document.getElementById('approve_btn_new_task')
    var cancel_btn_new_task = document.getElementById('cancel_btn_new_task')
    textarea_new_task.value = ''
    textarea_new_task.style.display = 'none'
    approve_btn_new_task.style.display = 'none'
    cancel_btn_new_task.style.display = 'none'
}

function update_task(element){
    //função que atualiza a descrição de uma tarefa
    if(!(element instanceof HTMLElement)){
        element = this
    }
    task_message = element.value
    if(task_message.trim() != ''){
        var i = get_position_task(element)
        var data = {
            'description': task_message,
            'index': i
        }
        send_task(data, 'PUT', '/update_task/')
    }
}

async function delete_task(element){
    //função que deleta uma tarefa
    //se o elemento tiver id é porque ainda é uma nova tarefa e não foi registrada no banco
    if(element.id){
        hide_new_task()
        task_opened = false
    }else{
        var i = get_position_task(element)
        var data = {
            'index': i
        }
        if(await send_task(data, 'DELETE', '/delete_task/')){
            element_parent = element.parentNode.parentNode
            element_parent.remove()
        }
    }
}

async function complete_task(element){
    //função que marca a tarefa como completada
    var i = get_position_task(element)
    var data = {
        'completed': 'true',
        'index': i
    }
    if(await send_task(data, 'PUT', '/update_task/')){
        element_parent = element.parentNode.parentNode
        var textarea = element_parent.getElementsByTagName('textarea')[0]
        textarea.style.color = 'white'
        textarea.style.background = '#198754'
        textarea.style.textDecoration = 'line-through'
    }
}

function get_position_task(element){
    //função que pega a posição da div da tarefa no dom
    element_parent = element.parentNode.parentNode
    tasks = document.getElementById('tasks')
    for(var i=0; i<tasks.children.length; i++){
        if(tasks.children[i] === element_parent){
            return i
        }
    }
    return null
}

async function send_task(data, method, url){
    //função que envia os dados para o servidor, passando o método e url como parâmetros
    return fetch(url,{
        method: method,
        headers: {
            Accept: 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify(data) 
    }).then(
        (res) => {
            if(res.status == 201 || res.status == 202){
                return true
            }
            return false
        }
    )
}