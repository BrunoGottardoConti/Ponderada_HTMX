from tinydb import TinyDB
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'db.json')
# Inicialização do banco de dados
db = TinyDB('db.json')
logs_table = db.table('logs')
