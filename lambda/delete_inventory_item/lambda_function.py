import boto3
import json
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        item_id = event['pathParameters']['id']

        # First find the item to get location_id
        response = table.scan(
            FilterExpression=Attr('item_id').eq(item_id)
        )

        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Item not found'})
            }

        item = items[0]

        # Delete using both PK and SK
        table.delete_item(
            Key={
                'item_id': item['item_id'],
                'location_id': item['location_id']
            }
        )

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Item deleted', 'item_id': item_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }