import os
import json
import requests
import boto3

TOKEN = os.getenv('TELEGRAM_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def handler(event, _context):
    DYNAMO_TABLE = os.getenv('DYNAMO_TABLE')
    GAME_PASSWORD = os.getenv('GAME_PASSWORD')
    client = boto3.client('dynamodb')
    try:
        response = client.query(
            TableName=DYNAMO_TABLE,
            IndexName='group-index',
            KeyConditionExpression='group = :group_pass',
            ExpressionAttributeValues={
                ":group_pass": {
                    'S': GAME_PASSWORD
                }
            },
        )
        print(response)
        #data = {"text": response.encode("utf8"), "chat_id": chat_id}
        #url = BASE_URL + "/sendMessage"
        #requests.post(url, data, timeout=15)
    except Exception as error:
        print(error)
