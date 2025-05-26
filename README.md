# DocuFlow - Gerenciador de Documentos Legislativos

**DocuFlow** é um sistema simples e eficiente para o gerenciamento de documentos oficiais, incluindo sua criação, edição e organização. Ideal para processos administrativos, esse sistema oferece uma interface amigável para facilitar o cadastro, a listagem, a remoção e a atualização dos documentos. Utiliza **Gradio** para a interface gráfica e **SQLite** como banco de dados local.

## 🚀 Funcionalidades

- Adicionar novos documentos com numeração automática ou manual.
- Editar o conteúdo do "Prefácio" dos documentos.
- Listar e filtrar documentos por ano.
- Remover documentos com reordenação automática de numeração.
- Interface gráfica simples e acessível via navegador.

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- [Gradio](https://gradio.app/) (interface gráfica)
- SQLite (banco de dados local)
- pandas (manipulação de dados)

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Lauro-Santos/DocuFlow.git
cd gerenciador-documentos
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo:
```bash
python app.py
```
## 📁 Estrutura do Projeto

```bash
📂 gerenciador-documentos
├── app.py             # Interface Gradio e lógica principal
├── database.py        # Conexão e operações com SQLite
├── documentos.db      # Arquivo do banco de dados (gerado automaticamente)
├── requirements.txt   # Lista de dependências do projeto
├── .gitignore         # Arquivos e pastas ignoradas pelo Git
└── README.md          # Este arquivo
```
### 📝 Licença
Este projeto é open source e distribuído sob a licença MIT. Sinta-se à vontade para contribuir ou adaptá-lo!

