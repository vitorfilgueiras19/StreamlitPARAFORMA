import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Streamlit-Indios📊", layout="wide", page_icon="🚀")

# Customização do tema (Fundo azul escuro e texto amarelo)
st.markdown(
    """
    <style>
    .stApp { background-color: #0A192F !important; }
    [data-testid="stSidebar"] { background-color: #0D203D !important; }
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown { color: #FFD700 !important; }
    button[data-baseweb="tab"] p { color: #FFD700 !important; }
    button[data-baseweb="tab"][aria-selected="true"] { border-bottom-color: #FFD700 !important; }
    [data-testid="stMetricLabel"] > div { color: #FFD700 !important; }
    [data-testid="stMetricValue"] > div { color: #FFFFFF !important; }
    </style>
    """,
    unsafe_allow_html=True
)