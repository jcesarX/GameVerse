from flask import Flask, render_template, request, redirect, url_for, flash
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


@app.route("/")
def index():

    nome = request.args.get("nome", "").lower()
    genero = request.args.get("genero", "").lower()
    categoria = request.args.get("categoria", "").lower()
    classificacao = request.args.get("classificacao", "").lower()
    ano = request.args.get("ano", "")

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

    return render_template(
        "index.html",
        jogos=resultado["jogos"],
        categorias=model.listar_categorias(),
        generos=model.listar_generos(),
        classificacoes=config.CLASSIFICACOES,
        ano_atual=datetime.now().year,
        total_jogos=resultado["total_jogos"],
        pagina=resultado["pagina"],
        total_paginas=resultado["total_paginas"]
    )


@app.route("/jogo/<string:id>")
def jogo(id):

    jogo = model.buscar_jogo(id)

    if not jogo:
        return redirect(url_for("index"))

    return render_template(
        "jogo.html",
        jogo=jogo
    )


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        arquivo = request.files.get("capa")
        url = request.form.get("capa_url")

        # Valida a URL, se fornecida
        if url and url.strip():
            if not validar_url_imagem(url):
                flash("A URL fornecida não é uma imagem válida.", "error")
                return render_template(
                    "cadastrar.html",
                    categorias=model.listar_categorias(),
                    generos=model.listar_generos(),
                    classificacoes=config.CLASSIFICACOES,
                    dados=request.form
                )

        # Obtém e valida o ano
        try:
            ano = int(request.form["ano"])
        except ValueError:
            flash("Ano inválido. Digite um número.", "error")
            return render_template(
                "cadastrar.html",
                categorias=model.listar_categorias(),
                generos=model.listar_generos(),
                classificacoes=config.CLASSIFICACOES,
                dados=request.form
            )

        if ano < 1970 or ano > datetime.now().year:
            flash(f"O ano deve estar entre 1970 e {datetime.now().year}.", "error")
            return render_template(
                "cadastrar.html",
                categorias=model.listar_categorias(),
                generos=model.listar_generos(),
                classificacoes=config.CLASSIFICACOES,
                dados=request.form
            )

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
        return redirect(url_for("index"))

    return render_template(
        "cadastrar.html",
        categorias=model.listar_categorias(),
        generos=model.listar_generos(),
        classificacoes=config.CLASSIFICACOES,
        dados={}
    )


@app.route("/editar/<string:id>", methods=["GET", "POST"])
def editar(id):
    jogo = model.buscar_jogo(id)
    if not jogo:
        return redirect(url_for("index"))

    if request.method == "POST":
        arquivo = request.files.get("capa")
        url = request.form.get("capa_url")

        # Valida a URL, se fornecida
        if url and url.strip():
            if not validar_url_imagem(url):
                flash("A URL fornecida não é uma imagem válida.", "error")
                return render_template(
                    "editar.html",
                    jogo=jogo,
                    categorias=model.listar_categorias(),
                    generos=model.listar_generos(),
                    classificacoes=config.CLASSIFICACOES,
                    ano_atual=datetime.now().year,
                    dados=request.form
                )

        # Obtém e valida o ano
        try:
            ano = int(request.form["ano"])
        except ValueError:
            flash("Ano inválido. Digite um número.", "error")
            return render_template(
                "editar.html",
                jogo=jogo,
                categorias=model.listar_categorias(),
                generos=model.listar_generos(),
                classificacoes=config.CLASSIFICACOES,
                ano_atual=datetime.now().year,
                dados=request.form
            )

        if ano < 1970 or ano > datetime.now().year:
            flash(f"O ano deve estar entre 1970 e {datetime.now().year}.", "error")
            return render_template(
                "editar.html",
                jogo=jogo,
                categorias=model.listar_categorias(),
                generos=model.listar_generos(),
                classificacoes=config.CLASSIFICACOES,
                ano_atual=datetime.now().year,
                dados=request.form
            )

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

        return redirect(url_for("jogo", id=id))

    return render_template(
        "editar.html",
        jogo=jogo,
        categorias=model.listar_categorias(),
        generos=model.listar_generos(),
        classificacoes=config.CLASSIFICACOES,
        dados={},
        ano_atual=datetime.now().year
    )


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

