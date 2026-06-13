import boto3
import os
from utils.aws_utils import get_aws_credentials
from Tables.dynamo_table import USERS, ORDERS, PRODUCTS

def connect_ddb(table_name):
    """
    Establish the connection with the dynamodb table and return the table object.

    Parameter:
        table_name (string): name of the DynamoDB table
    Returns:
        table: DynamoDB table object
    """
    session = boto3.Session(**get_aws_credentials())
    _client = session.resource('dynamodb')
    # pylint: disable=no-member
    return _client.Table(table_name)

def insert_into_dynamo(table_name, item):
    try:
        table = connect_ddb(table_name)
        table.put_item(Item=item)
    except Exception as err:
        print(f"Exception occured {err}")
        raise Exception(f"Failed to insert item into DynamoDB: {err}")

def update_item_in_dynamo(table_name, key, update_expression, expression_values):
    try:
        table = connect_ddb(table_name)
        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
    except Exception as err:
        print(f"Exception occured {err}")
        raise Exception(f"Failed to update item in DynamoDB: {err}")

def delete_item_from_dynamo(table_name, key):
    try:
        table = connect_ddb(table_name)
        table.delete_item(Key=key)
    except Exception as err:
        print(f"Exception occured {err}")
        raise Exception(f"Failed to delete item from DynamoDB: {err}")

if __name__ == "__main__":
    items = [
        {
            "customer_id": "123",
            "name": "John Doe",
            "email": "john.doe@example.com"
        },
        {
            "customer_id": "122",
            "name": "Sneha Adki",
            "email": "sneha.adki@example.com"
        },
        {
            "customer_id": "125",
            "name": "VK",
            "email": "vk@example.com"
        },
    ]
    
    for each_item in items:
        insert_into_dynamo(USERS, each_item)

    update_item_in_dynamo(USERS, {"customer_id": "122"}, 
                "SET email = :e", {":e": "johnsmith@example.com"})
    delete_item_from_dynamo(USERS, {"customer_id": "123"})