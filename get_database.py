import json
import requests
import tarfile
import shutil
import os.path

def baixar_e_descompactar(url):
    """
    Baixa um arquivo da URL especificada e descompacta-o na mesma pasta do script.

    Args:
        url (str): URL do arquivo a ser baixado.
    """

    # Obtendo o caminho absoluto da pasta do script
    caminho_atual = os.path.dirname(os.path.abspath(__file__))

    # Baixando o arquivo
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Verificando a extensão do arquivo
    if not response.headers['Content-Type'].startswith('application/x-gzip'):
        raise ValueError("O arquivo não é do tipo .ar.gz")

    # Salvando o arquivo temporariamente
    with open('arquivo.ar.gz', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    # Descompactando o arquivo na pasta atual
    with tarfile.open('arquivo.ar.gz', 'r:gz') as tar:
        tar.extractall(path=caminho_atual)


def txt2json(input, output):
    dataset = []

    with open(input, "r", encoding="utf-8") as file:
        for line in file:

            fields = line.strip().split('\t')

            if len(fields) == 7:
                wikpedia_id, freebase_id, titulo, autor, data_publi, genero, sinopse = fields

                book = {
                    "wikipedia_ID": wikpedia_id,
                    "freebase_ID": freebase_id,
                    "titulo": titulo,
                    "autor": autor,
                    "data de publicacao": data_publi,
                    "genero": genero,
                    "sinopse": sinopse
                }

                dataset.append(book)

    with open(output, "w", encoding="utf-8") as json_file:
        json.dump(dataset, json_file, ensure_ascii=False, indent=4)

def get_data():
    url = "https://www.cs.cmu.edu/~dbamman/data/booksummaries.tar.gz"
    if not os.path.exists("books.json"):
        baixar_e_descompactar(url)
        txt2json("booksummaries/booksummaries.txt", "books.json")

    with open("books.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    print("Successfully loaded data set")
    return books