# GameVerse

Sistema web desenvolvido em **Python** utilizando **Flask** para o cadastro e gerenciamento de jogos. O projeto permite adicionar, editar, excluir e visualizar jogos de forma simples e organizada, além de realizar pesquisas e filtrar os resultados.

---

# Objetivo

O GameVerse foi desenvolvido com o objetivo de aplicar conceitos de desenvolvimento web, programação em Python e organização de projetos utilizando o padrão MVC, proporcionando uma aplicação funcional para gerenciamento de um catálogo de jogos.

---

# Funcionalidades

* Cadastro de jogos
* Edição de informações dos jogos
* Exclusão de jogos
* Upload de imagem de capa
* Validação de imagens enviadas
* Pesquisa de jogos por nome
* Filtro por categoria e gênero
* Paginação da lista de jogos
* Interface responsiva
* Armazenamento dos dados em arquivos JSON

---

# Tecnologias Utilizadas

* Python 3
* Flask
* HTML5
* CSS3
* JavaScript
* Jinja2
* JSON

---

# Estrutura do Projeto

```text
GameVerse/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── imagens/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── cadastrar.html
│   ├── editar.html
│   └── ...
│
├── app.py
├── model.py
├── utils.py
├── config.py
├── jogos.json
├── categorias.json
├── generos.json
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
