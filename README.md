Documentação da Aplicação SD_Helper (Django)

1. Introdução

Este documento descreve a aplicação ExpertHelper, um sistema web desenvolvido com Python (Django) para auxiliar na resolução de problemas técnicos. A aplicação utiliza uma planilha Excel (troubleshooting.xlsx) como base de dados para guiar os usuários através de fluxos de perguntas e respostas até encontrar uma solução.

2. Arquitetura da Aplicação

A aplicação ExpertHelper segue a arquitetura Model-Template-View (MTV) do Django:

    Model: Embora esta versão utilize diretamente uma planilha Excel como fonte de dados, em aplicações Django mais complexas, os modelos definiriam a estrutura do banco de dados. Neste caso, a planilha Excel atua como nosso "modelo" de dados.
    Template: São os arquivos HTML (index.html, flow.html, error.html) responsáveis pela apresentação da interface do usuário. Eles utilizam a linguagem de templates do Django para exibir dados dinâmicos fornecidos pelas views.
    View: As classes (IndexView, FlowView) no arquivo views.py contêm a lógica de negócios da aplicação. Elas processam as requisições HTTP, interagem com os dados (lendo a planilha Excel) e decidem qual template renderizar e quais dados passar para ele.

3. Estrutura de Arquivos e Pastas

ExpertHelper/
├── XHelper/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Arquivo de configurações do Django
│   ├── urls.py             # Configurações de URLs do projeto
│   └── wsgi.py
├── todos_documentos/
│   └── troubleshooting.xlsx # Base de dados com os fluxos
├── core/                   # Aplicativo Django principal
│   ├── __init__.py
│   ├── admin.py            # Configurações do painel de administração (não utilizado extensivamente nesta versão)
│   ├── apps.py             # Configuração do aplicativo 'core'
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py           # Definição de modelos de dados (não utilizado diretamente nesta versão)
│   ├── templates/
│   │   ├── index.html      # Página inicial com a lista de aplicações
│   │   ├── flow.html       # Tela de perguntas e soluções do fluxo
│   │   └── error.html      # Página de erro genérica
│   ├── urls.py             # Configurações de URLs do aplicativo 'core'
│   └── views.py            # Lógica de negócios da aplicação (Views)
├── manage.py               # Script utilitário do Django
└── requirements.txt        # Lista de dependências do projeto

4. Funcionamento da Aplicação

    Leitura da Planilha (carregar_planilha):
        A função carregar_planilha(path) (definida em core/views.py) utiliza a biblioteca pandas para ler todas as abas do arquivo Excel troubleshooting.xlsx.
        Cada aba da planilha é interpretada como uma aplicação/sistema diferente, e seu conteúdo representa o fluxo de resolução de problemas para essa aplicação.
        A função retorna um dicionário onde as chaves são os nomes das abas (aplicações) e os valores são DataFrames do pandas contendo os dados do fluxo.
        Espera-se que cada aba da planilha tenha as seguintes colunas:
            ID: Identificador único para cada nó do fluxo (pergunta ou solução).
            Tipo: Indica se o nó é uma "pergunta" ou uma "solucao".
            Texto: O conteúdo da pergunta ou a descrição da solução.
            Próx. Sim: O ID do próximo nó a ser exibido se a resposta à pergunta for "Sim". (Apenas para nós do tipo "pergunta").
            Próx. Não: O ID do próximo nó a ser exibido se a resposta à pergunta for "Não". (Apenas para nós do tipo "pergunta").

    Página Inicial (/):
        A view IndexView (em core/views.py) é responsável por exibir a página inicial.
        Ela chama a função carregar_planilha para obter a lista de aplicações (nomes das abas do Excel).
        Renderiza o template index.html, passando a lista de aplicações para serem exibidas como links.
        Cada link direciona para a URL inicial do fluxo de uma aplicação específica (/<aplicacao>/).

    Fluxo de Perguntas e Soluções (/<aplicacao>/<node_id>/):
        A view FlowView (em core/views.py) lida com a exibição das perguntas e soluções.
        Ela recebe o nome da aplicação (aplicacao) e, opcionalmente, o node_id como parâmetros na URL.
        Ao acessar /<aplicacao>/ sem um node_id, a view carrega o fluxo da aplicação e redireciona para o primeiro nó do fluxo (assumindo que o primeiro ID na planilha é o ponto de partida).
        Para um node_id específico, a view:
            Carrega o fluxo de dados da aplicação correspondente.
            Localiza o nó (linha) na planilha com o ID fornecido.
            Verifica o Tipo do nó:
                Se for "pergunta", exibe o Texto da pergunta e os botões "Sim" e "Não". Os links desses botões direcionam para o próximo nó definido nas colunas Próx. Sim e Próx. Não, respectivamente.
                Se for "solucao", exibe o Texto da solução e botões para reiniciar o fluxo (voltando para a URL inicial da aplicação) ou voltar para a página inicial.
            Renderiza o template flow.html, passando os dados do nó atual para serem exibidos.
        Se a aplicação ou o node_id não forem encontrados, a view renderiza o template error.html com uma mensagem apropriada.

5. HTML Templates

    index.html:
        Exibe um título ("Selecione uma Aplicação").
        Itera sobre a lista de aplicacoes passada pela IndexView.
        Cria um link para cada aplicação, utilizando a tag de template {% url 'flow_inicio' aplicacao=aplicacao %} para gerar a URL correta.

    flow.html:
        Exibe o nome da aplicacao como título.
        Mostra o texto da pergunta ou da solução.
        Condicionalmente (usando {% if tipo == "pergunta" %}):
            Exibe os botões "Sim" e "Não".
            Os links dos botões são gerados usando {% url 'flow' aplicacao=aplicacao node_id=proximo_sim %} e {% url 'flow' aplicacao=aplicacao node_id=proximo_nao %} para direcionar para o próximo nó com base na resposta.
        Condicionalmente (usando {% elif tipo == "solucao" %}):
            Exibe uma mensagem indicando que a solução foi encontrada.
            Oferece links para reiniciar o fluxo ({% url 'flow_inicio' aplicacao=aplicacao %}) e voltar à página inicial ({% url 'index' %}).
        Exibe mensagens de erro, se houver ({% if mensagem %}).

    error.html (Opcional):
        Exibe um título de erro e a mensagem de erro passada pela view.
        Oferece um link para voltar à página inicial ({% url 'index' %}).

6. Manutenção e Expansão

    Adição de Novas Aplicações:
        Para adicionar um novo fluxo de resolução de problemas para uma nova aplicação ou sistema, basta criar uma nova aba na planilha troubleshooting.xlsx.
        O nome da aba será automaticamente detectado e exibido como um novo link na página inicial.
        Certifique-se de que a nova aba siga a mesma estrutura de colunas (ID, Tipo, Texto, Próx. Sim, Próx. Não).

    Estrutura dos Fluxos:
        A lógica do fluxo é definida inteiramente na planilha Excel. Para modificar um fluxo existente ou criar um novo, edite as linhas e colunas da aba correspondente.
        Garanta que os valores nas colunas Próx. Sim e Próx. Não correspondam aos IDs de outros nós válidos dentro da mesma aba (aplicação).

7. Requisitos e Instalação

    Python: Versão compatível com Django (geralmente Python 3.x).
    Django: Framework web Python.
    pandas: Biblioteca para análise de dados (usada para ler a planilha Excel).
    openpyxl: Biblioteca para leitura de arquivos Excel (necessária para o pandas ler arquivos .xlsx).

Instalação:

    Certifique-se de ter o Python instalado em seu sistema.
    Abra o terminal ou prompt de comando.
    Navegue até a pasta raiz do projeto (ExpertHelper).
    Crie um ambiente virtual (recomendado):
    Bash

python -m venv venv
source venv/bin/activate  # No Linux/macOS
venv\Scripts\activate  # No Windows

Instale as dependências listadas no arquivo requirements.txt:
Bash

    pip install -r requirements.txt

8. Execução

    No terminal ou prompt de comando (com o ambiente virtual ativado, se utilizado), navegue até a pasta raiz do projeto (ExpertHelper).
    Execute o servidor de desenvolvimento do Django:
    Bash

    python manage.py runserver

    Abra seu navegador web e acesse o endereço http://127.0.0.1:8000/. A página inicial com a lista de aplicações deverá ser exibida.

9. Considerações Finais

Esta aplicação demonstra uma forma simples de criar um sistema de suporte guiado utilizando uma planilha Excel como base de dados. Para aplicações mais complexas e com maior volume de dados, seria recomendado migrar para um banco de dados relacional tradicional gerenciado pelo Django ORM (Object-Relational Mapper). No entanto, para prototipagem rápida e casos de uso mais simples, essa abordagem pode ser eficiente. A principal vantagem é a facilidade de manutenção e expansão dos fluxos diretamente na planilha Excel por pessoas que podem não ter conhecimento técnico em programação.
