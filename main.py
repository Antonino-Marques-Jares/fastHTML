from fasthtml.common import fast_app, serve
from SGBD import get_db
from frm_pessoa import frm_pessoa, adiciona_pessoa, editar_pessoa, salvar_pessoa, excluir_pessoa, listar_pessoas

# Configuração do FastHTML
app, rt = fast_app()
db = get_db()

# Formulario Pessoa
rt("/frm/pessoa")(frm_pessoa)
rt("/adiciona/pessoa")(adiciona_pessoa)
rt("/editar/pessoa/{id}")(editar_pessoa)
rt("/salvar/pessoa/{id}")(salvar_pessoa)
rt("/excluir/pessoa/{id}")(excluir_pessoa)
rt("/listar/pessoas")(listar_pessoas)

#Outros formularios adicionar aqui !

# Servir a aplicação
serve()
