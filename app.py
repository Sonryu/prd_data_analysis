#
#  Copyright (c) 2026 Ramon Watson de Lima Vilar
#  Licensed under the MIT License. 
#  See LICENSE file in the project root for full license information.
#
#####||##########||##########||##########||##########||##########||##########||##########||#####
import tara as tr
import streamlit as st
import numpy as np
import formulas as fm 
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- configs
load_dotenv() # Carrega variáveis de ambiente do .env (apenas para rodar local)

# Configuração de Segurança: Busca a chave no ambiente ou nos Secrets do Streamlit
# ele apenas pedirá a chave ou usará a que estiver configurada no servidor do usuario
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

# cabeçalho
# ---------

# > mudar imagem elet.png
st.logo('Logo - PRD.png')
st.set_page_config(page_title='PRD: Análise de dados de teste estático', layout='centered', page_icon='Logo - PRD.png')
st.image('elet.jpg')
st.header('Sistema de análise de dados de teste estático')
st.subheader('Potiguar Rocket Design', divider=True)

with st.sidebar:
    st.image('analise_de_dados.jpg')

# upload de arquivo
# -----------------
uploaded_files = st.file_uploader(
        'Upload de arquivo para análise'
        ' Arquivos aceitos: `.csv`, `.txt` ou `.wsv` com valores separados por espaço "` `".',
        accept_multiple_files=True, type=['csv', 'txt', 'wsv'])
if not uploaded_files:
    continue
