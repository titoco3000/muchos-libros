import streamlit as st
import pandas as pd
from rec import recomendar

def exibirRecomendacao(resposta:str, recs:list):
    col1, col2 = st.columns([2, 1])

    # Coluna de mensagens    
    with col1:
        with st.chat_message("assistant"):
            st.markdown(resposta)
    
    # Coluna de recomendações    
    with col2:
        if len(recs) > 0:
            df = pd.DataFrame(
                [[livro["titulo"], livro["genero"]] for livro in recs], columns=("Título","Gênero"))
            st.table(df)


st.title("Book Bot")

# Define a mensagem inicial
INITIAL_MESSAGE = {"role": "assistant", "content": "Olá! Eu posso te recomendar livros."}

# Inicia estados 
if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_MESSAGE]
if "recomendacoes" not in st.session_state:
    st.session_state.recomendacoes = [[] for _ in st.session_state.messages]

# Adiciona botão de reset
if st.button("Limpar conversa"):
    st.session_state.messages = [INITIAL_MESSAGE]
    st.session_state.recomendacoes = [[]]

# Mostra mensagens e recomendações
for i, message in enumerate(st.session_state.messages):
    exibirRecomendacao(message["content"], st.session_state.recomendacoes[i])

# Define input
if prompt := st.chat_input("O que você procura?"):
    # Mostra msg do usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Adiciona ao historico
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mensagem do usuario não tem recomendações
    st.session_state.recomendacoes.append([])
    
    # Gera resposta e recomendações
    resposta, recomendacoes = recomendar(st.session_state.messages)
    
    exibirRecomendacao(resposta, recomendacoes)

    # Adiciona nova informação ao histórico da conversa
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.session_state.recomendacoes.append(recomendacoes)
