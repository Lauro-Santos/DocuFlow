# DocuFlow - Gestão de Documentos Oficiais

**DocuFlow** é um sistema simples e eficiente para o gerenciamento de documentos oficiais, incluindo sua criação, edição e organização. Ideal para processos administrativos, esse sistema oferece uma interface amigável para facilitar o cadastro, a listagem, a remoção e a atualização dos documentos.

## Funcionalidades

- **Adicionar Documento:** Cadastro de novos documentos com tipo, ano, e um prefácio descritivo.
- **Listar Documentos:** Visualização dos documentos cadastrados, com filtro por ano.
- **Remover Documento:** Excluir documentos específicos utilizando o número de processo.
- **Editar Prefácio:** Modificar o conteúdo do prefácio de um documento já registrado.

## Requisitos

- Python 3.7+
- Bibliotecas:
  - `pandas`
  - `gradio`
  
Essas bibliotecas podem ser instaladas utilizando o pip:

```bash
pip install pandas gradio
```

## Como Usar

1. **Clone o repositório ou baixe os arquivos.**

   Se preferir, pode clonar o repositório usando o comando:

   ```bash
   git clone https://github.com/seu-usuario/docuflow.git
   cd docuflow
   ```

2. **Execute o código Python.**

   Para iniciar o sistema, basta executar o arquivo Python principal:

   ```bash
   python app.py
   ```

3. **Interface Gráfica**

   A interface gráfica é construída com o Gradio, onde você pode:
   - Adicionar novos documentos com informações detalhadas.
   - Listar e filtrar documentos por ano.
   - Remover documentos indesejados.
   - Editar o conteúdo do prefácio de qualquer documento.

## Estrutura de Dados

O sistema utiliza um arquivo CSV para armazenar os dados dos documentos com as seguintes colunas:

- **Processo:** Número de identificação do processo.
- **Ano:** Ano do documento.
- **Tipo Documento:** Tipo de documento (ex: Requerimento, Moção de Congratulação, etc.).
- **Documento:** Número único para cada documento do tipo especificado.
- **Prefácio:** Texto completo que descreve o conteúdo do documento.

## Como Funciona

- **Adicionar Documento:** Ao adicionar um documento, o sistema gera automaticamente um número de processo e um número de documento, respeitando a sequência e o tipo de documento.
- **Listar Documentos:** Você pode filtrar os documentos por ano e visualizar todos os dados registrados.
- **Remover Documento:** Ao fornecer o número do processo, o sistema remove o documento e ajusta a sequência de documentos.
- **Editar Prefácio:** Caso precise alterar a descrição de um documento, basta informar o número do processo e inserir o novo texto.

## Personalizações

O tema da interface pode ser alterado conforme o gosto ou necessidade do usuário, utilizando a configuração de tema do Gradio. Além disso, a estrutura de dados pode ser ajustada para atender diferentes tipos de documentos ou formatos de armazenamento.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar o sistema ou adicionar novos recursos, sinta-se à vontade para abrir um *pull request*. 

### Como Contribuir

1. Faça um *fork* deste repositório.
2. Crie uma nova branch para suas mudanças.
3. Faça commit das suas alterações.
4. Envie um *pull request* com uma descrição detalhada das mudanças realizadas.

---

Obrigado por usar o **DocuFlow**! 🚀
```
