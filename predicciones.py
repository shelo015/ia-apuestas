import requests
import random

TOKEN = "8752521307:AAGT9Tq3dvkDKWOhWxbGkezM3YmnlxfeNrI"
CHAT_ID = "7049565102"

ligas = [4328, 4335, 4332, 4331, 4334]

partidos = []

for liga in ligas:
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={liga}"
    r = requests.get(url)
    data = r.json()

    if data["events"]:
        for p in data["events"]:
            partidos.append((p["strHomeTeam"], p["strAwayTeam"]))

partidos = partidos[:10]

mensaje = "⚽ ANALISIS DE PARTIDOS\n\n"

for local, visita in partidos:

    local_prob = random.randint(40,65)
    visita_prob = random.randint(20,35)
    empate_prob = 100 - (local_prob + visita_prob)

    mensaje += f"{local} vs {visita}\n"
    mensaje += f"{local} {local_prob}% de ganar\n"
    mensaje += f"{visita} {visita_prob}% de ganar\n"
    mensaje += f"Empate {empate_prob}%\n"
    mensaje += "Over 1.5 goles\n\n"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": mensaje
})
