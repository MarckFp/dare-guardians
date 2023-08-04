import os
import boto3
import botocore

def join_game(chat_id, message, first_name):
    print("Executed Exit command")
    DYNAMO_TABLE = os.getenv('DYNAMO_TABLE')
    GAME_PASSWORD = os.getenv('GAME_PASSWORD')
    client = boto3.client('dynamodb')
    response = "No pudo eliminarse del juego"
    if " " not in message:
        return "Porfavor introduce una contraseña o grupo del cual eliminarse"
    input_password = message.split(" ")[1]
    if input_password == GAME_PASSWORD:
        try:
            client.delete_item(
                TableName=DYNAMO_TABLE,
                Key={
                    'chat_id': {
                        'S': str(chat_id)
                    },
                },
            )
            response = f"Has sido eliminado correctamente del juego {first_name} =("
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
    return response
