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
    # 1. Leitura dos dados brutos (Exemplo assumindo colunas de tempo e valor bruto)
    # Aqui você usará sua lógica de leitura (ex: np.loadtxt ou genfromtxt)
    raw_data = np.genfromtxt(file, delimiter=None) # Ajustar delimitador se necessário
    
    # 2. Aplicação da TARA e Conversão de Tempo
    # tempo_s = fm.converter_segundos(raw_data[:, 0])
    # _, empuxo_n = tr.tara(raw_data[:, 0], raw_data[:, 1])
    
    st.header(f'Dados do teste: {file.name}', divider=True)
    name = st.text_input(f'Nome do teste ({i}):', value=file.name, key=f"name_{i}")

    col1, col2 = st.columns([60, 40])
    
    with col1:
        # Gráfico Principal usando os dados transformados
        fig = px.line(
            x=raw_data[:, 0], # Substituir por tempo_s após ajuste
            y=raw_data[:, 1], # Substituir por empuxo_n após ajuste
            markers=True, 
            title=f'Curva de empuxo: {name}', 
            template='plotly_dark'
        )
        
        fig.update_layout(xaxis_title='Tempo [s]', yaxis_title='Empuxo [N]')
        
        st.plotly_chart(fig, config={
            'modeBarButtonsToRemove': ['lasso2d', 'select', 'pan', 'zoomIn', 'zoomOut', 'autoScale'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'curva_empuxo_{name}',
                'width': 600,
                'height': 500,
                'scale': 2 # Melhora a resolução do PNG
            }
        }, theme=None)

    with col2:
        # Espaço reservado para a Tabela de Números (Passo 5)
        st.write("### Resumo de Métricas")
        # Aqui entrarão os cálculos de fm.calcular_empuxo_maximo, etc