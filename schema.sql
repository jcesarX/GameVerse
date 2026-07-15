-- ============================================
-- SCHEMA.SQL - GameVerse
-- Estrutura das tabelas + dados iniciais
-- ============================================

-- GÊNERO

CREATE TABLE IF NOT EXISTS genero(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

-- CATEGORIA

CREATE TABLE IF NOT EXISTS categoria(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

-- JOGO

CREATE TABLE IF NOT EXISTS jogo(
    id UUID PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    classificacao VARCHAR(10) NOT NULL,
    ano INTEGER NOT NULL,
    url_capa TEXT,
    genero_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY(genero_id) REFERENCES genero(id),
    FOREIGN KEY(categoria_id) REFERENCES categoria(id)
);

-- ============================================
-- DADOS INICIAIS - GÊNERO
-- ============================================

INSERT INTO genero(nome)
VALUES
    ('Ação'),
    ('Aventura'),
    ('RPG'),
    ('Estratégia'),
    ('Corrida'),
    ('Esporte'),
    ('FPS'),
    ('Luta'),
    ('Terror'),
    ('Simulação'),
    ('Puzzle')
ON CONFLICT(nome) DO NOTHING;

-- ============================================
-- DADOS INICIAIS - CATEGORIA
-- ============================================

INSERT INTO categoria(nome)
VALUES
    ('Singleplayer'),
    ('Multiplayer'),
    ('Cooperativo'),
    ('Online'),
    ('Competitivo')
ON CONFLICT(nome) DO NOTHING;

-- ============================================
-- DADOS INICIAIS - JOGOS
-- ============================================

INSERT INTO jogo(id, nome, descricao, classificacao, ano, url_capa, genero_id, categoria_id)
VALUES
    (
        'bbfbf2c7-4c89-40c8-a543-8fd6f9f70bc7',
        'GTA San Andreas',
        'Jogo de ação e mundo aberto com missões, gangues, exploração livre e grande variedade de veículos, armas e atividades em um mapa gigante inspirado na Califórnia dos anos 90.',
        '18 anos',
        2004,
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRu-syUB2MzEyxMcKbzRPJbeySTnPr8CaAG0HhblVLsdY75XW0tnZ2biw6njCTZujBzJY4GbhIFTRCwIMDBaYRuajGW2-CSn9uEoBKfI7CT-g&s=10',
        (SELECT id FROM genero WHERE nome = 'Ação'),
        (SELECT id FROM categoria WHERE nome = 'Singleplayer')
    ),
    (
        '4893cd73-d4ed-4ab1-bf60-eb6aae8baac3',
        'Ben 10: Protector of Earth',
        'Jogo de ação e aventura baseado no desenho Ben 10, onde o jogador se transforma em diferentes alienígenas para enfrentar inimigos e cumprir missões pelo mundo.',
        '10 anos',
        2007,
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVXNnwdLn10mTQ6dmioOkNE92JUhm73ltcXFtNNTXl4LFgQgWjVwu3mQoGD1UHHnR48v1KHmc-7J2-Gi71HMF7TzRu6oCico-TFAuWHrVw&s=10',
        (SELECT id FROM genero WHERE nome = 'Aventura'),
        (SELECT id FROM categoria WHERE nome = 'Singleplayer')
    ),
    (
        '5aa91bb7-893d-4e61-bec3-f4cc523dda05',
        'Call of Duty: Black Ops 6',
        'FPS militar com campanha intensa e modos multiplayer online competitivos, trazendo combates rápidos, arsenal variado de armas e cenários de guerra realistas.',
        '18 anos',
        2024,
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVA16k0IOQLOCNS4uL34vWUtvGYY2fWiADGMN-EkogDA&s=10',
        (SELECT id FROM genero WHERE nome = 'FPS'),
        (SELECT id FROM categoria WHERE nome = 'Online')
    )
ON CONFLICT(id) DO NOTHING;
