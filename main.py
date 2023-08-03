import os
import json
import requests
import boto3

TOKEN = os.getenv('TELEGRAM_TOKEN')
GAME_PASSWORD = os.getenv('GAME_PASSWORD')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
client = boto3.client('dynamodb')

def handler(event, context):
    try:
        data = json.loads(event["body"])
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]
        response = f"Porfavor escribe /start para empezar, {first_name}"

        if "/start" in message:
            response = f"Hola {first_name}! Para poder empezar a jugar a Dare Guardians escribe /subscribe seguido de un espacio y la constraseña"

        if "/subscribe" in message:
            #TODO: Add some type of rate limit by chat_id
            input_password = message.split(" ")[1]
            if input_password == GAME_PASSWORD:
                response = f"Has sido registrado correctamente en el juego {first_name}! La semana que viene empezará tu primer reto, juega limpio y diviertete =)"
                #TODO: Save User in the DynamoDB Table
            else:
                response = "Contraseña incorrecta"

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)
    except Exception as e:
        print(e)
        return {"statusCode": 500}
    return {"statusCode": 200}
