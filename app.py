from flask import Flask, render_template, request, redirect, url_for, flash
import json
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import datetime

CLASSIFICACOES = ['Livre', '10 anos', '12 anos', '14 anos', '16 anos', '18 anos']

app = Flask(__name__)
app.secret_key = 'gameverse_secret_key'
     
BASE_DIR = Path(__file__).parent

JOGOS_FILE = BASE_DIR / 'jogos.json'
CATEGORIAS_FILE = BASE_DIR / 'categorias.json'
GENEROS_FILE = BASE_DIR / 'generos.json'

UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def carregar_json(arquivo):

    if not arquivo.exists():
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

        return []

    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip()

            if not conteudo:
                return []

            return json.loads(conteudo)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def salvar_json(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

"""
def salvar_capa(arquivo, url=None):

    if arquivo and arquivo.filename and allowed_file(arquivo.filename):

        filename = secure_filename(arquivo.filename)

        ext = filename.rsplit('.', 1)[1].lower()

        nome_arquivo = f"{uuid.uuid4()}.{ext}"

        caminho = UPLOAD_FOLDER / nome_arquivo

        arquivo.save(caminho)

        return f"uploads/{nome_arquivo}"

    if url:
        return url.strip()

    return None
"""

@app.route('/')
def index():

    jogos = carregar_json(JOGOS_FILE)

    nome = request.args.get('nome', '').lower()
    genero = request.args.get('genero', '').lower()
    categoria = request.args.get('categoria', '').lower()
    classificacao = request.args.get('classificacao', '').lower()
    ano = request.args.get('ano', '')

    jogos_filtrados = []

    for jogo in jogos:

        if nome and nome not in jogo['nome'].lower():
            continue

        if genero and genero not in jogo['genero'].lower():
            continue

        if categoria and categoria not in jogo['categoria'].lower():
            continue

        if classificacao and classificacao not in jogo['classificacao'].lower():
            continue

        if ano and str(jogo['ano']) != ano:
            continue

        jogos_filtrados.append(jogo)

    ano_atual = datetime.now().year 

    return render_template(
        'index.html',
        jogos=jogos_filtrados,
        categorias=carregar_json(CATEGORIAS_FILE),
        generos=carregar_json(GENEROS_FILE),
        classificacoes=CLASSIFICACOES,
        ano_atual=ano_atual
    )


@app.route('/jogo/<string:id>')
def jogo(id):

    jogos = carregar_json(JOGOS_FILE)

    jogo_encontrado = next(
        (j for j in jogos if j['id'] == id),
        None
    )

    if not jogo_encontrado:
        return redirect(url_for('index'))

    return render_template(
        'jogo.html',
        jogo=jogo_encontrado
    )


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    if request.method == 'POST':

        jogos = carregar_json(JOGOS_FILE)

        # arquivo = request.files.get("capa")

        url = request.form.get("capa_url")

        #capa = salvar_capa(arquivo, url)

        capa = url.strip() if url else None

        ano  = int(request.form['ano'])
        
        if ano < 1970 or ano > datetime.now().year:
            flash(
                f"O ano deve estar entre 1970 e {datetime.now().year}.", "error")
            return redirect(url_for('cadastrar'))
        
        novo_jogo = {
            "id": str(uuid.uuid4()),
            "nome": request.form['nome'],
            "descricao": request.form['descricao'],
            "genero": request.form['genero'],
            "categoria": request.form['categoria'],
            "classificacao": request.form['classificacao'],
            "ano": ano,
            "capa": capa
        }

        jogos.append(novo_jogo)

        salvar_json(JOGOS_FILE, jogos)

        return redirect(url_for('index'))

    return render_template(
        'cadastrar.html',
        categorias=carregar_json(CATEGORIAS_FILE),
        generos=carregar_json(GENEROS_FILE),
        classificacoes=CLASSIFICACOES
    )


@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar(id):

    jogos = carregar_json(JOGOS_FILE)

    jogo = next(
        (j for j in jogos if j['id'] == id),
        None
    )

    if not jogo:
        return redirect(url_for('index'))

    if request.method == 'POST':

        # arquivo = request.files.get("capa")

        url = request.form.get("capa_url")

        # nova_capa = salvar_capa(arquivo, url)
        nova_capa = url.strip() if url else None

        if nova_capa:

            if jogo.get("capa") and not jogo["capa"].startswith("http"):

                capa_antiga = BASE_DIR / "static" / jogo["capa"]

                if capa_antiga.exists():
                    capa_antiga.unlink()

            jogo['capa'] = nova_capa

        jogo['nome'] = request.form['nome']
        jogo['descricao'] = request.form['descricao']
        jogo['genero'] = request.form['genero']
        jogo['categoria'] = request.form['categoria']
        jogo['classificacao'] = request.form['classificacao']
        ano = int(request.form['ano'])

        if ano < 1970 or ano > datetime.now().year:
            flash(
                f"O ano deve estar entre 1970 e {datetime.now().year}.", "error")
            return redirect(url_for('editar', id=id))

        jogo['ano'] = ano

        salvar_json(JOGOS_FILE, jogos)

        return redirect(url_for('jogo', id=id))

    ano_atual = datetime.now().year
    return render_template(
        'editar.html',
        jogo=jogo,
        categorias=carregar_json(CATEGORIAS_FILE),
        generos=carregar_json(GENEROS_FILE),
        classificacoes=CLASSIFICACOES,
        ano_atual=ano_atual
    )


@app.route('/deletar/<string:id>', methods=['POST'])
def deletar(id):

    jogos = carregar_json(JOGOS_FILE)

    jogo = next(
        (j for j in jogos if j['id'] == id),
        None
    )

    if jogo:

        """if jogo.get("capa") and not jogo["capa"].startswith("http"):

            capa_path = BASE_DIR / "static" / jogo["capa"]

            if capa_path.exists():
                capa_path.unlink()"""

        jogos = [j for j in jogos if j['id'] != id]

        salvar_json(JOGOS_FILE, jogos)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)