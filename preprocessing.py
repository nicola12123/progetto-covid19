import polars as pl

# Funzione per caricare e pulire i dati COVID-19
# Uso Polars come visto nei laboratori

def carica_e_pulisci_dati():
    df = pl.read_csv("data/owid-covid-data.csv")

    # Seleziono le colonne che mi interessano per il progetto
    df = df.select([
        "location",
        "date",
        "new_cases",
        "new_deaths",
        "people_vaccinated",
        "people_fully_vaccinated"
    ])

    # Converto la data in formato Date
    df = df.with_columns(
        pl.col("date").str.strptime(pl.Date, format="%Y-%m-%d"),
        pl.col("people_vaccinated").cast(pl.Float64, strict=False),
        pl.col("people_fully_vaccinated").cast(pl.Float64, strict=False)
    )

    # Rimuovo righe con valori null su location o date
    df = df.filter(pl.col("location").is_not_null() & pl.col("date").is_not_null())

    return df

# Test: stampo le prime 5 righe se eseguo direttamente il file
if __name__ == "__main__":
    df = carica_e_pulisci_dati()
    print(df.head())
