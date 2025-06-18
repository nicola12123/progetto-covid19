import altair as alt
import geopandas as gpd
import streamlit as st

def crea_grafico_linee(df, colonna_y, nome_paese):
    grafico = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Data"),
            y=alt.Y(f"{colonna_y}:Q", title=colonna_y.replace("_", " ").capitalize()),
            tooltip=["date", colonna_y]
        )
        .properties(
            title=f"{colonna_y.replace('_', ' ').capitalize()} in {nome_paese}",
            width=700,
            height=400
        )
    )
    return grafico



# Carico la geografia del mondo (come nel laboratorio mappe)
@st.cache_data
def carica_mondo():
    url = "https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip"
    mondo = gpd.read_file(url)
    return mondo

# Crea mappa percentuale vaccinati
def crea_mappa_percentuale(df_percentuale):
    mondo = carica_mondo()

    # Merge tra mondo e dati COVID
    df_join = mondo.merge(
        df_percentuale,
        how="left",
        left_on="ADMIN",
        right_on="location"
    )

    # Mappa Altair
    mappa = (
        alt.Chart(df_join)
        .mark_geoshape(stroke="white")
        .encode(
            color=alt.Color("percentuale_vaccinati:Q", scale=alt.Scale(scheme="viridis"), title="% popolazione vaccinata"),
            tooltip=["ADMIN", "percentuale_vaccinati"]
        )
        .properties(width=800, height=500)
        .project("equalEarth")
    )

    return mappa

# Funzione per salvare e mostrare la mappa (come add_map nel laboratorio)
def add_map(mappa):
    mappa.save("mappa.html")
    with open("mappa.html") as fp:
        st.components.v1.html(fp.read(), width=800, height=600)
