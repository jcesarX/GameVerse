from werkzeug.utils import secure_filename
import uuid

import config


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in config.ALLOWED_EXTENSIONS
    )


def salvar_capa(arquivo, url=None):

    if (
        arquivo
        and arquivo.filename
        and allowed_file(arquivo.filename)
    ):

        filename = secure_filename(arquivo.filename)

        ext = filename.rsplit(".", 1)[1].lower()

        nome_arquivo = f"{uuid.uuid4()}.{ext}"

        caminho = config.UPLOAD_FOLDER / nome_arquivo

        arquivo.save(caminho)

        return f"uploads/{nome_arquivo}"

    if url:

        url = url.strip()

        if url:
            return url

    return None