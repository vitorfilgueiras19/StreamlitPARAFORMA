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



# === ABA 2: PERGUNTAS 1 A 5 ===
with aba2:
    if df_filtrado.empty:
        st.warning("Selecione os filtros na barra lateral para gerar os gráficos.")
    else:
        # Pergunta 1
        st.subheader("1. Cidade com maior valor de venda em 'Office Supplies'")
        df_escritorio = df_filtrado[df_filtrado['Category'] == 'Office Supplies']
        if not df_escritorio.empty:
            cidade_campea = df_escritorio.groupby('City')['Sales'].sum().idxmax()
            valor_campeao = df_escritorio.groupby('City')['Sales'].sum().max()
            st.markdown(f"**Resultado:** {cidade_campea} (Total: ${valor_campeao:,.2f})")
            st.markdown("*Análise:* A concentração de vendas nesta cidade sugere maior densidade de clientes corporativos ou hubs comerciais.")
        else:
            st.write("Sem registros para esta categoria com os filtros atuais.")
        
        st.divider()

        # Pergunta 2
        st.subheader("2. Total de vendas por data do pedido")
        vendas_diarias = df_filtrado.groupby(df_filtrado['Order Date'].dt.date)['Sales'].sum()
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(vendas_diarias.index, vendas_diarias.values, color='cyan')
        ax2.set_title("Evolução Diária de Vendas")
        fig2.tight_layout()
        st.pyplot(fig2)
        st.markdown("*Análise:* O comportamento gráfico apresenta picos sazonais nítidos, característicos de compras volumosas em períodos específicos.")

        st.divider()

        # Pergunta 3
        st.subheader("3. Total de vendas por estado")
        vendas_por_estado = df_filtrado.groupby('State')['Sales'].sum().sort_values(ascending=False)
        fig3, ax3 = plt.subplots(figsize=(12, 5))
        vendas_por_estado.plot(kind='bar', ax=ax3, color='gold')
        plt.xticks(rotation=45, ha='right')
        fig3.tight_layout()
        st.pyplot(fig3)
        st.markdown("*Análise:* Distribuição desigual de receita entre os estados, evidenciando mercados consolidados versus regiões com potencial de expansão.")

        st.divider()

        # Pergunta 4
        st.subheader("4. Top 10 cidades em volume de vendas")
        top_cidades = df_filtrado.groupby('City')['Sales'].sum().nlargest(10)
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        top_cidades.plot(kind='bar', ax=ax4, color='lightgreen')
        plt.xticks(rotation=45, ha='right')
        fig4.tight_layout()
        st.pyplot(fig4)
        st.markdown("*Análise:* As dez principais cidades concentram uma parcela significativa do faturamento total da empresa.")

        st.divider()

        # Pergunta 5
        st.subheader("5. Representatividade de vendas por segmento")
        vendas_segmentos = df_filtrado.groupby('Segment')['Sales'].sum()
        fig5, ax5 = plt.subplots(figsize=(6, 6))
        ax5.pie(vendas_segmentos, labels=vendas_segmentos.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
        fig5.tight_layout()
        st.pyplot(fig5)
        st.markdown("*Análise:* Identificação do perfil de consumo predominante na base de dados atual, auxiliando o direcionamento estratégico.")
        
# === ABA 3: PERGUNTAS 6 A 10 ===
with aba3:
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

        # === ABA 3: PERGUNTAS 6 A 10 ===
with aba3:
    if df_filtrado.empty:
        st.warning("Selecione os filtros na barra lateral para gerar os gráficos.")
    else:
        # Pergunta 6
        st.subheader("6. Distribuição anual de vendas por segmento")
        vendas_ano_seg = df_filtrado.groupby(['Year', 'Segment'])['Sales'].sum().unstack()
        fig6, ax6 = plt.subplots(figsize=(10, 5))
        vendas_ano_seg.plot(kind='bar', ax=ax6)
        plt.xticks(rotation=0)
        fig6.tight_layout()
        st.pyplot(fig6)
        st.markdown("Análise: Permite monitorar o crescimento ou retração histórica de cada segmento de mercado.")

        st.divider()

        # Perguntas 7 e 8
        st.subheader("7 & 8. Simulação de Margem com Políticas de Desconto")
        c_sim1, c_sim2, c_sim3 = st.columns(3)
        limite = c_sim1.number_input("Gatilho do pedido ($)", value=1000)
        desc_alto = c_sim2.slider("Desconto para pedidos acima do gatilho (%)", 0, 50, 15) / 100
        desc_baixo = c_sim3.slider("Desconto padrão (%)", 0, 50, 10) / 100

        df_sim = df_filtrado.copy()
        df_sim['Desconto_Aplicado'] = df_sim['Sales'].apply(lambda x: desc_alto if x > limite else desc_baixo)
        df_sim['Sales_Com_Desconto'] = df_sim['Sales'] * (1 - df_sim['Desconto_Aplicado'])
        
        qtd_vendas_desc_alto = len(df_sim[df_sim['Desconto_Aplicado'] == desc_alto])
        
        st.write(f"*Pedidos afetados pelo desconto maior:* {qtd_vendas_desc_alto}")
        st.write(f"*Ticket médio original:* ${df_sim['Sales'].mean():,.2f}")
        st.write(f"*Ticket médio projetado:* ${df_sim['Sales_Com_Desconto'].mean():,.2f}")
        st.markdown("Análise: A simulação quantifica o impacto direto na receita bruta caso regras de precificação promocional flexíveis sejam adotadas.")

        st.divider()

        # Pergunta 9
        st.subheader("9. Média mensal de vendas por segmento")
        media_mensal = df_filtrado.groupby(['Ano-Mes', 'Segment'])['Sales'].mean().unstack()
        fig9, ax9 = plt.subplots(figsize=(10, 5))
        media_mensal.plot(kind='line', ax=ax9, marker='o', alpha=0.7)
        fig9.tight_layout()
        st.pyplot(fig9)
        st.markdown("Análise: Análise do comportamento do ticket médio por período, útil para detecção de variações e sazonalidade de curto prazo.")

        st.divider()

        # Pergunta 10
        st.subheader("10. Faturamento das 12 principais subcategorias por categoria")
        top12 = df_filtrado.groupby('Sub-Category')['Sales'].sum().nlargest(12).index
        df_top12 = df_filtrado[df_filtrado['Sub-Category'].isin(top12)]
        vendas_cat_sub = df_top12.groupby(['Sub-Category', 'Category'])['Sales'].sum().unstack()
        
        fig10, ax10 = plt.subplots(figsize=(12, 6))
        vendas_cat_sub.plot(kind='bar', stacked=True, ax=ax10)
        plt.xticks(rotation=45, ha='right')
        fig10.tight_layout()
        st.pyplot(fig10)
        st.markdown("Análise: Detalhamento do mix de produtos mais relevantes, indicando quais subcategorias sustentam as categorias macro.")