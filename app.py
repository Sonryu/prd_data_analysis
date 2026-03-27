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

# cabeçalho
# ---------
st.logo('Logo - PRD.png')
st.set_page_config(page_title='PRD: Análise de dados de teste estático', layout='centered', page_icon='Logo - PRD.png')
st.image('elet.jpg')
st.header('Sistema de análise de dados de teste estático')
st.subheader('Potiguar Rocket Design', divider=True)

with st.sidebar:
    st.image('analise_de_dados.jpg')

