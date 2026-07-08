from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Arquivos de dados
JOGOS_FILE = BASE_DIR / "jogos.json"
GENEROS_FILE = BASE_DIR / "generos.json"
CATEGORIAS_FILE = BASE_DIR / "categorias.json"

# Upload de imagens
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}

# Configurações da aplicação
SECRET_KEY = "gameverse_secret_key"

# Classificações indicativas
CLASSIFICACOES = [
    "Livre",
    "10 anos",
    "12 anos",
    "14 anos",
    "16 anos",
    "18 anos"
]

# Paginação
JOGOS_POR_PAGINA_PADRAO = 8
OPCOES_POR_PAGINA = {2, 4, 6, 8}