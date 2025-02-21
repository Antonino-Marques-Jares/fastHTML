from fasthtml.common import database, dataclass

db = None

# Definição da tabela Pessoa
@dataclass
class Pessoa:
    id: int
    nome: str

@dataclass
class Carro:
    id: int
    nome: str

# Inicializa a conexão com o banco
def get_db():
    global db
    db = database("dados.db")
    return db

# Fechar a base de dados
def close_db():
    db_instance = get_db()
    db_instance.close()

def cria_tabelas():
    db = get_db()
    db.create(Pessoa, pk="id")
    close_db()



