import requests
import random

TOKEN = "8752521307:AAGT9Tq3dvkDKWOhWxbGkezM3YmnlxfeNrI"
CHAT_ID = "7049565102"

# Ligas grandes (IDs de TheSportsDB)
LEAGUES = [
    4328,  # Premier League
    4335,  # La Liga
    4332,  # Serie A
    4331,  # Bundesliga
    4334   # Ligue 1
]

partidos = []

# Obtener partidos próximos de varias ligas
for league_id in LEAGUES:
    try:
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={league_id}"
        r = requests.get(url, timeout=10)
        data = r.json()

        if data and data.get("events"):
            for p in data["events"]:
                partidos.append({
                    "local": p["strHomeTeam"],
                    "visita": p["strAwayTeam"]
                })
    except:
        pass

# Limitar a 10 partidos
partidos = partidos[:10]

mensaje = "⚽ ANALISIS DE PARTIDOS\n\n"

for p in partidos:

    local = p["local"]
    visita = p["visita"]

    # Probabilidades simples
    local_prob = random.randint(40, 65)
    visita_prob = random.randint(15, 35)
    empate_prob = 100 - (local_prob + visita_prob)

    mensaje += f"{local} vs {visita}\n"
    mensaje += f"{local} {local_prob}% de ganar\n"
    mensaje += f"{visita} {visita_prob}% de ganar\n"
    mensaje += f"Empate {empate_prob}%\n"
    mensaje += "Over 1.5 goles\n\n"

# Enviar mensaje a Telegram
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": mensaje
    }
)
