import pandas as pd
import gradio as gr
import os
from datetime import datetime

# Caminho do CSV no Google Drive
caminho_csv = '/content/drive/MyDrive/processos.csv'
colunas = ["Processo", "Ano", "Tipo Documento", "Documento", "Prefácio"]

def carregar_dados():
    if os.path.exists(caminho_csv):
        try:
            df = pd.read_csv(caminho_csv)
            if list(df.columns) != colunas:
                raise ValueError("Cabeçalho incorreto")
        except Exception:
            df = pd.DataFrame(columns=colunas)
            df.to_csv(caminho_csv, index=False)
    else:
        df = pd.DataFrame(columns=colunas)
        df.to_csv(caminho_csv, index=False)
    return df

def salvar_dados(df):
    df.to_csv(caminho_csv, index=False)

def gerar_numero(df, tipo):
    numero_processo = 1 if df.empty else df["Processo"].max() + 1

    tipos_compartilhados = ["Requerimento", "Moção de congratulação"]
    if tipo in tipos_compartilhados:
        filtro = df[df["Tipo Documento"].isin(tipos_compartilhados)]
    else:
        filtro = df[df["Tipo Documento"] == tipo]

    if filtro.empty:
        numero_documento = 1
    else:
        numero_documento = filtro["Documento"].max() + 1

    return numero_processo, numero_documento

def adicionar_documento(tipo, prefacio, ano):
    if not prefacio.strip():
        return "Prefácio não pode estar vazio.", carregar_dados(), ""

    df = carregar_dados()
    numero_processo, numero_documento = gerar_numero(df, tipo)
    novo = pd.DataFrame([[numero_processo, int(ano), tipo, numero_documento, prefacio]], columns=colunas)
    df = pd.concat([df, novo], ignore_index=True)
    salvar_dados(df)
    return f"Documento adicionado com sucesso!", df, ""

def listar_documentos(ano):
    df = carregar_dados()
    if ano and ano != "Todos":
        df = df[df["Ano"] == int(ano)]
    return gr.update(value=df)

def remover_documento(numero_processo):
    df = carregar_dados()
    df = df[df["Processo"] != numero_processo]

    df = df.sort_values(by=["Ano", "Processo"]).reset_index(drop=True)
    df["Processo"] = range(1, len(df) + 1)

    df["Documento"] = 0
    tipos_compartilhados = ["Requerimento", "Moção de congratulação"]
    contadores = {}

    for i, row in df.iterrows():
        tipo = row["Tipo Documento"]
        key = "compartilhado" if tipo in tipos_compartilhados else tipo
        contadores[key] = contadores.get(key, 0) + 1
        df.at[i, "Documento"] = contadores[key]

    salvar_dados(df)
    return gr.update(value=df)

def anos_disponiveis():
    df = carregar_dados()
    return sorted(df["Ano"].dropna().unique().astype(int))

def editar_prefacio(numero_processo, novo_prefacio):
    df = carregar_dados()
    if numero_processo not in df["Processo"].values:
        return "Número de processo não encontrado.", df
    df.loc[df["Processo"] == numero_processo, "Prefácio"] = novo_prefacio
    salvar_dados(df)
    return "Prefácio atualizado com sucesso!", df

# Interface Gradio
custom_theme = gr.Theme(
    primary_hue="blue",
    secondary_hue="indigo",
    neutral_hue="gray",
    font=["Inter", "sans-serif"]
)

with gr.Blocks(theme=custom_theme, css="""
    body { background-color: #f9fafb; }
    .gr-box { border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); padding: 16px; }
    .gr-button { font-weight: bold; }
    .gr-input, .gr-textbox, .gr-dropdown { border-radius: 8px; }
    .gr-dataframe { background-color: #fff; border-radius: 8px; overflow: auto; }
""") as app:
    gr.Markdown("""
    # 🗂️ Gestão de Documentos Oficiais
    Sistema para cadastro, edição e organização de documentos.
    """)
    with gr.Tabs():
        with gr.TabItem("➕ Adicionar Documento"):
            with gr.Row():
                tipo_input = gr.Dropdown(label="Tipo de Documento", choices=["Requerimento", "Moção de congratulação", "Decreto", "Projeto de Lei", "Decreto Titulo de cidadão"], interactive=True)
                ano_input_add = gr.Dropdown(label="Ano", choices=[str(a) for a in range(2000, datetime.now().year+2)], value=str(datetime.now().year), interactive=True)
            prefacio_input = gr.Textbox(label="Prefácio", lines=6, max_lines=10, placeholder="Digite o prefácio completo aqui...")
            adicionar_btn = gr.Button("➕ Adicionar Documento", variant="primary")
            msg_output = gr.Textbox(label="Status", interactive=False)
            tabela_output = gr.Dataframe(label="Lista Atualizada de Documentos")

            adicionar_btn.click(adicionar_documento, inputs=[tipo_input, prefacio_input, ano_input_add], outputs=[msg_output, tabela_output, prefacio_input])
            tabela_output.value = carregar_dados()

        with gr.TabItem("📋 Listar e Remover") as tab_listar:
            ano_input = gr.Dropdown(label="Filtrar por Ano", choices=["Todos"] + [str(a) for a in anos_disponiveis()], value="Todos", interactive=True)
            tabela_listagem = gr.Dataframe(label="Documentos Filtrados", value=carregar_dados())
            ano_input.change(fn=listar_documentos, inputs=ano_input, outputs=tabela_listagem)
            tab_listar.select(lambda: listar_documentos(""), outputs=tabela_listagem)

            gr.Markdown("### 🗑️ Remover Documento por Número de Processo")
            with gr.Row():
                numero_remover = gr.Number(label="Número do Processo", precision=0)
                remover_btn = gr.Button("🗑️ Remover", variant="stop")
            remover_btn.click(remover_documento, inputs=numero_remover, outputs=tabela_listagem)

            gr.Markdown("### ✏️ Editar Prefácio de Documento")
            with gr.Row():
                numero_editar = gr.Number(label="Número do Processo", precision=0)
                novo_prefacio = gr.Textbox(label="Novo Prefácio", lines=4)
                editar_btn = gr.Button("✏️ Atualizar Prefácio", variant="primary")
                editar_msg = gr.Textbox(label="Status", interactive=False)
            editar_btn.click(editar_prefacio, inputs=[numero_editar, novo_prefacio], outputs=[editar_msg, tabela_listagem])

app.launch()
