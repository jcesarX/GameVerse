import uuid
import psycopg2
import psycopg2.extras
from psycopg2 import sql

HOST = "localhost"
PORT = "5432"
DB_NAME = "gameverse"
USER = "postgres"
PASSWORD = "postgres"

# CONEXÃO

def criar_banco():

    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname="postgres",
        user=USER,
        password=PASSWORD
    )

    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_NAME,)
    )

    if cur.fetchone() is None:

        cur.execute(
            sql.SQL(
                "CREATE DATABASE {}"
            ).format(
                sql.Identifier(DB_NAME)
            )
        )

        print("Banco criado com sucesso!")

    else:

        print("Banco já existe.")

    cur.close()
    conn.close()


def get_conn():

    return psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD
    )


# CRIAÇÃO DAS TABELAS

def criar_tabelas():

    conn = get_conn()

    cur = conn.cursor()

    # GÊNERO

    cur.execute("""

        CREATE TABLE IF NOT EXISTS genero(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(50)
            UNIQUE NOT NULL

        );

    """)

    # CATEGORIA

    cur.execute("""

        CREATE TABLE IF NOT EXISTS categoria(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(50)
            UNIQUE NOT NULL

        );

    """)

    # JOGO

    cur.execute("""

        CREATE TABLE IF NOT EXISTS jogo(
            id UUID PRIMARY KEY,
            nome VARCHAR(100)
            NOT NULL,
            descricao TEXT
            NOT NULL,
            classificacao VARCHAR(10)
            NOT NULL,
            ano INTEGER
            NOT NULL,
            capa TEXT,
            genero_id INTEGER
            NOT NULL,
            categoria_id INTEGER
            NOT NULL,
            FOREIGN KEY(genero_id)
                REFERENCES genero(id),
            FOREIGN KEY(categoria_id)
                REFERENCES categoria(id)
        );

    """)

    # INSERÇÃO DE DADOS INICIAIS

    cur.executemany(

        """
        INSERT INTO genero(nome)
        VALUES(%s)

        ON CONFLICT(nome)
        DO NOTHING

        """,

        [
            ("Ação",),
            ("Aventura",),
            ("RPG",),
            ("Estratégia",),
            ("Corrida",),
            ("Esporte",),
            ("FPS",),
            ("Luta",),
            ("Terror",),
            ("Simulação",),
            ("Puzzle",)
        ]
    )

    cur.executemany(

        """

        INSERT INTO categoria(nome)
        VALUES(%s)

        ON CONFLICT(nome)
        DO NOTHING

        """,

        [
            ("Singleplayer",),
            ("Multiplayer",),
            ("Cooperativo",),
            ("Online",),
            ("Competitivo",)
        ]

    )

    conn.commit()

    cur.close()

    conn.close()


def listar_generos():

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cur.execute("""

        SELECT *

        FROM genero

        ORDER BY nome

    """)

    generos = cur.fetchall()

    cur.close()
    conn.close()

    return generos



def listar_categorias():

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cur.execute("""

        SELECT *
        FROM categoria
        ORDER BY nome

    """)

    categorias = cur.fetchall()

    cur.close()
    conn.close()

    return categorias



def listar_jogos():

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cur.execute("""

        SELECT
            j.id,
            j.nome,
            j.descricao,
            j.classificacao,
            j.ano,
            j.capa,
            g.nome AS genero,
            c.nome AS categoria,
            j.genero_id,
            j.categoria_id
                
        FROM jogo j
        INNER JOIN genero g
            ON j.genero_id = g.id
        INNER JOIN categoria c
            ON j.categoria_id = c.id
        ORDER BY j.nome
    """)

    jogos = cur.fetchall()

    cur.close()
    conn.close()

    return jogos



def buscar_jogo(id):

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cur.execute("""

        SELECT
            j.id,
            j.nome,
            j.descricao,
            j.classificacao,
            j.ano,
            j.capa,
            g.nome AS genero,
            c.nome AS categoria,
            j.genero_id,
            j.categoria_id

        FROM jogo j
        INNER JOIN genero g
            ON j.genero_id = g.id
        INNER JOIN categoria c
            ON j.categoria_id = c.id
        WHERE j.id = %s

    """,

    (id,))

    jogo = cur.fetchone()

    cur.close()

    conn.close()

    return jogo


#CRUD

def adicionar_jogo(jogo):

    conn = get_conn()

    cur = conn.cursor()

    cur.execute("""

        INSERT INTO jogo(
            id,
            nome,
            descricao,
            classificacao,
            ano,
            capa,
            genero_id,
            categoria_id
        )

        VALUES(

            %s,%s,%s,%s,%s,%s,%s,%s

        )

    """,

    (
        jogo["id"],
        jogo["nome"],
        jogo["descricao"],
        jogo["classificacao"],
        jogo["ano"],
        jogo["capa"],
        jogo["genero_id"],
        jogo["categoria_id"]
    ))

    conn.commit()

    cur.close()

    conn.close()


def criar_jogo(
    nome,
    descricao,
    genero_id,
    categoria_id,
    classificacao,
    ano,
    capa
):

    return {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "descricao": descricao,
        "genero_id": int(genero_id),
        "categoria_id": int(categoria_id),
        "classificacao": classificacao,
        "ano": ano,
        "capa": capa
    }



def editar_jogo(
    jogo,
    nome,
    descricao,
    genero_id,
    categoria_id,
    classificacao,
    ano,
    capa

):

    conn = get_conn()

    cur = conn.cursor()

    if capa is None:

        capa = jogo["capa"]

    cur.execute("""

        UPDATE jogo

        SET
            nome=%s,
            descricao=%s,
            classificacao=%s,
            ano=%s,
            capa=%s,
            genero_id=%s,
            categoria_id=%s

        WHERE id=%s

    """,

    (
        nome,
        descricao,
        classificacao,
        ano,
        capa,
        int(genero_id),
        int(categoria_id),
        jogo["id"]
    ))

    conn.commit()

    cur.close()

    conn.close()



def excluir_jogo(id):

    conn = get_conn()

    cur = conn.cursor()

    cur.execute(

        """

        DELETE
        FROM jogo
        WHERE id=%s

        """,

        (id,)

    )

    conn.commit()

    cur.close()

    conn.close()



#Filtros e paginação

def filtrar_jogos(
    nome="",
    genero="",
    categoria="",
    classificacao="",
    ano=""
):

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    sql = """

        SELECT
            j.id,
            j.nome,
            j.descricao,
            j.classificacao,
            j.ano,
            j.capa,
            g.nome AS genero,
            c.nome AS categoria,
            j.genero_id,
            j.categoria_id

        FROM jogo j

        INNER JOIN genero g
            ON j.genero_id = g.id
        INNER JOIN categoria c
            ON j.categoria_id = c.id
        WHERE TRUE

    """

    parametros = []

    if nome:
        sql += " AND LOWER(j.nome) LIKE %s"
        parametros.append(f"%{nome.lower()}%")

    if genero:
        sql += " AND LOWER(g.nome) LIKE %s"
        parametros.append(f"%{genero.lower()}%")

    if categoria:
        sql += " AND LOWER(c.nome) LIKE %s"
        parametros.append(f"%{categoria.lower()}%")

    if classificacao:
        sql += " AND LOWER(j.classificacao) LIKE %s"
        parametros.append(f"%{classificacao.lower()}%")

    if ano:

        sql += " AND j.ano = %s"

        parametros.append(int(ano))

    sql += " ORDER BY j.nome"

    cur.execute(sql, parametros)

    jogos = cur.fetchall()

    cur.close()
    conn.close()

    return jogos


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



criar_banco()
criar_tabelas()