📄 Documentação do Projeto Fênix
Plataforma Inteligente de Detecção de Fraudes

Versão: 1.0 (Ciclo de Polimento)
Autor: Victor
Data: 14 de Junho de 2025
🗺 Tabela de Conteúdos

    Visão Geral

    ✨ Funcionalidades Principais

    ⚙ Arquitetura e Tecnologias

    🚀 Guia de Instalação e Execução

    📁 Estrutura de Ficheiros Relevantes

    🧠 Fluxo de Análise de IA

    📈 Melhorias Futuras

1. Visão Geral

O Projeto Fênix é uma aplicação web completa desenvolvida com Django, que serve como um centro de comando para analistas de segurança. O seu objetivo é otimizar o processo de deteção de fraudes financeiras, utilizando Inteligência Artificial para analisar lotes de transações e destacar as atividades mais suspeitas num dashboard profissional e interativo. A arquitetura foi desenhada para ser robusta, escalável e proporcionar uma experiência de utilizador fluida.
2. ✨ Funcionalidades Principais

    Sistema de Autenticação Seguro: Controlo de acesso para múltiplos analistas com páginas de login e logout personalizadas.

    Dashboard Interativo: Interface moderna (baseada no template Tabler) com:

        Cards de estatísticas (Total, Pendentes, Confirmadas, Seguras).

        Gráficos dinâmicos (Top 5 Alertas Críticos, Distribuição de Risco) criados com Chart.js.

        Tabela de alertas avançada com pesquisa, ordenação e paginação em tempo real, fornecida por DataTables.js.

    Ingestão de Dados via CSV: Funcionalidade de upload para processar novos lotes de transações.

    Análise com Inteligência Artificial: Utiliza um modelo de Machine Learning (IsolationForest) para detetar anomalias, considerando não apenas o valor da transação, mas também o comportamento histórico do cliente.

    Processamento Assíncrono: Graças à biblioteca django-background-tasks, o processamento de ficheiros CSV ocorre em segundo plano, garantindo que a interface do utilizador nunca fica bloqueada, mesmo com grandes volumes de dados.

3. ⚙ Arquitetura e Tecnologias

O sistema opera com uma arquitetura de múltiplos componentes que se comunicam de forma eficiente.

Fluxo de Dados Simplificado:
Utilizador ➔ Django (Site) ➔ Banco de Dados (Fila) ➔ Processador de Tarefas ➔ Modelo de IA ➔ Banco de Dados (Resultados) ➔ Django (Dashboard)

Stack Tecnológico:

    Backend: Python 3, Django

    Banco de Dados: SQLite (para desenvolvimento)

    Frontend: HTML5, CSS3, JavaScript

    Framework de UI: Tabler (via CDN)

    Bibliotecas JavaScript: jQuery, Chart.js, DataTables.js (via CDN)

    Inteligência Artificial: Scikit-learn, Pandas

    Tarefas em Segundo Plano: django-background-tasks

4. 🚀 Guia de Instalação e Execução

Siga estes passos para configurar o ambiente de desenvolvimento.

Passo 1: Pré-requisitos

    Python 3 instalado.

    Git instalado (opcional, para clonar).

Passo 2: Configuração Inicial

# Clone o repositório (se estiver no Git)
git clone [URL_DO_SEU_REPOSITORIO]
cd painel_fraude_projeto

# Crie e ative um ambiente virtual
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

Passo 3: Instalar Dependências

# Crie um ficheiro requirements.txt primeiro: pip freeze > requirements.txt
pip install -r requirements.txt

# Ou instale manualmente:
pip install django pandas scikit-learn django-background-tasks

Passo 4: Preparar a Aplicação

# Aplique as migrações para criar as tabelas da base de dados
python manage.py migrate

# Crie uma conta de administrador para aceder ao sistema
python manage.py createsuperuser

Passo 5: Treinar o Modelo de IA

    Execute o servidor Django (python manage.py runserver), aceda ao site, faça login e carregue um ficheiro transacoes.csv com dados iniciais para popular a base de dados.

    Depois, pare o servidor e execute o script de treino:

    python treinar_modelo.py

    Isto criará o ficheiro modelo_fraude.joblib.

Passo 6: Iniciar os Processos (em 2 terminais separados)

    Terminal 1 - Processador de Tarefas:

    python manage.py process_tasks

    Terminal 2 - Servidor Web:

    python manage.py runserver

Passo 7: Aceder ao Painel

    Abra o seu navegador e vá para http://127.0.0.1:8000/.

5. 📁 Estrutura de Ficheiros Relevantes

    painel_fraude/settings.py: Ficheiro principal de configuração. Contém as INSTALLED_APPS, as configurações da base de dados e as URLs de login/logout.

    detector/models.py: Define os modelos Transacao e Alerta, que representam as tabelas da base de dados.

    detector/views.py: Contém a lógica das páginas (ex: dashboard, upload_csv). As views são protegidas para exigir autenticação.

    detector/tasks.py: Define a função processar_csv_task que executa o trabalho pesado em segundo plano.

    templates/: Contém todos os ficheiros HTML da aplicação, seguindo a estrutura de templates do Django.

    treinar_modelo.py: Script autónomo para treinar e salvar o modelo de IA.

6. 🧠 Fluxo de Análise de IA

O processo de análise de uma nova transação é o seguinte:

    Agendamento: A view upload_csv recebe o ficheiro e agenda a tarefa processar_csv_task.

    Execução: O worker (process_tasks) executa a tarefa.

    Pré-processamento: Para cada linha do CSV, a tarefa cria um objeto Transacao.

    Análise de Contexto: A função analisar_transacao_com_ml é chamada. Ela consulta a base de dados para obter o histórico do cliente (média de gastos, nº de compras).

    Predição: Os dados da transação atual, juntamente com o contexto do cliente, são enviados para o modelo de IA.

    Geração de Alerta: Se o modelo classificar a transação como uma anomalia (retornando -1), um novo registo Alerta é criado na base de dados com o respetivo score de fraude.

    Visualização: O analista atualiza o dashboard e o novo alerta aparece para análise.

7. 📈 Melhorias Futuras

O Projeto Fênix é uma plataforma sólida, mas com um vasto potencial de expansão:

    Inteligência Explicável (XAI): Aprimorar o modelo para que ele justifique as suas decisões (ex: "Score alto porque o valor da transação é 10x superior à média do cliente").

    API de Ingestão em Tempo Real: Substituir o upload de CSV por uma API REST para análise instantânea de transações.

    Relatórios e Exportação: Adicionar funcionalidades para exportar os alertas e análises para ficheiros PDF ou Excel.

    Sistema de Permissões: Diferenciar os papéis de "Analista" e "Administrador", com diferentes níveis de acesso e funcionalidades.

    Dashboard por Cliente: Criar uma página dedicada a um cliente específico, mostrando o seu histórico completo de transações e alertas.
