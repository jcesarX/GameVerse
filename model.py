import json
import uuid

from config import (
    JOGOS_FILE,
    GENEROS_FILE,
    CATEGORIAS_FILE
)


# ==========================
# Leitura e escrita dos JSON
# ==========================

def carregar_json(arquivo):

    if not arquivo.exists():

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

        return []

    try:

        with open(arquivo, "r", encoding="utf-8") as f:

            conteudo = f.read().strip()

            if not conteudo:
                return []

            return json.loads(conteudo)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def salvar_json(arquivo, dados):

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# ==========================
# Listagens
# ==========================

def listar_jogos():
    return carregar_json(JOGOS_FILE)


def listar_generos():
    return carregar_json(GENEROS_FILE)


def listar_categorias():
    return carregar_json(CATEGORIAS_FILE)


def salvar_jogos(jogos):
    salvar_json(JOGOS_FILE, jogos)


# ==========================
# Busca
# ==========================

def buscar_jogo(id):

    jogos = listar_jogos()

    return next(
        (j for j in jogos if j["id"] == id),
        None
    )


# ==========================
# CRUD
# ==========================

def criar_jogo(
    nome,
    descricao,
    genero,
    categoria,
    classificacao,
    ano,
    capa
):

    return {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "descricao": descricao,
        "genero": genero,
        "categoria": categoria,
        "classificacao": classificacao,
        "ano": ano,
        "capa": capa
    }


def adicionar_jogo(jogo):

    jogos = listar_jogos()

    jogos.append(jogo)

    salvar_jogos(jogos)


def atualizar_jogo(jogo_atualizado):

    jogos = listar_jogos()

    for i, jogo in enumerate(jogos):

        if jogo["id"] == jogo_atualizado["id"]:

            jogos[i] = jogo_atualizado
            break

    salvar_jogos(jogos)


def editar_jogo(
    jogo,
    nome,
    descricao,
    genero,
    categoria,
    classificacao,
    ano,
    capa
):

    jogo["nome"] = nome
    jogo["descricao"] = descricao
    jogo["genero"] = genero
    jogo["categoria"] = categoria
    jogo["classificacao"] = classificacao
    jogo["ano"] = ano

    if capa is not None:
        jogo["capa"] = capa

    atualizar_jogo(jogo)


def excluir_jogo(id):

    jogos = listar_jogos()

    jogos = [j for j in jogos if j["id"] != id]

    salvar_jogos(jogos)


# ==========================
# Filtros
# ==========================

def filtrar_jogos(
    nome="",
    genero="",
    categoria="",
    classificacao="",
    ano=""
):

    jogos = listar_jogos()

    jogos_filtrados = []

    for jogo in jogos:

        if nome and nome not in jogo["nome"].lower():
            continue

        if genero and genero not in jogo["genero"].lower():
            continue

        if categoria and categoria not in jogo["categoria"].lower():
            continue

        if classificacao and classificacao not in jogo["classificacao"].lower():
            continue

        if ano and str(jogo["ano"]) != str(ano):
            continue

        jogos_filtrados.append(jogo)

    return jogos_filtrados


# ==========================
# Paginação
# ==========================

def paginar_jogos(jogos, pagina, por_pagina):

    total_jogos = len(jogos)

    total_paginas = max(
        1,
        (total_jogos + por_pagina - 1) // por_pagina
    )

    pagina = max(
        1,
        min(pagina, total_paginas)
    )

    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina

    jogos_paginados = jogos[inicio:fim]

    return {
        "jogos": jogos_paginados,
        "pagina": pagina,
        "total_paginas": total_paginas,
        "total_jogos": total_jogos
    }