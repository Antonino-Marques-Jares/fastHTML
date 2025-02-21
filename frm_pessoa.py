from fasthtml.common import fast_app, Div, Titled, Hr, Button, Form, Fieldset, Input, Table, Tr, Th, Td, A,Label, database, dataclass, Script, Redirect
from constantes import NUMERO_REGISTROS_POR_PAGINA, REGEX_VALIDAR
from SGBD import get_db
from componentes import caixa_mensagem
from classes import Pessoa
import re

# Configuração do FastHTML
app, rt = fast_app()
db = get_db()
#Cria a Tabela com base na sua classe
db_pessoa = db.create(Pessoa, pk="id")

# Função para limpar o formulário
def limpar_formulario():
    return Script("document.getElementById('nome-input').value = '';")

# Formulário da Tabela 
@rt("/frm/pessoa")
def frm_pessoa(page: int = 1, edit_id: int = None, mensagem: str = None):
    # Exibe a mensagem, se houver
    mensagem_div = Div(id="mensagem", style="margin-top: 10px; color: green; font-weight: bold;")
    if mensagem:
        if "sucesso" in mensagem.lower():
            mensagem_div = caixa_mensagem("sucesso", mensagem)
        else:
            mensagem_div = caixa_mensagem("erro", mensagem)

    if edit_id:
        pessoa = db_pessoa.get(edit_id)
        if not pessoa:
            return caixa_mensagem("erro", "Pessoa não encontrada!")

        form = Form(
            Fieldset(
                Input(name="nome", id="ipt-nome", value=pessoa.nome),
                Button("💾 Salvar", type="submit", style="background:#FFD700; color:black; border:none; padding:8px 12px; cursor:pointer;"),
                Button(
                    "🔙 Voltar",
                    type="button",
                    onclick=f"window.location.href='/frm/pessoa?page={page}'",
                    style="background:#007bff; color:white; border:none; padding:8px 12px; cursor:pointer;"
                ),
                role="group",
                style="display: flex; gap: 10px;"
            ),
            hx_post=f"/salvar/pessoa/{edit_id}?page={page}",  
            hx_target="#listagem",
            hx_swap="innerHTML"
        )
    else:
        form = Form(
            Fieldset(
                Input(name="nome", placeholder="Digite o seu Nome", id="nome-input"),
                Button("➕ Adicionar", type="submit", style="margin-left:10px; background:#1A4D2E; color:white; border:none; padding:8px 12px; cursor:pointer;"),
                Button("🔄 Limpar", type="button", hx_get="/limpar/formulario", hx_target="#frm-pessoa", style="background:#FFD700; color:black; border:none; padding:8px 12px; cursor:pointer;"),
                role="group",
                style="display: flex; gap: 10px;"
            ),
            hx_post="/adiciona/pessoa",
            hx_target="#listagem",
            hx_swap="innerHTML"
        )

    return Titled(
        "Formulário de Pessoas",
        Hr(),
        form,
        Div(id="listagem", hx_get=f"/listar/pessoas?page={page}", hx_trigger="load"),  # 🔥 Mantendo a página correta!
        Div(id="mensagem", style="margin-top: 10px; color: green; font-weight: bold;"),
        mensagem_div  # Exibe a mensagem aqui
    )

# Adiciona registro a Tabela
@rt("/adiciona/pessoa")
def adiciona_pessoa(nome: str):
    try:
        if validar_formulario(nome):
            db_pessoa.insert(nome=nome)
            return Div(
                listar_pessoas(page=1),
                caixa_mensagem("sucesso","Pessoa adicionada com sucesso!"),
                limpar_formulario()  # Chamando a função para limpar o formulário
            )

    except ValueError as e:
        return Div(
                listar_pessoas(page=1),
                caixa_mensagem("erro", str(e)),
                limpar_formulario()  # Chamando a função para limpar o formulário
            )

# Editar item da Tabela
@rt("/editar/pessoa/{id}")
def editar_pessoa(id: int, page: int = 1):
    pessoa = db_pessoa.get(id)
    if not pessoa:
        return caixa_mensagem("erro", "Pessoa não encontrada!")

    # Redireciona para a página de edição passando o ID e página atual
    return Redirect(f"/frm/pessoa?edit_id={id}&page={page}")
   

# Salvar Edição
@rt("/salvar/pessoa/{id}")
def salvar_pessoa(id: int, nome: str, page: int = 1):
    try:
        # Valida o formulário antes de salvar as alterações
        validar_formulario(nome)
        
        # Se a validação passar, atualiza o registro no banco de dados
        db_pessoa.update({"id": id, "nome": nome})
        
        # Redireciona para a listagem com uma mensagem de sucesso
        return Redirect(f"/frm/pessoa?page={page}&mensagem=Pessoa atualizada com sucesso!")
    except ValueError as e:
        # Se a validação falhar, redireciona para a página de edição com uma mensagem de erro
        return Redirect(f"/frm/pessoa?edit_id={id}&page={page}&mensagem={str(e)}")

# Excluir item da Tabela
@rt("/excluir/pessoa/{id}")
def excluir_pessoa(id: int, page: int = 1):
    db_pessoa.delete(id)
    
    # Obter o total de registros restantes
    total_pessoas = len(db_pessoa())
    
    # Calcular o total de páginas restantes
    total_paginas = (total_pessoas + NUMERO_REGISTROS_POR_PAGINA - 1) // NUMERO_REGISTROS_POR_PAGINA

    # Se a página atual ficou vazia e não for a primeira, voltar uma página
    if page > total_paginas and page > 1:
        page -= 1

    return Div(
        listar_pessoas(page=page),  # Atualiza a listagem mantendo a página correta
        caixa_mensagem("sucesso", "✖ Pessoa removida com sucesso!")
    )

# Listar itens em Tabela com Paginação (Página Anterior, Próxima, Primeira e Última)
@rt("/listar/pessoas")
def listar_pessoas(page: int = 1):
    total_pessoas = len(db_pessoa())
    total_paginas = (total_pessoas + NUMERO_REGISTROS_POR_PAGINA - 1) // NUMERO_REGISTROS_POR_PAGINA

    inicio = (page - 1) * NUMERO_REGISTROS_POR_PAGINA
    pessoas = db_pessoa()[inicio:inicio + NUMERO_REGISTROS_POR_PAGINA]

    tabela = Table(
        Tr(Th("Id"), Th("Nome"), Th("Ações")),
        *[
            Tr(
                Td(pessoa.id),
                Td(pessoa.nome),
                Td(
                    Button("✏️ Editar",
                        hx_get=f"/editar/pessoa/{pessoa.id}?page={page}",
                        hx_target="#listagem",
                        hx_swap="innerHTML",
                        style="background:#134B70; color:white; border:none; padding:5px 8px; cursor:pointer;"),
                    Button("✖ Excluir", 
                        hx_get=f"/excluir/pessoa/{pessoa.id}?page={page}", 
                        hx_target="#listagem", 
                        hx_swap="innerHTML", 
                        style="margin-left:10px; background:#A0153E; color:white; border:none; padding:5px 8px; cursor:pointer;")
                )
            ) for pessoa in pessoas
        ]
    )

    paginacao = Div(
        A("⏮️", title="Primeira Página", hx_get=f"/listar/pessoas?page=1", hx_target="#listagem", style="font-size: 30px; margin-right: 10px;" if page > 1 else "display:none;"),
        A("◀️", title="Anterior", hx_get=f"/listar/pessoas?page={page-1}", hx_target="#listagem", style="font-size: 30px; margin-right: 10px;" if page > 1 else "display:none;"),
        Label(f" {page} ", style="font-size: 30px; color: blue"),
        A("▶️", title="Próxima", hx_get=f"/listar/pessoas?page={page+1}", hx_target="#listagem", style="font-size: 30px; margin-left: 10px;" if page < total_paginas else "display:none;"),
        A("⏩", title="Última Página", hx_get=f"/listar/pessoas?page={total_paginas}", hx_target="#listagem", style="font-size: 30px; margin-left: 10px;" if page < total_paginas else "display:none;"),
        style="margin-top: 20px; display: flex; gap: 10px;"
    )

    return Div(
        tabela,
        paginacao,
        limpar_formulario()  # 🔥 Sempre limpa o formulário ao mudar de página
    )

def validar_formulario(nome):
    valido = True
    if not nome :
        valido = False
        raise ValueError("O campo 'nome' é obrigatório")
    if re.search(REGEX_VALIDAR["tem_numeros"], nome):
        valido = False
        raise ValueError("O campo 'nome' não pode ter números.")
    if re.search(REGEX_VALIDAR["tem_caracteres_especiais"], nome):
        valido = False
        raise ValueError("O campo 'nome' não pode ter caracteres especiais.")
    return valido
