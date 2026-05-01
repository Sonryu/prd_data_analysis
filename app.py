## ==========================================
#  Copyright (c) 2026 Ramon Watson de Lima Vilar
#  Licensed under the MIT License. 
#  See LICENSE file in the project root for full license information.
## ==========================================

import plotly.express as px
import plotly.graph_objects as go
import tara as tr
import streamlit as st
import numpy as np
import formulas as fm 
from google import genai 
import os
from dotenv import load_dotenv
from PIL import Image
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title='PRD: Análise de dados de teste estático', 
    layout='centered', 
    page_icon='Logo - PRD.png'
)

# --- Configurações de API e Variáveis de Ambiente ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

with st.sidebar:
    st.image('image/foguete_rasgando_ceu.png')
    st.markdown("---")
    custom_key = st.text_input("Insira sua Gemini API Key", type="password")
    if custom_key:
        api_key = custom_key

if api_key:
    client = genai.Client(api_key=api_key)
    st.sidebar.success("Gemini API pronta!")
else:
    st.sidebar.error("API Key não encontrada.")

# --- Interface Visual (Logo e Banner) ---
st.logo('image/Logo - PRD.png')

img = Image.open('image/foguete_app_analise_de_dados.png')
largura, altura = img.size
caixa_de_corte = (0, 150, largura, altura - 170)
img_cortada = img.crop(caixa_de_corte)
st.image(img_cortada)

st.header('Sistema de análise de dados de teste estático')
st.subheader('Potiguar Rocket Design', divider=True)

# --- Upload de Arquivos ---
uploaded_files = st.file_uploader(
        'Upload de arquivo para análise (CSV, TXT ou WSV)',
        accept_multiple_files=True, type=['csv', 'txt', 'wsv']
)

if not uploaded_files:
    st.stop()

st.success(f"Análise iniciada para {len(uploaded_files)} arquivo(s)!")

# --- Processamento de Dados ---
dados_comparativos = []

for i, file in enumerate(uploaded_files):
    # Leitura e calibração
    data_bruta = np.genfromtxt(file, delimiter=None)
    data_calibrada_full = fm.calibrar_curva_cel_grande(data_bruta)
    
    # Detecção automática de queima (corte por limiar de empuxo)
    limiar = 5.0 
    indices_queima = np.where(data_calibrada_full[:, 1] > limiar)[0]

    if len(indices_queima) > 0:
        data = data_calibrada_full[indices_queima[0]:indices_queima[-1], :]
    else:
        data = data_calibrada_full
    
    name = st.text_input(f'Nome do teste ({i}):', value=file.name, key=f"name_{i}")

    # Extração de métricas
    tempo_rel_s = fm.converter_segundos(data[:, 0] - data[0, 0])
    empuxo_n = data[:, 1]
    
    dados_comparativos.append({
        'Tempo [s]': tempo_rel_s,
        'Empuxo [N]': empuxo_n,
        'Motor': name
    })

    # Exibição de resultados individuais
    st.header(f'Análise: {file.name}', divider=True)
    col1, col2 = st.columns([65, 35])
    
    with col1:
        fig_final = px.line(
            x=tempo_rel_s, 
            y=empuxo_n, 
            markers=True, 
            template='plotly_dark',
            labels={'x': 'Tempo [s]', 'y': 'Empuxo [N]'}
        )
        fig_final.update_layout(xaxis_title='Tempo [s]', yaxis_title='Empuxo [N]')
        st.plotly_chart(fig_final, use_container_width=True, key=f"fig_{i}")

    with col2:
        st.write("### Estatísticas")
        stats_data = {
            "Métrica": ["Empuxo Máximo", "Empuxo Médio", "Impulso Total", "Tempo de Queima", "Tempo até o pico"],
            "Valor": [
                f"{fm.calcular_empuxo_maximo(empuxo_n):.2f} N",
                f"{fm.empuxo_medio(empuxo_n, fm.calcular_tempo(tempo_rel_s)):.2f} N",
                f"{fm.calcular_impulso_total(empuxo_n, tempo_rel_s):.2f} Ns",
                f"{fm.calcular_tempo(tempo_rel_s):.3f} s",
                f"{fm.calcular_t_p(empuxo_n, tempo_rel_s):.3f} s"
            ]
        }
        st.table(stats_data)

        # Tabela estilizada para exportação (PNG)
        df_export = pd.DataFrame(stats_data)
        fig_table = go.Figure(data=[go.Table(
            header=dict(
                values=[f"<b>{c}</b>" for c in df_export.columns],
                fill_color='#1E1E1E',
                align='center',
                font=dict(color='white', size=14),
                line_color='black'
            ),
            cells=dict(
                values=[df_export.Métrica, df_export.Valor],
                fill_color='#2D2D2D',
                align='left',
                font=dict(color='white', size=13),
                line_color='black',
                height=30
            ))
        ])
        
        fig_table.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=200
        )
        
        st.plotly_chart(fig_table, use_container_width=True, config={
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'estatisticas_{name}',
                'scale': 3
            }
        })

# --- Comparativo Geral (se houver mais de um motor) ---
if len(dados_comparativos) > 1:
    st.divider()
    st.header("🚀 Comparativo Geral de Motores")
    
    df_lista = [pd.DataFrame({'Tempo [s]': d['Tempo [s]'], 'Empuxo [N]': d['Empuxo [N]'], 'Motor': d['Motor']}) for d in dados_comparativos]
    df_final_comp = pd.concat(df_lista)

    fig_comp = px.line(
        df_final_comp, 
        x='Tempo [s]', 
        y='Empuxo [N]', 
        color='Motor',
        title="Comparação de Curvas de Empuxo",
        template='plotly_dark'
    )
    st.plotly_chart(fig_comp, use_container_width=True)