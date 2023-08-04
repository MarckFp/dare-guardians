import os
import boto3
import botocore

def join_game(chat_id, message, first_name, last_name, username):
    print("Executed Join command")
    DYNAMO_TABLE = os.getenv('DYNAMO_TABLE')
    GAME_PASSWORD = os.getenv('GAME_PASSWORD')
    client = boto3.client('dynamodb')
    response = "Contraseña incorrecta, grupo no encontrado"
    if " " not in message:
        return "Porfavor introduce una contraseña o grupo"
    input_password = message.split(" ")[1]
    if input_password == GAME_PASSWORD:
        try:
            client.put_item(
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
                        'N': '0'
                    },
                    'score': {
                        'N': '0'
                    },
                    'group': {
                        'S': GAME_PASSWORD
                    }
                },
                ConditionExpression='attribute_not_exists(chat_id)'
            )
            response = f"¡Has sido registrado correctamente en el juego {first_name}! La semana que viene empezará tu primer reto, juega limpio y diviertete =)"
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
    return response
