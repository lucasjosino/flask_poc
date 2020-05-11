window.onload = entityPopulate();

// adiciona um novo input no modal
function addItem(){
    form = document.getElementById("form");
    row = document.createElement("div");
    row.className = "row";
    row.innerHTML = '<input name="nomecampo" required type="text" placeholder="Nome da propriedade..." /><select name="tipo"><option value="string">String</option><option value="integer">Integer</option><option value="decimal">Decimal</option><option value="date">Date</option></select>'
   form.appendChild(row); 
}

// popula a tela com as entidades já cadastradas no banco
function entityPopulate(){
    var entities;
    $.ajax({
        method: "GET",
        url: "/entities",
            success: function (data) {
                entities = data;
                for (entity in entities)
                {
                    addEntity(entities[entity])
                }
            },
    });
}

function addEntityModal(){
    modal = document.getElementById("modal");
    modal.style.display = "flex";
}

function addEntity(entityName){
    entities = document.getElementById("groupEntities");

    fullEntity = document.createElement("div");
    fullEntity.className = "fullEntity";

    entity = document.createElement("div");
    entity.className = "entity";
    entity.innerText = entityName;
    entity.style.background = 'linear-gradient(90deg, #'+(Math.random()*0xFFFFFF<<0).toString(16)+' 0%, #'+ (Math.random()*0xFFFFFF<<0).toString(16) +' 45%, #'+ (Math.random()*0xFFFFFF<<0).toString(16) +' 100%)'
    if(entity.style.background == "")
    {
        entity.style.background = 'linear-gradient(90deg, #'+(Math.random()*0xFFFFFF<<0).toString(16)+' 0%, #'+ (Math.random()*0xFFFFFF<<0).toString(16) +' 100%)'
    }
    optionsentity = document.createElement("div");
    optionsentity.className = "optionsEntity";
    optionsentity.innerHTML = '<div onclick=entityModal("'+entityName+'","get") class="get">Get</div><div onclick=entityModal("'+entityName+'","getid") class="getid">Get ID</div><div onclick=entityModal("'+entityName+'","post") class="post">Post</div><div onclick=entityModal("'+entityName+'","put") class="put">Put</div><div onclick=entityModal("'+entityName+'","delete") class="delete">Delete</div>'
    
    fullEntity.appendChild(entity);
    fullEntity.appendChild(optionsentity);
    
    entities.appendChild(fullEntity);
}

function closeModal(){
    var modalEntity = document.getElementById("modalEntity")
    modal.style.filter = "opacity(0)";
    modalEntity.style.display = "none";
}

function entityModal(entityName,method){
    modal = document.getElementById("modalEntity");
    nome = document.getElementById("nameEntity");
    link = document.getElementById("linkEntity");
    content = document.getElementById("content");
    resultado = document.getElementById("resultado");
    nome.innerText = entityName;

    if (method == 'get')
    {
        link.innerHTML = "<a href='/"+entityName.toLowerCase()+"'>/"+entityName+"</a>"
        content.innerHTML = "Método de requisição HTTP GET"
    }
    else if (method == 'getid')
    {
        link.innerText = "/"+entityName+"/id"
        content.innerHTML = "Método de requisição HTTP GET"
    }
    else if (method == 'delete')
    {
        link.innerText = "/"+entityName
        content.innerHTML = "Método de requisição HTTP DELETE e ID do objeto deletado"
    }
    else if (method == 'put')
    {
        link.innerText = "/"+entityName
        content.innerHTML = "Método de requisição HTTP PUT e dados que serão atualizados"
    }
    else if (method == 'post')
    {
        console.log("entrou!")
        link.innerText = "/"+entityName
        content.innerHTML = "Método de requisição HTTP POST e dados que serão inseridos"
        datax = {id:2,nome:"josino",idade:"Francanalha"}
        $.ajax({
            method: "POST",
            url: "/"+entityName.toLowerCase(),
            contentType: "application/json",                                                                                                                                                                                                                                                    
            data: JSON.stringify(datax),
                success: function (data) {
                },
                error: function (data) {
                    alert("houve algum problema!");
                },
        });
    }
    modal.style.filter = "opacity(1)";
    modal.style.display = "flex";   
}

function salvarEntity(){
    var form = document.getElementById("form");
    if(form.reportValidity())
    {
        $.ajax({
        method: "POST",
        url: "/cadastramodelo",
        data: $('form').serialize(),
            success: function (data) {
                console.log(data);
                window.location.reload();
            },
            error: function (data) {
                erro = document.getElementById("erro");
                erro.innerText ="Ocorreu algum problema! tente conferir os campos ou atualizar a página.";
            },
        });
    }
    
}