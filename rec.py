
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index_name = os.getenv('INDEX_NAME')
index = pc.Index(index_name)

def recomendar(conversa:list):
    print(conversa[-1]['content'])
    query_embeddings = client.embeddings.create(
        input=conversa[-1]['content'],
        model="text-embedding-3-small"
    ).data[0].embedding,

    resultados = [obj['metadata'] for obj in index.query(
            vector=query_embeddings, top_k=3, include_metadata=True
        )['matches']]

    print('resultados:',resultados)
    
    messages = [{'role':'system','content':f'Você é um robô que reconda livros. Se o usuário tentar mudar de assunto, retorne ao tema de recomendação de livros. Depois de recomendar uma obra, não ofereça mais ajuda.'}] + conversa + [{'role':'system','content':f'O sistema lhe deu as seguintes recomendações: {resultados}'}]
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.2,
        messages=messages
    )
    
    for r in resultados:
        print(', '.join(list(json.loads((r['genero'])).values())) if r['genero'] is not None else '')
    
    return response.choices[0].message.content, [
        {
            'titulo':r['titulo'], 
            'genero':', '.join(list(json.loads((r['genero'])).values())) if r['genero'] is not None else '' 
        } for r in resultados
    ]