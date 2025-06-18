import streamlit as st
import polars as pl
from preprocessing import carica_e_pulisci_dati
from visualizations import crea_grafico_linee

# Titolo della pagina Streamlit
st.write("""
# Andamento COVID-19: contagi e vaccinazioni
""")

st.write("""
I dati utilizzati provengono da [Our World in Data](https://ourworldindata.org/coronavirus-source-data).
Questa applicazione permette di esplorare l'andamento dei contagi e delle vaccinazioni nei diversi paesi.
""")

# Carico i dati usando la funzione che ho definito
dati = carica_e_pulisci_dati()

# Estraggo la lista dei paesi unici (ordinati)
paesi = dati.select("location").unique().sort("location").to_series().to_list()

# Selectbox per scegliere il paese
paese_selezionato = st.selectbox(
    "Seleziona un paese:",
    paesi,
    index=paesi.index("Italy") if "Italy" in paesi else 0
)

# Filtro il dataframe sul paese selezionato
dati_filtrati = dati.filter(pl.col("location") == paese_selezionato)

# Slider per scegliere l'intervallo temporale
data_min = dati_filtrati.select("date").min()[0, 0]
data_max = dati_filtrati.select("date").max()[0, 0]

intervallo_date = st.slider(
    "Seleziona l'intervallo temporale:",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

# Applico il filtro
dati_filtrati = dati_filtrati.filter(
    (pl.col("date") >= intervallo_date[0]) & (pl.col("date") <= intervallo_date[1])
)

# Mostro i dati filtrati (tabella)
st.write("Dati selezionati:", dati_filtrati)

# Converto in dataframe pandas per il grafico Altair
dati_pd = dati_filtrati.to_pandas()

# Radio per scegliere la variabile da plottare
variabile = st.radio(
    "Cosa vuoi visualizzare?",
    options=["new_cases", "new_deaths", "people_vaccinated", "people_fully_vaccinated"],
    index=0
)

# Creo il grafico
grafico = crea_grafico_linee(dati_pd, variabile, paese_selezionato)

# Mostro il grafico
st.altair_chart(grafico, use_container_width=True)
