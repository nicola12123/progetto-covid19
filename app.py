import streamlit as st
import polars as pl
from preprocessing import load_and_clean_data

# Titolo e descrizione della pagina
st.write("""
# Andamento COVID-19: contagi e vaccinazioni
""")

st.write("""
I dati sono presi da [Our World in Data](https://ourworldindata.org/coronavirus-source-data).
Questo grafico permette di vedere come sono cambiati i contagi e i tassi di vaccinazione nei diversi paesi.
""")

# Carico i dati già puliti (funzione fatta in preprocessing.py)
df = load_and_clean_data()

# Seleziono tutti i paesi unici disponibili
countries = df.select("location").unique().sort("location").to_series().to_list()

# Selettore per il paese
selected_country = st.selectbox(
    "Seleziona un paese:",
    countries,
    index=countries.index("Italy") if "Italy" in countries else 0
)

# Filtro il dataframe sul paese selezionato
df_selected = df.filter(pl.col("location") == selected_country)

# Slider per selezionare un range temporale
min_date = df_selected.select("date").min()[0, 0]
max_date = df_selected.select("date").max()[0, 0]

date_range = st.slider(
    "Seleziona l'intervallo temporale:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Applico il filtro sul range temporale
df_selected = df_selected.filter(
    (pl.col("date") >= date_range[0]) & (pl.col("date") <= date_range[1])
)

# Mostro il dataframe filtrato
st.write("Dati filtrati:", df_selected)

# Per ora mostro anche un grafico a linee semplice (contagi nel tempo)
# Nella prossima versione lo faremo bello con Altair!

st.line_chart(
    df_selected.to_pandas(),
    x="date",
    y="new_cases"
)
