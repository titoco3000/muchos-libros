import json
import requests
import tarfile
import shutil
import os.path

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
    if not os.path.exists("books.json"):
        txt2json("booksummaries.txt", "books.json")

    with open("books.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    print("Successfully loaded data set")
    return books