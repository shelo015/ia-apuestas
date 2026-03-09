
import requests
import pandas as pd
from datetime import datetime
import random
import math

leagues={
"Premier League":4328,
"La Liga":4335,
"Bundesliga":4331,
"Ligue 1":4334
}

results=[]

def poisson_prob(lmbda,k):
    return (lmbda**k * math.exp(-lmbda))/math.factorial(k)

for league,league_id in leagues.items():

    print("Analizando",league)

    url=f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={league_id}"

    r=requests.get(url)
    data=r.json()

    if data["events"] is None:
        continue

    for game in data["events"]:

        home=game["strHomeTeam"]
        away=game["strAwayTeam"]
        date=game["dateEvent"]

        home_attack=random.uniform(1.2,2.0)
        away_attack=random.uniform(0.8,1.8)

        home_xg=home_attack
        away_xg=away_attack

        home_win=0
        draw=0
        away_win=0
        over25=0
        btts=0

        for i in range(6):
            for j in range(6):

                p=poisson_prob(home_xg,i)*poisson_prob(away_xg,j)

                if i>j:
                    home_win+=p
                elif i==j:
                    draw+=p
                else:
                    away_win+=p

                if i+j>=3:
                    over25+=p

                if i>0 and j>0:
                    btts+=p

        home_p=round(home_win*100)
        draw_p=round(draw*100)
        away_p=round(away_win*100)
        over_p=round(over25*100)
        btts_p=round(btts*100)

        # cuotas simuladas
        odd_home=round(random.uniform(1.8,3.5),2)
        odd_over=round(random.uniform(1.7,2.4),2)

        # probabilidad casa
        book_home=round(100/odd_home)

        value_home=home_p-book_home

        results.append({

            "Liga":league,
            "Fecha":date,
            "Local":home,
            "Visitante":away,

            "Local %":home_p,
            "Empate %":draw_p,
            "Visitante %":away_p,

            "Over2.5 %":over_p,
            "BTTS %":btts_p,

            "Cuota Local":odd_home,
            "Value Local":value_home

        })

df=pd.DataFrame(results)

print("\nPARTIDOS ANALIZADOS\n")

print(df)

today=datetime.today().strftime("%Y-%m-%d")

filename=f"predicciones_{today}.xlsx"

df.to_excel(filename,index=False)

print("\nExcel guardado:",filename)

best=df.sort_values("Value Local",ascending=False).head(3)

print("\nTOP 3 VALUE BETS\n")

print(best)

import requests

TOKEN = "8752521307:AAFvIi2jsCSAYZkD3emgigAcehefC0R9pQU"
CHAT_ID = "7049565102"

mensaje = "⚽ IA Apuestas ejecutada correctamente!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": 7049565102,
    "text": mensaje
})
