import polars as pl

# Questa funzione carica il dataset COVID-19 e applica una prima fase di pulizia.
# Ho usato Polars come indicato nei laboratori per il preprocessing dei dati.

def load_clean():
    # Carico il CSV con i dati COVID-19
    df = pl.read_csv("data/owid-covid-data.csv")

    # Seleziono solo le colonne che mi servono per l'analisi.
    # In questo caso: location (paese), data, nuovi casi, decessi, vaccinazioni.
    df = df.with_columns(
    pl.col("date").str.strptime(pl.Date, format="%Y-%m-%d"),
    pl.col("people_vaccinated").cast(pl.Float64, strict=False),
    pl.col("people_fully_vaccinated").cast(pl.Float64, strict=False)
)

    # Rimuovo eventuali righe con valori null su location o data
    # per evitare problemi successivi durante la visualizzazione
    df = df.filter(pl.col("location").is_not_null() & pl.col("date").is_not_null())

    return df

# Come nei laboratori, metto un test di verifica qui sotto:
# Se eseguo direttamente preprocessing.py, stampo 5 righe per controllare il risultato

if __name__ == "__main__":
    df = load_clean()
    print(df.head())

