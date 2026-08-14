from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import config
import model
from utils import salvar_capa, validar_url_imagem

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def obter_jogos_por_pagina():
    valor = request.cookies.get("jogos_por_pagina")

    try:
        valor = int(valor)
    except (TypeError, ValueError):
        return config.JOGOS_POR_PAGINA_PADRAO

    if valor in config.OPCOES_POR_PAGINA:
        return valor

    return config.JOGOS_POR_PAGINA_PADRAO


def eh_ajax():
    """Identifica se a requisição veio do JS (fetch), para retornar
    apenas o fragmento HTML/JSON necessário, sem a página inteira."""
    return request.headers.get("X-Requested-With") == "fetch"


@app.route("/")
def index():

    nome = request.args.get("nome", "").lower()
    genero = request.args.get("genero", "").lower()
    categoria = request.args.get("categoria", "").lower()
    classificacao = request.args.get("classificacao", "").lower()
    ano = request.args.get("ano", "")

    if ano:
        try:
            int(ano)
        except ValueError:
            flash("Ano inválido. O filtro de ano foi ignorado.", "error")
            ano = ""

    jogos_filtrados = model.filtrar_jogos(
        nome,
        genero,
        categoria,
        classificacao,
        ano
    )

    jogos_por_pagina = obter_jogos_por_pagina()

    try:
        pagina = int(request.args.get("pagina", 1))
    except ValueError:
        pagina = 1

    resultado = model.paginar_jogos(
        jogos_filtrados,
        pagina,
        jogos_por_pagina
    )

    contexto = dict(
        jogos=resultado["jogos"],
        categorias=model.listar_categorias(),
        generos=model.listar_generos(),
        classificacoes=config.CLASSIFICACOES,
        ano_atual=datetime.now().year,
        total_jogos=resultado["total_jogos"],
        pagina=resultado["pagina"],
        total_paginas=resultado["total_paginas"]
    )

    if eh_ajax():
        return render_template("_resultados.html", **contexto)

    return render_template("index.html", **contexto)


@app.route("/jogo/<string:id>")
def jogo(id):

    jogo = model.buscar_jogo(id)

    if not jogo:
        return redirect(url_for("index"))

    return render_template(
        "jogo.html",
        jogo=jogo,
        ano_atual=datetime.now().year
    )


def renderizar_formulario(modo, jogo, dados, status=200):
    """Renderiza o formulário de cadastro/edição.
    Se a requisição vier do JS (painel), devolve só o fragmento HTML do
    formulário. Caso contrário, devolve a página completa (fallback)."""
    contexto = dict(
        modo=modo,
        jogo=jogo,
        dados=dados,
        categorias=model.listar_categorias(),
        generos=model.listar_generos(),
        classificacoes=config.CLASSIFICACOES,
        ano_atual=datetime.now().year
    )

    if eh_ajax():
        return render_template("_jogo_form.html", **contexto), status

    pagina = "cadastrar.html" if modo == "cadastrar" else "editar.html"
    return render_template(pagina, **contexto), status


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        arquivo = request.files.get("capa")
        url = request.form.get("capa_url")

        # Valida a URL, se fornecida
        if url and url.strip():
            if not validar_url_imagem(url):
                flash("A URL fornecida não é uma imagem válida.", "error")
                return renderizar_formulario("cadastrar", None, request.form, status=400)

        # Obtém e valida o ano
        try:
            ano = int(request.form["ano"])
        except ValueError:
            flash("Ano inválido. Digite um número.", "error")
            return renderizar_formulario("cadastrar", None, request.form, status=400)

        if ano < 1970 or ano > datetime.now().year:
            flash(f"O ano deve estar entre 1970 e {datetime.now().year}.", "error")
            return renderizar_formulario("cadastrar", None, request.form, status=400)

        url_capa = salvar_capa(arquivo, url)

        novo_jogo = model.criar_jogo(
            request.form["nome"],
            request.form["descricao"],
            request.form["genero_id"],
            request.form["categoria_id"],
            request.form["classificacao"],
            ano,
            url_capa
        )

        model.adicionar_jogo(novo_jogo)

        if eh_ajax():
            return jsonify(ok=True), 201

        return redirect(url_for("index"))

    return renderizar_formulario("cadastrar", None, {})


@app.route("/editar/<string:id>", methods=["GET", "POST"])
def editar(id):
    jogo = model.buscar_jogo(id)
    if not jogo:
        if eh_ajax():
            return jsonify(erro="Jogo não encontrado."), 404
        return redirect(url_for("index"))

    if request.method == "POST":
        arquivo = request.files.get("capa")
        url = request.form.get("capa_url")

        # Valida a URL, se fornecida
        if url and url.strip():
            if not validar_url_imagem(url):
                flash("A URL fornecida não é uma imagem válida.", "error")
                return renderizar_formulario("editar", jogo, request.form, status=400)

        # Obtém e valida o ano
        try:
            ano = int(request.form["ano"])
        except ValueError:
            flash("Ano inválido. Digite um número.", "error")
            return renderizar_formulario("editar", jogo, request.form, status=400)

        if ano < 1970 or ano > datetime.now().year:
            flash(f"O ano deve estar entre 1970 e {datetime.now().year}.", "error")
            return renderizar_formulario("editar", jogo, request.form, status=400)

        nova_url_capa = salvar_capa(arquivo, url)

        if nova_url_capa is not None:
            if jogo.get("url_capa") and not jogo["url_capa"].startswith("http"):
                capa_antiga = config.BASE_DIR / "static" / jogo["url_capa"]
                if capa_antiga.exists():
                    capa_antiga.unlink()

        model.editar_jogo(
            jogo,
            request.form["nome"],
            request.form["descricao"],
            request.form["genero_id"],
            request.form["categoria_id"],
            request.form["classificacao"],
            ano,
            nova_url_capa
        )

        if eh_ajax():
            return jsonify(ok=True), 200

        return redirect(url_for("jogo", id=id))

    return renderizar_formulario("editar", jogo, {})


@app.route("/deletar/<string:id>", methods=["POST"])
def deletar(id):

    jogo = model.buscar_jogo(id)

    if jogo:

        if jogo.get("url_capa") and not jogo["url_capa"].startswith("http"):

            capa = config.BASE_DIR / "static" / jogo["url_capa"]

            if capa.exists():
                capa.unlink()

        model.excluir_jogo(id)

    return redirect(url_for("index"))


model.criar_banco()
model.criar_tabelas()

if __name__ == "__main__":
    app.run(debug=True)
