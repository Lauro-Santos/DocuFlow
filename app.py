import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
import gradio as gr

DB_PATH = Path("documentos.db")

COLUNAS = ["Processo", "Ano", "Tipo Documento", "Documento", "Prefácio"]
TIPOS_COMPARTILHADOS = ["Requerimento", "Moção de congratulação"]
TIPOS_DOCUMENTO = ["Requerimento", "Moção de congratulação", "Decreto", "Projeto de Lei", "Projeto de Camplementar", "Decreto Titulo de cidadão"]

def conectar():
    conn = sqlite3.connect(DB_PATH)
    return conn

def inicializar_bd():
    with conectar() as conn:
        conn.execute(f"""
        CREATE TABLE IF NOT EXISTS documentos (
            Processo INTEGER PRIMARY KEY,
            Ano INTEGER,
            "Tipo Documento" TEXT,
            Documento INTEGER,
            Prefácio TEXT
        )
        """)

inicializar_bd()

def carregar_dados():
    with conectar() as conn:
        cursor = conn.execute("SELECT * FROM documentos ORDER BY Ano, Processo")
        dados = cursor.fetchall()
    return pd.DataFrame(dados, columns=COLUNAS)

def salvar_documento(processo, ano, tipo, documento, prefacio):
    with conectar() as conn:
        conn.execute(
            "INSERT INTO documentos (Processo, Ano, \"Tipo Documento\", Documento, Prefácio) VALUES (?, ?, ?, ?, ?)",
            (processo, ano, tipo, documento, prefacio)
        )

def adicionar_documento(tipo, prefacio, ano, processo_manual=None, documento_manual=None):
    if not tipo or not ano or not prefacio.strip():
        return "Todos os campos devem ser preenchidos.", gr.update(value=carregar_dados()), ""

    try:
        ano = int(ano)
        if ano < 1000 or ano > 9999:
            return "⚠️ O ano deve conter 4 dígitos.", gr.update(value=carregar_dados()), ""
    except ValueError:
        return "⚠️ Ano inválido. Insira um número inteiro de 4 dígitos.", gr.update(value=carregar_dados()), ""

    df = carregar_dados()

    if processo_manual:
        try:
            processo = int(processo_manual)
        except ValueError:
            return "⚠️ Número de processo inválido.", gr.update(value=df), ""
    else:
        processo = 1 if df.empty else df["Processo"].max() + 1

    if documento_manual:
        try:
            documento = int(documento_manual)
        except ValueError:
            return "⚠️ Número de documento inválido.", gr.update(value=df), ""
    else:
        if tipo in TIPOS_COMPARTILHADOS:
            filtro = df[df["Tipo Documento"].isin(TIPOS_COMPARTILHADOS)]
        else:
            filtro = df[df["Tipo Documento"] == tipo]

        documento = 1 if filtro.empty else filtro["Documento"].max() + 1

    salvar_documento(processo, ano, tipo, documento, prefacio)
    return f"✅ Documento adicionado com sucesso!", gr.update(value=carregar_dados()), ""

def listar_documentos(ano):
    df = carregar_dados()
    if ano and ano != "Todos":
        df = df[df["Ano"] == int(ano)]
    return df

def remover_documento(numero_processo):
    with conectar() as conn:
        conn.execute("DELETE FROM documentos WHERE Processo = ?", (numero_processo,))

    df = carregar_dados().reset_index(drop=True)
    df["Processo"] = range(1, len(df) + 1)

    contadores = {}
    documentos = []
    for _, row in df.iterrows():
        tipo = row["Tipo Documento"]
        key = "compartilhado" if tipo in TIPOS_COMPARTILHADOS else tipo
        contadores[key] = contadores.get(key, 0) + 1
        documentos.append(contadores[key])
    df["Documento"] = documentos

    with conectar() as conn:
        conn.execute("DELETE FROM documentos")
        for _, row in df.iterrows():
            conn.execute(
                "INSERT INTO documentos (Processo, Ano, \"Tipo Documento\", Documento, Prefácio) VALUES (?, ?, ?, ?, ?)",
                tuple(row)
            )

    return gr.update(value=carregar_dados())

def editar_prefacio(numero_processo, novo_prefacio):
    with conectar() as conn:
        cur = conn.execute("SELECT 1 FROM documentos WHERE Processo = ?", (numero_processo,))
        if not cur.fetchone():
            return "⚠️ Número de processo não encontrado.", gr.update(value=carregar_dados())

        conn.execute("UPDATE documentos SET Prefácio = ? WHERE Processo = ?", (novo_prefacio, numero_processo))
    return "✏️ Prefácio atualizado com sucesso!", gr.update(value=carregar_dados())

def anos_disponiveis():
    df = carregar_dados()
    return ["Todos"] + sorted(df["Ano"].dropna().unique().astype(int).tolist())

with gr.Blocks(title="Gerenciador de Documentos") as demo:
    with gr.Tab("Adicionar Documento"):
        with gr.Row():
            tipo = gr.Dropdown(label="Tipo de Documento", choices=TIPOS_DOCUMENTO)
            ano = gr.Text(label="Ano", placeholder="YYYY")
        with gr.Row():
            processo_manual = gr.Text(label="Número do Processo")
            documento_manual = gr.Text(label="Número do Documento")
        prefacio = gr.Textbox(label="Prefácio", lines=4, placeholder="Digite o conteúdo do documento aqui...")
        btn_adicionar = gr.Button("Adicionar Documento")
        saida_adicionar = gr.Textbox(label="Status", interactive=False)        

    with gr.Tab("Listar/Remover Documentos"):
        with gr.Row():
            remover_id = gr.Number(label="Número do Processo a Remover")
            btn_remover = gr.Button("Remover")
        with gr.Row():
            ano_filtro = gr.Dropdown(label="Filtrar por Ano (opcional)", choices=anos_disponiveis(), value="Todos")
            btn_filtrar = gr.Button("Filtrar")
        tabela_lista = gr.Dataframe(headers=COLUNAS, datatype=["number", "number", "str", "number", "str"], label="Documentos", interactive=False, value=carregar_dados())

    with gr.Tab("Editar Prefácio"):
        editar_id = gr.Number(label="Número do Processo")
        novo_prefacio = gr.Textbox(label="Novo Prefácio", lines=3)
        btn_editar = gr.Button("Salvar Alterações")
        saida_editar = gr.Textbox(label="Status", interactive=False)

        tabela_documentos = gr.Dataframe(
            headers=COLUNAS, 
            datatype=["number", "number", "str", "number", "str"], 
            label="Documentos", 
            interactive=False,
            value=carregar_dados()  # já mostra os dados ao iniciar
        )

        btn_adicionar.click(
            adicionar_documento,
            inputs=[tipo, prefacio, ano, processo_manual, documento_manual],
            outputs=[saida_adicionar, tabela_documentos, processo_manual]
        )

        btn_remover.click(
            remover_documento,
            inputs=[remover_id],
            outputs=[tabela_lista]
        )

        btn_filtrar.click(
            listar_documentos,
            inputs=[ano_filtro],
            outputs=[tabela_lista]
        )

        btn_editar.click(
            editar_prefacio,
            inputs=[editar_id, novo_prefacio],
            outputs=[saida_editar, tabela_documentos]
        )

        demo.load(
            lambda: gr.update(choices=anos_disponiveis()),
            outputs=[ano_filtro]
        )

demo.launch()
