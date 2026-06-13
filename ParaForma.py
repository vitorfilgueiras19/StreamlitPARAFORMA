import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Stream-Paraforma📊", layout="wide", page_icon="🚀")

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

# Painel lateral de filtros
st.sidebar.header("🔍 Filtros")

anos = sorted(df['Year'].unique().tolist())
ano_escolhido = st.sidebar.multiselect("Selecione o(s) Ano(s)", anos, default=anos)

lista_regioes = df['Region'].unique().tolist() if 'Region' in df.columns else df['State'].unique().tolist()
regiao_escolhida = st.sidebar.multiselect("Selecione a Região/Estado", lista_regioes, default=lista_regioes)

lista_segmentos = df['Segment'].unique().tolist()
segmento_escolhido = st.sidebar.multiselect("Selecione o(s) Segmento(s)", lista_segmentos, default=lista_segmentos)

# Aplicação dos filtros no dataframe
df_filtrado = df[df['Year'].isin(ano_escolhido) & df['Segment'].isin(segmento_escolhido)]
if 'Region' in df.columns:
    df_filtrado = df_filtrado[df_filtrado['Region'].isin(regiao_escolhida)]
else:
    df_filtrado = df_filtrado[df_filtrado['State'].isin(regiao_escolhida)]

# Interface principal
st.title("Stream-Paraforma 📊")
st.markdown("Dashboard operacional de análise de vendas.")

aba1, aba2, aba3, aba4 = st.tabs([
    "🏠 Visão Geral", 
    "📈 Perguntas 1-5", 
    "🚀 Perguntas 6-10", 
    "💡 Conclusões"
])

# === ABA 1: VISÃO GERAL ===
with aba1:
    st.header("Visão Geral da Base de Dados")
    
    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado para a combinação de filtros selecionada.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total de Vendas", f"${df_filtrado['Sales'].sum():,.2f}")
        c2.metric("Total de Pedidos", len(df_filtrado))
        c3.metric("Cidades Atendidas", df_filtrado['City'].nunique())
        
        st.dataframe(df_filtrado.head(10), use_container_width=True)
        
        # Exportação dos dados filtrados
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Baixar Dados Filtrados (CSV)", data=csv, file_name='dados_filtrados.csv', mime='text/csv')