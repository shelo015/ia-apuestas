print("PRUEBA NUEVA IA FUNCIONANDO")
import requests

TOKEN = "8752521307:AAGT9Tq3dvkDKWOhWxbGkezM3YmnlxfeNrI"
CHAT_ID = "7049565102"

mensaje = """
⚽ PRUEBA IA

Liverpool vs Tottenham
Liverpool 60% de ganar
Tottenham 30% de ganar
Empate 10%
Over 1.5 goles
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": mensaje
})
