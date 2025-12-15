import json
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# Caminho do json
caminho = "CA_category_id.json"
#carregamento dos dados com cache
@st.cache_data
def carregar_dados():
    df_ca= pd.read_csv("CAvideos.csv", encoding='UTF-8')
    df_jp =pd.read_csv("JPvideos.csv", encoding='UTF-8')
    df_gb= pd.read_csv("GBvideos.csv", encoding='UTF-8')
    df_de =pd.read_csv("DEvideos.csv", encoding='UTF-8')
    df_in= pd.read_csv("INvideos.csv", encoding='UTF-8')
    df_kr =pd.read_csv("KRvideos.csv", encoding='UTF-8')
    df_ru= pd.read_csv("RUvideos.csv", encoding='UTF-8')
    df_us =pd.read_csv("USvideos.csv", encoding='UTF-8')
    df_mx= pd.read_csv("MXvideos.csv", encoding='UTF-8')
    df_fr =pd.read_csv("FRvideos.csv", encoding='UTF-8')
    return df_ca,df_jp,df_gb,df_de,df_in,df_kr,df_ru,df_us,df_mx,df_fr
df_ca,df_jp,df_gb,df_de,df_in,df_kr,df_ru,df_us,df_mx,df_fr = carregar_dados()


st.set_page_config(layout="wide")

# abrir e carregar o json
with open(caminho, "r", encoding="utf-8") as f:
    data = json.load(f)

categorias = {
    int(item["id"]): item["snippet"]["title"]
    for item in data["items"]
}

#mapeamento das categorias

df_ca['category_id'] = df_ca['category_id'].map(categorias)
df_jp['category_id'] = df_jp['category_id'].map(categorias)
df_gb['category_id'] = df_gb['category_id'].map(categorias)
df_de['category_id'] = df_de['category_id'].map(categorias)
df_in['category_id'] = df_in['category_id'].map(categorias)
df_kr['category_id'] = df_kr['category_id'].map(categorias)
df_ru['category_id'] = df_ru['category_id'].map(categorias)
df_us['category_id'] = df_us['category_id'].map(categorias)
df_mx['category_id'] = df_mx['category_id'].map(categorias)
df_fr['category_id'] = df_fr['category_id'].map(categorias)







st.title("Análise dos vídeos em alta no YouTube por país")


#cores dos gráficos
cores = cm.plasma(np.linspace(0, 1, 10))
#seletor dos países
escolhas = {
    "Canadá": df_ca,
    "Japão": df_jp,
    "Reino Unido": df_gb,
    "Alemanha": df_de,
    "Índia": df_in,
    "Coreia do Sul": df_kr,
    "Rússia": df_ru,
    "Estados Unidos": df_us,
    "México": df_mx,
    "França": df_fr
}
st.subheader(f'Top 10 categorias com mais vídeos em alta')

#gráficos lado a lado
col1, col2 = st.columns(2)
with col1:
    #filtro
    opcao = st.selectbox("Selecione o país:", list(escolhas.keys()), key='opcao1')
    #grafico
    fig,ax= plt.subplots(figsize=(25,10))
    ax.barh(escolhas[opcao].groupby('category_id').size().sort_values(ascending=False).head(10).index,
      escolhas[opcao].groupby('category_id').size().sort_values(ascending=False).head(10).values,color= cores)
    plt.xticks( fontsize=25)
    plt.yticks( fontsize=25)
    plt.xlabel("Quantidade de vídeos em alta", fontsize=25)
    plt.ylabel("Categoria", fontsize=25)
    ax.invert_yaxis()
    st.pyplot(fig)

with col2:
    #filtro
    opcao2 = st.selectbox("Selecione o país:", list(escolhas.keys()), key='opcao2')
    #grafico
    fig,ax= plt.subplots(figsize=(25,10))
    ax.barh(escolhas[opcao2].groupby('category_id').size().sort_values(ascending=False).head(10).index,
    escolhas[opcao2].groupby('category_id').size().sort_values(ascending=False).head(10).values, color= cores)
    plt.xticks( fontsize=25)
    plt.yticks( fontsize=25)
    plt.xlabel("Quantidade de vídeos em alta", fontsize=25)
    plt.ylabel("Categoria", fontsize=25)
    ax.invert_yaxis()
    st.pyplot(fig)


st.subheader(f'Países que mais engajam (Likes/Views)')


vl=[]
#calculo do engajamento médio por país
for i in escolhas.values():
    vl.append(i['likes'].sum()/i['views'].sum())
pais=list(escolhas.keys())


#grafico
fig,ax= plt.subplots(figsize=(25,10))
ax.bar(pais,vl,color=cores)
plt.xticks( fontsize=20)
plt.yticks( fontsize=20)
plt.xlabel("País", fontsize=20)
plt.ylabel("Engajamento médio (likes / views)", fontsize=20)
st.pyplot(fig)


st.subheader(f'Países que mais engajam (Likes/Views) por categoria')
#filtro
pais_eng = st.selectbox(
    "Selecione o país:", 
    list(escolhas.keys()), 
    key="engajamento_pais")

df_eng = escolhas[pais_eng].copy()
#criacao de nova coluna
df_eng["engajamento"] = df_eng["likes"] / df_eng["views"]
eng_por_categoria = (df_eng.groupby("category_id")["engajamento"].mean().sort_values(ascending=False))
#grafico
fig, ax = plt.subplots(figsize=(25, 10))
ax.barh(eng_por_categoria.index, eng_por_categoria.values, color=cores)
ax.invert_yaxis()
plt.xlabel("Engajamento médio (likes / views)", fontsize=25)
plt.ylabel("Categoria", fontsize=25)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

st.pyplot(fig)

st.subheader("Engajamento médio geral por categoria (Likes/Views)")

#juntar os dataframes
df_all = pd.concat(escolhas.values(), ignore_index=True)
#calcular engajamento
df_all["engajamento"] = (df_all["likes"]  ) / df_all["views"]

eng_geral_cat = (df_all.groupby("category_id")["engajamento"].mean().sort_values(ascending=False))
# gráfico
fig, ax = plt.subplots(figsize=(25, 10))
ax.barh(eng_geral_cat.index, eng_geral_cat.values, color=cores)
ax.invert_yaxis()

plt.xlabel("Engajamento médio likes / views", fontsize=25)
plt.ylabel("Categoria", fontsize=25)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

st.pyplot(fig)

tab1,tab2= st.tabs(["Canais mais famosos por país","Canais mais famosos por ano"])
with tab1:
    st.subheader("Canais com mais vídeos em alta por país")
    #filtro
    pais= tab1.selectbox("Selecione o país:", list(escolhas.keys()), key='canalpais')
    #grafico
    fig,ax= plt.subplots(figsize=(25,10))
    ax.barh(escolhas[pais].groupby('channel_title').size().sort_values(ascending=False).head(10).index,
    escolhas[pais].groupby('channel_title').size().sort_values(ascending=False).head(10).values,color= cores)
    plt.xticks( fontsize=25)
    plt.yticks( fontsize=25)
    plt.xlabel("Número de vídeos em alta", fontsize=25)
    plt.ylabel("Canal", fontsize=25)
    ax.invert_yaxis()
    tab1.pyplot(fig)
with tab2:
    st.subheader("Canais com mais vídeos em alta por ano")
    c4, c5= st.columns(2)
    #filtros
    with c4:
        ano= st.selectbox("Selecione o ano:", ['2017','2018'], key='canalano')
    with c5:
        pais= st.selectbox("Selecione o país:", list(escolhas.keys()), key='canalpais2')
    #conversao da coluna de data
    escolhas[pais]['trending_date'] = pd.to_datetime(df_us['trending_date'], format='%y.%d.%m')
    #separacao por ano
    df_ano = escolhas[pais][escolhas[pais]['trending_date'].dt.year == int(ano)]
    #top 5 canais
    top5 = (df_ano.groupby('channel_title').size().sort_values(ascending=False).head(5).index)
    df_top5 = df_ano[df_ano['channel_title'].isin(top5)]
    #remocao de um outlier (mês 6 de 2018 poucos vídeos)
    df_top5 = df_top5[~((df_top5['trending_date'].dt.year == 2018) & 
          (df_top5['trending_date'].dt.month == 6))]
    #agrupamento por mês e canal
    df_top5['mes'] = df_top5['trending_date'].dt.month
    df_plot = df_top5.groupby(['mes', 'channel_title']).size().reset_index(name='qtd')
    fig, ax = plt.subplots(figsize=(25, 10))
    #plotagem das linhas
    for canal in top5:
        dados = df_plot[df_plot['channel_title'] == canal]
        ax.plot(dados['mes'], dados['qtd'], marker='o', label=canal)
    #grafico
    ax.set_xlabel("Mês", fontsize=25)
    ax.set_ylabel("Quantidade de vídeos em alta", fontsize=25)
    ax.tick_params(axis='both', labelsize=22)
    ax.legend(fontsize=20)
    ax.grid(True, linestyle='--', alpha=0.4)
    tab2.pyplot(fig)




