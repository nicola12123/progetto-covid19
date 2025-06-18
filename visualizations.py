import altair as alt

# Funzione che crea un grafico a linee con Altair
# df: dataframe pandas
# colonna_y: la variabile che voglio rappresentare
# nome_paese: nome del paese selezionato

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
