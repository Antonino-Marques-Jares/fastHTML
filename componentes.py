from fasthtml.common import Div, Script

def caixa_mensagem(tipo: str, texto: str):
    cores = {
        "sucesso": "background-color: #28a745; color: white;",
        "erro": "background-color: #dc3545; color: white;",
        "info": "background-color: #007bff; color: white;"
    }
    
    estilo = cores.get(tipo, "background-color: #007bff; color: white;")

    return Div(
        Div(
            texto,
            id="caixa-mensagem",
            style=f"position: absolute; top: 20px; right: 20px; padding: 10px 20px; border-radius: 5px; {estilo}; "
                  f"box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 1000; width: auto;"
        ),
        Script("""
            setTimeout(function() {
                var msgElement = document.getElementById('caixa-mensagem');
                if (msgElement) {
                    msgElement.style.display = 'none';
                }
            }, 5000);
        """)
    )
