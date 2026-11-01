import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "clinica.db")

def get_connection():
    """Retorna uma conexão com o banco de dados SQLite com suporte a dicionários."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa as tabelas do banco de dados caso não existam."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            email TEXT NOT NULL,
            celular TEXT NOT NULL,
            servico TEXT NOT NULL,
            data_preferencial TEXT,
            horario_preferencial TEXT,
            observacoes TEXT,
            status TEXT DEFAULT 'Pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def criar_agendamento(nome_completo, email, celular, servico, data_preferencial=None, horario_preferencial=None, observacoes=None):
    """Insere um novo agendamento no banco de dados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agendamentos (nome_completo, email, celular, servico, data_preferencial, horario_preferencial, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nome_completo.strip(), email.strip().lower(), celular.strip(), servico.strip(), data_preferencial, horario_preferencial, observacoes))
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return novo_id

def listar_agendamentos(status=None, busca=None):
    """Lista todos os agendamentos com opções de filtro."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM agendamentos WHERE 1=1"
    params = []

    if status and status.lower() != 'todos':
        query += " AND status = ?"
        params.append(status)

    if busca:
        query += " AND (nome_completo LIKE ? OR celular LIKE ? OR email LIKE ?)"
        termo = f"%{busca}%"
        params.extend([termo, termo, termo])

    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    registros = cursor.fetchall()
    conn.close()
    return registros

def obter_agendamento_por_id(agendamento_id):
    """Retorna os dados de um agendamento específico."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agendamentos WHERE id = ?", (agendamento_id,))
    registro = cursor.fetchone()
    conn.close()
    return registro

def atualizar_status(agendamento_id, novo_status):
    """Atualiza o status de um agendamento."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE agendamentos SET status = ? WHERE id = ?", (novo_status, agendamento_id))
    conn.commit()
    conn.close()

def excluir_agendamento(agendamento_id):
    """Exclui um agendamento pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (agendamento_id,))
    conn.commit()
    conn.close()

def obter_estatisticas():
    """Retorna contadores de agendamentos agrupados por status."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END) as pendentes,
            SUM(CASE WHEN status = 'Confirmado' THEN 1 ELSE 0 END) as confirmados,
            SUM(CASE WHEN status = 'Concluído' THEN 1 ELSE 0 END) as concluidos,
            SUM(CASE WHEN status = 'Cancelado' THEN 1 ELSE 0 END) as cancelados
        FROM agendamentos
    """)
    stats = cursor.fetchone()
    conn.close()
    return {
        "total": stats["total"] or 0,
        "pendentes": stats["pendentes"] or 0,
        "confirmados": stats["confirmados"] or 0,
        "concluidos": stats["concluidos"] or 0,
        "cancelados": stats["cancelados"] or 0
    }

if __name__ == "__main__":
    init_db()
    print("Banco de dados SQLite inicializado com sucesso!")
