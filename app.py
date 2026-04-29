## ========================================== # ==========================================
#  Copyright (c) 2026 Ramon Watson de Lima Vilar
#  Licensed under the MIT License. 
#  See LICENSE file in the project root for full license information.
#
# ========================================== # ==========================================
import plotly.express as px
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
    st.image('image/analise_de_dados.jpg')
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
st.logo('image/Logo - PRD.png')
st.image('image/elet.jpg')
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

# --- avaliar e limpar os comentarios e configuacoes:

# Lista para armazenar os dados processados para a comparação 
analises_processadas = []

# Loop para processar cada arquivo individualmente
for i, file in enumerate(uploaded_files):

#  Leitura dos dados brutos
    
    data_bruta = np.genfromtxt(file, delimiter=None)
    
    # CALIBRAÇÃO: Aplicando a TARA e convertendo o tempo
    # data_bruta[:, 0] é a primeira coluna (tempo em ms)
    # data_bruta[:, 1] é a segunda coluna (leitura bruta do sensor)
    tempo_s_raw = fm.converter_segundos(data_bruta[:, 0])
    tempo_s, empuxo_n = tr.tara(tempo_s_raw, data_bruta[:, 1])

    st.header(f'Dados do teste: {file.name}', divider=True)
    name = st.text_input(f'Nome do teste ({i}):', value=file.name, key=f"name_{i}")

    col1, col2 = st.columns([60, 40])
    
    with col1:
        # 3. Gráfico com os dados CALIBRADOS
        fig = px.line(
            x=tempo_s,    # Agora em Segundos e calibrado
            y=empuxo_n,   # Agora em Newtons (N)
            markers=True, 
            title=f'Curva de empuxo (Calibrada): {name}', 
            template='plotly_dark'
        )
        
        fig.update_layout(xaxis_title='Tempo [s]', yaxis_title='Empuxo [N]')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Espaço reservado para a Tabela de Números (Passo 5)
        st.write("### Resumo de Métricas")
        # Aqui entrarão os cálculos de fm.calcular_empuxo_maximo, etc