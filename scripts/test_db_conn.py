import traceback
from database.db import Database
from sqlalchemy import inspect

try:
    db = Database()
    engine = db.get_engine()
    conn = engine.connect()
    print('Conectado ao banco com sucesso.')
    insp = inspect(engine)
    try:
        tables = insp.get_table_names()
        print('Tabelas visíveis no schema:', tables)
    except Exception as e:
        print('Erro ao listar tabelas:', e)
    conn.close()
except Exception as e:
    print('Falha ao conectar ao banco:')
    traceback.print_exc()
