import requests
import pandas as pd
import random

# -------------------------
# TELEGRAM
# -------------------------

TOKEN = "8752521307:AAGT9Tq3dvkDKWOhWxbGkezM3YmnlxfeNrI"
CHAT_ID = "7049565102"

# -------------------------
# LIGAS A ANALIZAR
# -------------------------

ligas = {
    "Premier League": "4328",
    "La Liga": "4335",
    "Bundesliga": "4331",
    "Ligue 1": "4334"
}

resultados = []

print("INICIANDO ANALISIS\n")

# -------------------------
# ANALISIS DE PARTIDOS
# -------------------------

for liga, id_liga in ligas.items():

    print(f"Analizando {liga}")

    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={id_liga}"

    r = requests.get(url)
    data = r.json()

    if data["events"]:

        for partido in data["events"]:

            local = partido["strHomeTeam"]
            visitante = partido["strAwayTeam"]
            fecha = partido["dateEvent"]

            prob_local = random.randint(40,65)
            prob_visita = random.randint(20,40)
            prob_empate = 100 - prob_local - prob_visita

            cuota_local = round(random.uniform(1.8,3.5),2)

            value = int(prob_local - (100/cuota_local))

            resultados.append({
                "Liga": liga,
                "Fecha": fecha,
                "Local": local,
                "Visitante": visitante,
                "Local %": prob_local,
                "Empate %": prob_empate,
                "Visitante %": prob_visita,
                "Cuota Local": cuota_local,
                "Value Local": value
            })

# -------------------------
# DATAFRAME
# -------------------------

df = pd.DataFrame(resultados)

print("\nPARTIDOS ANALIZADOS\n")
print(df)

# -------------------------
# GUARDAR EXCEL
# -------------------------

nombre_excel = "predicciones.xlsx"
df.to_excel(nombre_excel,index=False)

print(f"\nExcel guardado: {nombre_excel}")

# -------------------------
# TOP APUESTAS
# -------------------------

top10 = df.sort_values("Value Local",ascending=False).head(10)

print("\nTOP APUESTAS\n")
print(top10)

# -------------------------
# MENSAJE TELEGRAM
# -------------------------

mensaje = "⚽ TOP 10 APUESTAS DEL DIA\n\n"

for i,row in top10.iterrows():

    mensaje += f"{row['Local']} vs {row['Visitante']}\n"
    mensaje += f"{row['Local']} gana: {row['Local %']}%\n"
    mensaje += f"{row['Visitante']} gana: {row['Visitante %']}%\n"
    mensaje += "Over 1.5 goles\n\n"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url,data={
"chat_id":CHAT_ID,
"text":mensaje
})

print("\nMensaje enviado a Telegram")
