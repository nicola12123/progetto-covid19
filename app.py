import streamlit as st
import polars as pl
from preprocessing import carica_e_pulisci_dati
from visualizations import crea_grafico_linee

# Titolo della pagina Streamlit
st.write("""# Andamento COVID-19: contagi e vaccinazioni""")

st.write("""Questa applicazione permette di esplorare l'andamento dei contagi e delle vaccinazioni nei diversi paesi.""")

# Carico i dati
dati = carica_e_pulisci_dati()

# Estraggo la lista dei paesi unici (ordinati)
paesi = dati.select("location").unique().sort("location").to_series().to_list()

# Selectbox per scegliere il paese
paese_selezionato = st.selectbox("Seleziona un paese:",paesi)

# Filtro il dataframe sul paese selezionato
dati_filtrati = dati.filter(pl.col("location") == paese_selezionato)

# Slider per scegliere l'intervallo temporale
data_min = dati_filtrati.select("date").min()[0, 0]
data_max = dati_filtrati.select("date").max()[0, 0]

intervallo_date = st.slider("Seleziona l'intervallo temporale:",
                            value=(data_min, data_max),
                            min_value=data_min,
                            max_value=data_max)

# Applico il filtro
dati_filtrati = dati_filtrati.filter(
    (pl.col("date") >= intervallo_date[0]) & (pl.col("date") <= intervallo_date[1])
)

# Mostro i dati filtrati (tabella)
st.write("Dati selezionati:", dati_filtrati)

# Converto in dataframe pandas per il grafico Altair
dati_pd = dati_filtrati.to_pandas()

# Radio per scegliere la variabile da plottare
variabile = st.radio("Cosa vuoi visualizzare?",
    options=["new_cases", "new_deaths", "people_vaccinated", "people_fully_vaccinated"],
    index=0)


grafico = crea_grafico_linee(dati_pd, variabile, paese_selezionato)

# Mostro il grafico
st.altair_chart(grafico, use_container_width=True)



# Mappa percentuale vaccinati

st.write("### Mappa globale - Percentuale popolazione vaccinata")

# Calcolo percentuale vaccinati
dati_completi = carica_e_pulisci_dati().join(
    pl.read_csv("data/owid-covid-data.csv").select(["location", "population"]).unique(),
    on="location",
    how="left"
)

dati_percentuale = (
    dati_completi.group_by("location")
    .agg(
        pl.col("people_vaccinated").max().alias("people_vaccinati"),
        pl.col("population").max().alias("population")
    )
    .with_columns(
        (pl.col("people_vaccinati") / pl.col("population") * 100).alias("percentuale_vaccinati")
    )
    .select(["location", "percentuale_vaccinati"])
    .to_pandas()
)

# Creo e mostro la mappa
from visualizations import crea_mappa_percentuale, add_map

mappa = crea_mappa_percentuale(dati_percentuale)
add_map(mappa)

