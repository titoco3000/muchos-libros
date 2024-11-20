from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from dotenv import load_dotenv
import os
import itertools
import get_database

load_dotenv()

# livros = [
#     {
#         "nome":"A Saga de Fulano", 
#         "sinopse":"Um herói segue aventuras fantasticas em busca da espada sagrada para destruir o terrível imperador do mal.",
#         "genero":"aventura"
#     },
#     {
#         "nome":"Um corpo na Esquina", 
#         "sinopse":"A renomada detetive Sicrana, já não mais em seu dias de glória, se encontra de volta ao jogo contra a sua vontade.",
#         "genero":"suspense"
#     },
# ]

livros = get_database.get_data()


pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index_name = os.getenv('INDEX_NAME')

if index_name in pc.list_indexes().names():
    try:
        pc.delete_index(index_name, 30)
    except:
        print('não excluiu index (demorou demais)')
    print('excluiu')
    
    
pc.create_index(
    name=index_name, 
    dimension=1536, #dimensão usada pela openai
    metric='euclidean',
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1' #é a unica regiao no plano gratuito
    )
)
print("Created Index")

index = pc.Index(index_name)

client = OpenAI()

# vectors = [{
#     "id": str(i), 
#     "values": client.embeddings.create(
#         input=livro['sinopse'],
#         model="text-embedding-3-small"
#     ).data[0].embedding, 
#     "metadata": livro
# } for i, livro in enumerate(livros) ]

for i, livro in enumerate(livros):
    try:
        embedding = client.embeddings.create(input = livro['sinopse'],model = "text-embedding-3-small").data[0].embedding

        vector = {
            "id": str(i),
            "values": embedding,
            "metadata": livro
        }

        index.upsert(vectors=[vector])
        print(f"Vetor para '{livro['titulo']}' inserido com sucesso.")
    except Exception as e:
        print(f"Erro ao processar '{livro['nome']}': {e}")

# print(vectors)
print("Vetores Pronto")

def chunks(iterable, batch_size=200):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

vector_dim = 128
vector_count = 10000

# Upsert data with 200 vectors per upsert request
# for ids_vectors_chunk in chunks(vectors, batch_size=200):
#     index.upsert(vectors=ids_vectors_chunk) 