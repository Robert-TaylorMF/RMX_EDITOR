🧾 XMLEditor RM — Documentação do Projeto

🎯 Objetivo
O XMLEditor RM é um aplicativo desktop em Python com interface Tkinter, projetado para editar e atualizar eventos XML presentes na tabela PESOCIALEVENTOS em bancos SQL Server utilizados pela empresa. Ele oferece suporte a diferentes ambientes (Produção, Homologação e Teste) e adapta-se a máquinas com diferentes configurações de driver.

⚙️ Funcionalidades
- 🔌 Conexão inteligente com SQL Server (com fallback entre drivers)
- 📥 Leitura e exibição formatada de eventos XML
- 💾 Salvamento com backup da versão anterior
- 🔍 Verificação de driver ODBC instalado
- 🔄 Verificação de versão e sugestão de atualização
- 🎨 Interface visual moderna e responsiva
- 📁 Estrutura de projeto organizada em módulos

📁 Estrutura de Arquivos
RMX_EDITOR/
│
├── main.py                  # Interface gráfica principal
├── conexao.py               # Lógica de conexão com fallback de driver
├── xml_operacoes.py         # Funções de leitura e gravação de XML
├── verificador.py           # Verifica driver e versão atual
├── versao.json              # Armazena versão local
├── versao.txt               # Versão publicada (online)
├── bases/
│   └── conexoes.json        # Informações das bases disponíveis
├── recursos/                # Imagens e ícones opcionais
└── README.md                # Documentação do projeto



🔌 Conexão com Banco SQL Server
A função obter_conexao() verifica os drivers disponíveis na máquina:
- Tenta conectar com ODBC Driver 17 for SQL Server
- Se falhar, usa SQL Server Native Client 11.0
- Se nenhum funcionar, exibe aviso e encerra aplicação
Informações do servidor, banco, usuário e senha vêm do conexoes.json.

📥 Carregamento de XML
- Busca na tabela PESOCIALEVENTOS o evento com id fornecido
- Formata o conteúdo em XML e exibe no ScrolledText
- Realce de sintaxe e feedback na barra de status

💾 Salvamento de XML
- Realiza backup do campo mensagem antes da alteração
- Atualiza o campo com o novo XML informado
- Exibe mensagem de sucesso e atualiza destaque visual

🔄 Atualização Automática
- Compara VERSAO_ATUAL com conteúdo remoto em versao.txt
- Se houver versão mais recente, sugere ao usuário a atualização
- Permite abrir navegador diretamente na release pública do GitHub

🔍 Verificação de Driver
- Detecta se o driver ODBC necessário está instalado
- Se ausente, exibe messagebox com botão para abrir o site oficial: Download ODBC Driver

🎨 Interface Visual
- Layout com LabelFrame, Radiobutton, ScrolledText e barra de status
- Cores suaves, espaçamento organizado e fontes modernas
- Campo XML cresce automaticamente com redimensionamento da janela
- Seletor de ambiente intuitivo e responsivo

🔐 Boas Práticas Aplicadas
- Separação modular dos componentes
- Conexão resiliente em diferentes máquinas
- Armazenamento limpo e seguro em JSON
- Centralização da versão com VERSAO_ATUAL
- Feedback visual e tratamento de exceções

📦 Distribuição
- Aplicativo empacotado via PyInstaller
- Instalador gerado com inclusão de arquivos essenciais
- Atualização automática (em desenvolvimento)

✉️ Autor
Robert Taylor
Projeto com foco em automação segura de eventos XML no sistema RM.

🚀 Futuras Melhorias
- Tema escuro com ttk.Style
- Validação XML com esquema XSD
- Splash refinado e assistente de conexão
- Log de operação e histórico de edição
