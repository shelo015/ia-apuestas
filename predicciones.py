import requests

TOKEN = "8752521307:AAGT9Tq3dvkDKWOhWxbGkezM3YmnlxfeNrI"
CHAT_ID = "7049565102"

top10 = df.sort_values("Value Local", ascending=False).head(10)

mensaje = "⚽ TOP APUESTAS DEL DIA\n\n"

for i,row in top10.iterrows():

    mensaje += f"{row['Local']} vs {row['Visitante']}\n"
    mensaje += f"Prob Local: {row['Local %']}%\n"
    mensaje += f"Prob Visitante: {row['Visitante %']}%\n"
    mensaje += f"Over 1.5 goles\n\n"

url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url,data={
"chat_id":CHAT_ID,
"text":mensaje
})
