import requests
import os
from datetime import datetime

API_KEY = os.environ["ODDS_API_KEY"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

sports = {
"Premier League":"soccer_epl",
"La Liga":"soccer_spain_la_liga",
"Serie A":"soccer_italy_serie_a",
"Bundesliga":"soccer_germany_bundesliga",
"Champions":"soccer_uefa_champs_league"
}

fuertes=[]
medios=[]
otros=[]

for liga,sport in sports.items():

    url=f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals,btts"

    r=requests.get(url)

    if r.status_code!=200:
        continue

    data=r.json()

    for match in data:

        home=match["home_team"]
        away=match["away_team"]

        fecha=datetime.fromisoformat(
        match["commence_time"].replace("Z","")
        ).strftime("%d-%m-%Y %H:%M")

        cuotas_home=[]
        cuotas_away=[]
        cuotas_over=[]
        cuotas_btts=[]

        try:
            for b in match["bookmakers"]:
                for m in b["markets"]:

                    if m["key"]=="h2h":
                        for o in m["outcomes"]:
                            if o["name"]==home:
                                cuotas_home.append(o["price"])
                            if o["name"]==away:
                                cuotas_away.append(o["price"])

                    if m["key"]=="totals":
                        for o in m["outcomes"]:
                            if o["name"]=="Over":
                                cuotas_over.append(o["price"])

                    if m["key"]=="btts":
                        for o in m["outcomes"]:
                            if o["name"]=="Yes":
                                cuotas_btts.append(o["price"])
        except:
            continue

        if len(cuotas_home)==0 or len(cuotas_away)==0:
            continue

        media_home=sum(cuotas_home)/len(cuotas_home)
        media_away=sum(cuotas_away)/len(cuotas_away)

        if media_home < media_away:
            favorito=home
            cuota_fav=media_home
        else:
            favorito=away
            cuota_fav=media_away

        prob=round(100/cuota_fav)

        recomendacion=None

        if len(cuotas_over)>0:
            media_over=sum(cuotas_over)/len(cuotas_over)
            if media_over<1.60:
                recomendacion="Habrá más de 2.5 goles"

        if recomendacion is None and len(cuotas_btts)>0:
            media_btts=sum(cuotas_btts)/len(cuotas_btts)
            if media_btts<1.70:
                recomendacion="Ambos equipos marcarán"

        if recomendacion is None:
            recomendacion=f"Gana {favorito}"

        info=(liga,home,away,fecha,favorito,prob,recomendacion)

        if cuota_fav<1.50:
            fuertes.append(info)

        elif cuota_fav<1.75:
            medios.append(info)

        else:
            otros.append(info)

mensaje="⚽ IA APUESTAS DEL DIA\n\n"

if len(fuertes)==0 and len(medios)==0 and len(otros)==0:

    mensaje+="⚠️ NO SE ENCONTRARON PARTIDOS CON DATOS HOY\n"

else:

    if fuertes:
        mensaje+="🔥 APUESTAS MUY FUERTES\n\n"
        for f in fuertes[:3]:
            mensaje+=f"{f[0]}\n{f[1]} vs {f[2]}\n📅 {f[3]}\nFavorito: {f[4]}\nProbabilidad ganar: {f[5]}%\nRecomendación: {f[6]}\n\n"

    if medios:
        mensaje+="⭐ APUESTAS NIVEL MEDIO\n\n"
        for m in medios[:3]:
            mensaje+=f"{m[0]}\n{m[1]} vs {m[2]}\n📅 {m[3]}\nFavorito: {m[4]}\nProbabilidad ganar: {m[5]}%\nRecomendación: {m[6]}\n\n"

    if not fuertes and not medios and otros:
        mensaje+="📊 PARTIDOS ANALIZADOS\n\n"
        for o in otros[:5]:
            mensaje+=f"{o[0]}\n{o[1]} vs {o[2]}\n📅 {o[3]}\nFavorito: {o[4]} {o[5]}%\n\n"

requests.post(
f"https://api.telegram.org/bot{TOKEN}/sendMessage",
data={"chat_id":CHAT_ID,"text":mensaje}
)

print("BOT EJECUTADO OK")
