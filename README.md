# entityGenerator
pequeno sistema que permite criar entidades com CRUD em REST.


# Getting Started
O micro-serviço pode ser acessado pelo link:
https://entitygenerator.herokuapp.com/

Se houver a necessidade de instalação local utilizar o comando pip install -r requirements.txt dentro da raiz do projeto.

# Prerequisites
Python == 3.7
O restante dos pré-requisitos estão disponíveis no arquivo requirements.txt.

# Api Usage
#Cadastro da entidade-
Clicar no botão novo modelo e especificar os parametro e o nome da entidade. Após salvar todos os recursos básicos da API estarão disponíveis.
Exemplo: Empregados{ nome: String, idade:Integer}

GET-
Retorna a lista de todos os objetos da entidade 
Exemplo: https://entitygenerator.herokuapp.com/empregados

GETID-
Retorna o objeto com o ID especificado
Exemplo: https://entitygenerator.herokuapp.com/empregados/2

POST-
Insere um objeto com os atributos definidos no request no banco de dados
Exemplo: https://entitygenerator.herokuapp.com/empregados
{"nome":"Lucas Josino", "idade":24}

PUT-
Atualiza o objeto com o ID especificado com os atributos definidos no request
Exemplo: https://entitygenerator.herokuapp.com/empregados/2
{"nome":"Lucas Josino Goncalves", "idade":23}

DELETE-
Remove o objeto com o ID especificado
Exemplo: https://entitygenerator.herokuapp.com/empregados/2

# Author
Lucas Josino de Paula Gonçalves 
