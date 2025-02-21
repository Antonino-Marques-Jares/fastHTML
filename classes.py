from fasthtml.common import dataclass

# Definição da tabela Pessoa
@dataclass
class Pessoa:
    id: int
    nome: str
        
# Definição da tabela cidade
@dataclass
class Cidade:
    id: int
    nome: str
    estado: str
    pais:str
    lat:int
    lng:int
