GameVerse

Sistema web para cadastro e gerenciamento de jogos, desenvolvido como projeto acadêmico para aplicação prática de conceitos de desenvolvimento web, Python, Flask e banco de dados.

Sobre o projeto

O GameVerse permite organizar um catálogo de jogos através de uma aplicação web, possibilitando cadastrar, editar, excluir, pesquisar e filtrar registros.

O projeto foi desenvolvido buscando separar responsabilidades entre as diferentes partes da aplicação, facilitando sua organização e manutenção.

Funcionalidades

- Cadastro de jogos
- Edição de jogos
- Exclusão de jogos
- Pesquisa por nome
- Filtros por categoria e gênero
- Paginação
- Upload de capas
- Validação de imagens
- Interface responsiva
- Persistência de dados em banco de dados

Tecnologias

- Python
- Flask
- PostgreSQL
- SQL
- HTML5
- CSS3
- JavaScript
- Jinja2
- Git/GitHub

Estrutura

GameVerse/
├── static/
│   ├── css/
│   ├── js/
│   ├── imagens/
│   └── uploads/
├── templates/
├── app.py
├── config.py
├── model.py
├── utils.py
├── requirements.txt
└── README.md

Principais conceitos aplicados

- Desenvolvimento web com Flask
- Arquitetura e organização modular
- Operações CRUD
- Integração com banco de dados relacional
- SQL
- Relacionamento entre entidades
- Validação de dados
- Upload e gerenciamento de arquivos
- Paginação e filtros
- Controle de versão com Git

Execução

Clone o repositório:

git clone https://github.com/jcesarX/GameVerse.git
cd GameVerse

Crie um ambiente virtual:

python -m venv venv

Ative o ambiente virtual e instale as dependências:

pip install -r requirements.txt

Configure o banco de dados conforme as configurações do projeto e execute:

python app.py

Objetivo

Projeto desenvolvido para fins acadêmicos e de aprendizado, com foco na prática de desenvolvimento de aplicações web utilizando Python e Flask.

Autor

Júlio César Xavier Marinho

"GitHub" (https://github.com/jcesarX)├── generos.json
├── requirements.txt
└── README.md
```

---

# Como Executar

## 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/GameVerse.git
```

## 2. Entre na pasta do projeto

```bash
cd GameVerse
```

## 3. Crie um ambiente virtual

Windows

```bash
python -m venv venv
```

Linux

```bash
python3 -m venv venv
```

---

## 4. Ative o ambiente virtual

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

---

## 5. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 6. Execute o projeto

```bash
python app.py
```

A aplicação ficará disponível em:

```
http://127.0.0.1:5000
```

---

# Como Utilizar

1. Acesse a página inicial.
2. Visualize os jogos cadastrados.
3. Utilize a barra de pesquisa para encontrar jogos.
4. Filtre os resultados por categoria ou gênero.
5. Clique em **Cadastrar** para adicionar um novo jogo.
6. Utilize **Editar** para alterar informações existentes.
7. Utilize **Excluir** para remover um jogo do catálogo.

---

# Principais Recursos

* Interface simples e intuitiva.
* Upload de capas para os jogos.
* Validação de arquivos de imagem.
* Organização dos dados em arquivos JSON.
* Paginação para facilitar a navegação.
* Layout responsivo para diferentes tamanhos de tela.

---

# Organização do Código

O projeto foi dividido em módulos para facilitar a manutenção.

| Arquivo      | Responsabilidade                                        |
| ------------ | ------------------------------------------------------- |
| `app.py`     | Rotas da aplicação e controle das requisições           |
| `model.py`   | Manipulação dos dados dos jogos                         |
| `utils.py`   | Funções auxiliares, como upload e validações            |
| `config.py`  | Configurações gerais da aplicação                       |
| `templates/` | Páginas HTML utilizando Jinja2                          |
| `static/`    | Arquivos estáticos (CSS, JavaScript, imagens e uploads) |

---

# Possíveis Melhorias Futuras

* Banco de dados (SQLite ou PostgreSQL)
* Sistema de autenticação de usuários
* Favoritar jogos
* Avaliações e comentários
* API REST
* Dashboard administrativo
* Upload de múltiplas imagens
* Melhorias de acessibilidade
* Testes automatizados

---

# Autor

Desenvolvido como projeto acadêmico para estudo de desenvolvimento web utilizando Python e Flask.

---

# Licença

Este projeto possui finalidade exclusivamente educacional.
