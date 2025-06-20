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



import altair as alt
import geopandas as gpd
import streamlit as st

# Funzione per caricare la mappa del mondo (come da laboratorio)
@st.cache_data
def carica_mondo():
    url = "https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip"
    return gpd.read_file(url)

# Funzione per creare la mappa con percentuale vaccinati
def crea_mappa_percentuale(df_percentuale):
    mondo = carica_mondo()

    df_join = mondo.merge(
        df_percentuale,
        how="left",
        left_on="ADMIN",
        right_on="location"
    )

    mappa = (
        alt.Chart(df_join)
        .mark_geoshape(stroke="white")
        .encode(
            color=alt.Color(
                "percentuale_vaccinati:Q",
                scale=alt.Scale(
                    scheme="inferno",  # scelte: inferno, plasma, viridis, magma
                    domain=(0, 100),
                    clamp=True
                ),
                title="% popolazione vaccinata"
            ),
            tooltip=[
                "ADMIN",
                alt.Tooltip("percentuale_vaccinati:Q", format=".1f", title="% vaccinati")
            ]
        )
        .properties(width=800, height=500)
        .project("equalEarth")
    )

    return mappa

# Funzione add_map (opzionale — se vuoi come nei laboratori)
def add_map(mappa):
    mappa.save("mappa.html")
    with open("mappa.html") as fp:
        st.components.v1.html(fp.read(), width=800, height=600)
