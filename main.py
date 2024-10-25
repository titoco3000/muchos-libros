
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

query = "Eu gosto de histórias noir"
client = OpenAI()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index_name = "libros"
index = pc.Index(index_name)


query_embeddings = client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
).data[0].embedding,

resultados = [obj['metadata'] for obj in index.query(
        vector=query_embeddings, top_k=1, include_metadata=True
    )['matches']]

print(resultados)

messages = [
    {'role':'system','content':f'Based on the list below, answer to any question with book recomendations, with justification: {resultados}'},
    {'role':'user','content':query},
]

response = client.chat.completions.create(
    model='gpt-4o-mini',
    temperature=0.2,
    messages=messages
)

print(response.choices[0].message.content)
