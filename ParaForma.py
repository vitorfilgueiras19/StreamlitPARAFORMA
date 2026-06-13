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

# Configuração global do Matplotlib para seguir o tema do app
plt.rcParams.update({
    'figure.facecolor': '#0A192F',
    'axes.facecolor': '#0A192F',
    'text.color': '#FFD700',
    'axes.labelcolor': '#FFD700',
    'axes.edgecolor': '#FFD700',
    'xtick.color': '#FFD700',
    'ytick.color': '#FFD700'
})

@st.cache_data
def carregar_dados():
    df = pd.read_excel("Sample - Superstore.xls")
    
    # Tratamento de tipos e valores ausentes
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['City'] = df['City'].fillna("Não Informado")
    df['State'] = df['State'].fillna("Não Informado")
    
    # Colunas auxiliares para agrupamento temporal
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Ano-Mes'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
    
    return df

df = carregar_dados()