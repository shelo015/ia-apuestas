import requests

TOKEN = "8752521307:AAGT9Tq3dvkDKWOhWxbGkezM3YmnlxfeNrI"
CHAT_ID = "7049565102"

mensaje = "PRUEBA NUEVA IA 123456"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": mensaje
})
