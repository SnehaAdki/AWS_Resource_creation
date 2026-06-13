from Tables.dynamo_table import USERS, ORDERS, PRODUCTS
import boto3
from botocore.exceptions import ClientError
from utils.aws_utils import get_aws_credentials
session = boto3.Session(**get_aws_credentials()) 
DYNAMO_CLIENT = session.client('dynamodb')

TABLE_CONFIGURATIONS = {
    USERS :{
     "TableName":USERS,
     "KeySchema": [{'AttributeName': 'customer_id', 'KeyType': 'HASH'}],
     "AttributeDefinitions":[{
         'AttributeName': 'customer_id','AttributeType':'S'
     }]
    },
    ORDERS :{
     "TableName":ORDERS,
     "KeySchema": [{'AttributeName': 'order_id', 'KeyType': 'HASH'}],
     "AttributeDefinitions":[{
         'AttributeName': 'order_id','AttributeType':'S'
     }]
    },
    PRODUCTS :{
     "TableName":PRODUCTS,
     "KeySchema": [{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
     "AttributeDefinitions":[{
         'AttributeName': 'product_id','AttributeType':'S'
     }]
    }
}



def create_table_dynamod(table_details):
    try:
        print(f"Creating Users table {table_details['TableName']}....")
        DYNAMO_CLIENT.create_table(
         TableName=table_details['TableName'],
         KeySchema=table_details['KeySchema'],
         AttributeDefinitions=table_details['AttributeDefinitions'],
         BillingMode='PAY_PER_REQUEST',
        )
        print("Table Creation Successfully")
    except ClientError as err:
        print(f"Exception occured {err}")
        raise Exception(f"Failed at table creation {table_details['TableName']}")

if __name__ == '__main__':
    TABLE_NAME = [USERS, ORDERS, PRODUCTS]
    for each_table in TABLE_NAME:
        create_table_dynamod(each_table)