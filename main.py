import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# Dados de exemplo
dados = [
    {
        "nome": "Desvio Porto do Itaqui",
        "tipo": "Desvio Ferroviário",
        "status": "Concluída",
        "lat": -2.574826,
        "lon": -44.367735,
        "inicio": "2022-02-01",
        "fim": "2022-07-01",
        "foto_antes": "https://www.seligaalagoinhas.com.br/wp-content/uploads/2018/03/ANTT-publica-plano-de-outorga-para-leil%C3%A3o-da-Ferrovia-Norte-Sul.jpeg",
        "foto_depois": "https://folhadobico.com.br/wp-content/arquivo/2010/03/to127.jpg"
    },
    {
        "nome": "Soldagem Pátio Tirirical",
        "tipo": "Soldagem Aluminotérmica",
        "status": "Em andamento",
        "lat": -2.604922,
        "lon": -44.237591,
        "inicio": "2023-03-15",
        "fim": "",
        "foto_antes": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoD8zy5xiBgBhViu5Y85d1s89FaRT_r4dZ1oOQg02ahT9LJoHR0uuUpDWKs_af0CTy9HU&usqp=CAU",
        "foto_depois": "https://metainspecoes.com.br/servicos/inspecao-soldas/serv3/2.jpg"
    },
    {
        "nome": "Recuperação Linha Bacabeira",
        "tipo": "Manutenção de Linha",
        "status": "Concluída",
        "lat": -2.964373,
        "lon": -44.316992,
        "inicio": "2021-08-10",
        "fim": "2021-12-05",
        "foto_antes": "https://vault.pulsarimagens.com.br/file/thumb/11CD851.jpg",
        "foto_depois": "https://abet-trabalho.org.br/wp-content/uploads/2024/02/ferrovia20.02-1024x768.jpeg"
    },
    {
        "nome": "Obra Ponte Ferroviária Arari",
        "tipo": "Infraestrutura",
        "status": "Em andamento",
        "lat": -3.453175,
        "lon": -44.766433,
        "inicio": "2025-04-01",
        "fim": "",
        "foto_antes": "https://i.ytimg.com/vi/ieZ45cRudgo/maxresdefault.jpg",

    },

    {
        "nome": "Manutenção Ramal Bacanga",
        "tipo": "Manutenção de Ramal",
        "status": "Concluída",
        "lat": -2.539135,
        "lon": -44.307236,
        "inicio": "2022-08-02",
        "fim": "2022-09-17",
        "foto_antes": "https://www.comprerural.com/wp-content/uploads/2020/07/ferrovia-norte-sul-do-Brasil-2.jpg",
        "foto_depois": "https://agenciainfra.com/blog/wp-content/uploads/2023/05/credito-Tina-Coelho-Terra-Imagem-Infra-SA.jpeg"
    },
    {
        "nome": "Recapeamento Via Ferroviária Santa Inês",
        "tipo": "Recapeamento de Via",
        "status": "Concluída",
        "lat": -3.667028,
        "lon": -45.377506,
        "inicio": "2023-01-05",
        "fim": "2023-02-25",
        "foto_antes": "https://i.ytimg.com/vi/UQNCFJgVzsQ/hq720.jpg?sqp=-oaymwE7CK4FEIIDSFryq4qpAy0IARUAAAAAGAElAADIQj0AgKJD8AEB-AH-CYAC0AWKAgwIABABGGUgVyhAMA8=&rs=AOn4CLBI5GjR6LrJb7JqLvbKDQO49JksmA",

    },
    {
        "nome": "Terraplenagem Ferrovia Açailândia",
        "tipo": "Terraplenagem",
        "status": "Em andamento",
        "lat": -4.948277,
        "lon": -47.500017,
        "inicio": "2024-05-10",
        "fim": "",
        "foto_antes": "https://i0.wp.com/www.brasilferroviario.com.br/wp-content/uploads/2024/01/image-38.png?w=816&ssl=1",

    }
]

df = pd.DataFrame(dados)
st.set_page_config(layout="wide")

# --- TOPO: Logo e Título colorido ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image('logo_dl.png', width=90)
with col2:
    st.markdown(
        "<h1 style='color:#ff5a00; font-size: 2.5em; font-weight: bold; margin-bottom: 0.1em;'>"
        "Painel de Obras Engenharia</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 3px solid #ff5a00; margin-top: 0.1em; margin-bottom: 1em;'>", unsafe_allow_html=True)

# --- KPIs rápidos ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de Obras", len(df))
kpi2.metric("Concluídas", len(df[df['status']=="Concluída"]))
kpi3.metric("Em andamento", len(df[df['status']=="Em andamento"]))
kpi4.metric("Municípios", df['nome'].str.extract(r'([A-ZÁ-Úa-zá-ú\s]+)$').nunique()[0])  # Simples, pode melhorar se quiser campo 'cidade'

# --- Descrição ---
st.write(
    "Selecione os filtros ao lado para explorar todas as obras da empresa de forma interativa no mapa abaixo. "
    "Clique nos marcadores para visualizar detalhes e fotos de cada projeto."
)

# --- FILTROS ---
tipos = ["Todos"] + sorted(df["tipo"].unique())
status_opcoes = ["Todos"] + sorted(df["status"].unique())
tipo_filtro = st.sidebar.selectbox("Filtrar por Tipo de Serviço", tipos)
status_filtro = st.sidebar.selectbox("Filtrar por Status", status_opcoes)
busca = st.sidebar.text_input("Buscar por nome da obra")

# Aplicar filtros
df_filtrado = df.copy()
if tipo_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["tipo"] == tipo_filtro]
if status_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["status"] == status_filtro]
if busca:
    df_filtrado = df_filtrado[df_filtrado["nome"].str.contains(busca, case=False)]

# --- Centralização dinâmica do mapa ---
if not df_filtrado.empty:
    lat_center = df_filtrado['lat'].mean()
    lon_center = df_filtrado['lon'].mean()
else:
    lat_center, lon_center = -2.7, -44.3

# --- Mapa com ícones customizados ---
m = folium.Map(location=[lat_center, lon_center], zoom_start=7)
for idx, row in df_filtrado.iterrows():
    html = f"""
    <h4 style='color:#ff5a00;'>{row['nome']}</h4>
    <b>Tipo:</b> {row['tipo']}<br>
    <b>Status:</b> {row['status']}<br>
    <b>Início:</b> {row['inicio']}<br>
    <b>Fim:</b> {row['fim'] if row['fim'] else 'Em andamento'}<br>
    """

    if 'foto_antes' in row and row['foto_antes']:
        html += f"<b>Antes:</b><br><div style='text-align:center'><img src='{row['foto_antes']}' style='width:100%; max-width:350px;'></div><br>"
    if 'foto_depois' in row and row['foto_depois']:
        html += f"<b>Depois:</b><br><div style='text-align:center'><img src='{row['foto_depois']}' style='width:100%; max-width:350px;'></div><br>"

    popup = folium.Popup(html, max_width=400)
    # aumente o max_width conforme preferir

    color = 'green' if row['status'] == 'Concluída' else 'blue'
    icone = "wrench"
    if row['tipo'] == "Desvio Ferroviário":
        icone = "train"
    elif row['tipo'] == "Infraestrutura":
        icone = "road-bridge"
    elif row['tipo'] == "Soldagem Aluminotérmica":
        icone = "fire"
    elif row['tipo'] == "Expansão de Pátio":
        icone = "warehouse"
    elif row['tipo'] == "Terraplenagem":
        icone = "truck"
    elif row['tipo'] == "Passagem de Nível":
        icone = "road"
    elif row['tipo'] == "Recapeamento de Via":
        icone = "road"
    elif row['tipo'] == "Terminal Ferroviário":
        icone = "industry"
    elif row['tipo'] == "Manutenção de Linha":
        icone = "tools"
    elif row['tipo'] == "Manutenção de Ramal":
        icone = "tools"
    # Outros tipos...

    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=popup,
        icon=folium.Icon(color=color, icon=icone, prefix="fa")
    ).add_to(m)

# --- Mapa no Streamlit ---
st_folium(m, width=1500, height=800)

# --- Download Excel dos dados filtrados ---
st.download_button(
    label="Baixar Excel das Obras Filtradas",
    data=df_filtrado.to_csv(index=False).encode('utf-8'),
    file_name="obras_filtradas.csv",
    mime="text/csv",
)

# --- Galeria de fotos "depois" ---
if not df_filtrado.empty:
    st.markdown("### Fotos das Obras Concluídas (Depois)")
    imagens = [row['foto_depois'] for idx, row in df_filtrado.iterrows() if row['foto_depois']]
    cols = st.columns(5)
    for i, img in enumerate(imagens):
        with cols[i % 5]:
            st.image(img, use_column_width='always', caption=f"Obra {i+1}")

# --- Tabela expandida ---
with st.expander("Ver tabela de obras filtradas"):
    st.dataframe(df_filtrado)

# --- Rodapé ---
st.markdown(
    "<hr style='border: 1px solid #ff5a00;'>"
    "<p style='text-align: right; color: #ff5a00; margin-top: 2em;'>"
    "Segurança, qualidade e pontualidade – sua obra mapeada do início ao fim."
    "</p>",
    unsafe_allow_html=True
)
