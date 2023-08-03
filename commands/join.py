import os
import boto3

def join_game(chat_id, message, first_name, last_name, username):
    DYNAMO_TABLE = os.getenv('DYNAMO_TABLE')
    GAME_PASSWORD = os.getenv('GAME_PASSWORD')
    client = boto3.client('dynamodb')
    #TODO: Add some type of rate limit by chat_id
    input_password = message.split(" ")[1]
    if input_password == GAME_PASSWORD:
        response = f"¡Has sido registrado correctamente en el juego {first_name}! La semana que viene empezará tu primer reto, juega limpio y diviertete =)"
        boto_response = client.put_item(
            TableName=DYNAMO_TABLE,
            Item={
                'chat_id': {
                    'S': str(chat_id)
                },
                'username': {
                    'S': username
                },
                'first_name': {
                    'S': first_name
                },
                'last_name': {
                    'S': last_name
                },
                'role': {
                    'S': 'None'
                },
                'attempts': {
                    'N': 0
                },
                'score': {
                    'N': 0
                },
                'group': {
                    'S': GAME_PASSWORD
                }
            }
        )
    else:
        response = "Contraseña incorrecta, grupo no encontrado"
    return response
