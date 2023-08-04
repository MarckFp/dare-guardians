import os
import json
import requests
from commands.join import join_game

TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def handler(event, _context):
    try:
        data = json.loads(event["body"])
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]
        last_name = data["message"]["chat"]["last_name"]
        username = data["message"]["chat"]["username"]
        response = f"Porfavor escribe /start para empezar, {first_name}"
        print(f"chat_id: {chat_id}")
        print(f"username: {username}")

        if "/start" in message:
            response = f"¡Hola {first_name}!\nEsto es Dare Guardians, un entretenido juego de retos con el que poder jugar con tus amigos. La idea del juego es simple, hay una serie de guardianes y un infiltrado, una vez a la semana un reto nuevo sale a la luz y se escoge un infiltrado al azar. El resto actuaran como guardianes. La idea es intentar completar el reto sin que nadie se de cuenta.\n\n/join - Para poder empezar a jugar a Dare Guardians escribe el comando seguido de un espacio y el ID de tu grupo\n/rules - Para entender mejor las reglas (WIP)\n/create - Para crear un grupo de guardianes (WIP)\n/exit - Para salir del juego (WIP)"

        if "/join" in message:
            response = join_game(chat_id, message, first_name, last_name, username)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data, timeout=15)
    except Exception as error:
        print(error)
        return {"statusCode": 500}
    return {"statusCode": 200}
