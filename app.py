## ========================================== # ==========================================
#  Copyright (c) 2026 Ramon Watson de Lima Vilar
#  Licensed under the MIT License. 
#  See LICENSE file in the project root for full license information.
#
# ========================================== # ==========================================
import tara as tr
import streamlit as st
import numpy as np
import formulas as fm 
from google import genai 
import os
from dotenv import load_dotenv




# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA (DEVE SER O PRIMEIRO)
# ==========================================

st.set_page_config(
    page_title='PRD: Análise de dados de teste estático', 
    layout='centered', 
    page_icon='Logo - PRD.png'
)



# ==========================================
# 2. CONFIGURAÇÕES E CHAVES (LOGICA)
# ==========================================

load_dotenv() # Carrega variáveis de ambiente do .env (apenas para rodar local)

# Prioridade de chave: 1. Sidebar (se digitada) | 2. Env/Secrets
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

# Lógica da Sidebar para chave customizada
with st.sidebar:
    st.image('analise_de_dados.jpg')
    st.markdown("---")
    custom_key = st.text_input("Insira sua Gemini API Key", type="password")
    if custom_key:
        api_key = custom_key

# Inicialização do Gemini
if api_key:
    client = genai.Client(api_key=api_key) # Novo jeito de criar o cliente
    st.sidebar.success("Gemini API (v3) pronta!")
else:
    st.sidebar.error("API Key não encontrada.")


# ==========================================
# 3. CABEÇALHO E INTERFACE (VISUAL)
# ==========================================

# > mudar imagem elet.png
st.logo('Logo - PRD.png')
st.image('elet.jpg')
st.header('Sistema de análise de dados de teste estático')
st.subheader('Potiguar Rocket Design', divider=True)



# ==========================================
# 4. ENTRADA DE DADOS
# ==========================================

uploaded_files = st.file_uploader(
        'Upload de arquivo para análise'
        ' Arquivos aceitos: `.csv`, `.txt` ou `.wsv` com valores separados por espaço "` `".',
        accept_multiple_files=True, type=['csv', 'txt', 'wsv']
)

if not uploaded_files:
    st.stop()

st.success(f"Análise iniciada para {len(uploaded_files)} arquivo(s)!")