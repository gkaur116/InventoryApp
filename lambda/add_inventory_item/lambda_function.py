import boto3
import json
import os
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        item = {
            'item_id': str(uuid.uuid4()),
            'item_name': body['item_name'],
            'item_description': body.get('item_description', ''),
            'item_qty_on_hand': int(body['item_qty_on_hand']),
            'item_price': Decimal(str(body['item_price'])),
            'location_id': int(body['location_id'])
        }

        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item created', 'item_id': item['item_id']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }