import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("documentos.db")

COLUNAS = ["Processo", "Ano", "Tipo Documento", "Documento", "Prefácio"]
TIPOS_COMPARTILHADOS = ["Requerimento", "Moção de congratulação"]
TIPOS_DOCUMENTO = ["Requerimento", "Moção de congratulação", "Decreto", "Projeto de Lei", "Projeto de Camplementar", "Decreto Titulo de cidadão"]

def conectar():
    return sqlite3.connect(DB_PATH)

def inicializar_bd():
    with conectar() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            Processo INTEGER PRIMARY KEY,
            Ano INTEGER,
            "Tipo Documento" TEXT,
            Documento INTEGER,
            Prefácio TEXT
        )
        """)

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

def remover_documento(numero_processo):
    with conectar() as conn:
        conn.execute("DELETE FROM documentos WHERE Processo = ?", (numero_processo,))

def editar_prefacio(numero_processo, novo_prefacio):
    with conectar() as conn:
        conn.execute(
            "UPDATE documentos SET Prefácio = ? WHERE Processo = ?",
            (novo_prefacio, numero_processo)
        )

def anos_disponiveis():
    df = carregar_dados()
    return sorted(df["Ano"].dropna().unique().astype(int))
