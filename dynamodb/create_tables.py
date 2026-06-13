from Tables.dynamo_table import USERS, ORDERS, PRODUCTS
import boto3
from utils.aws_utils import get_aws_credentials

session = boto3.Session(**get_aws_credentials()) 
DYNAMO_CLIENT = session.client('dynamodb')

def create_table_dynamod(USERS):
    print("Creating Users table ....")
    DYNAMO_CLIENT.create_table(
     TableName=USERS   
    )

if __name__ == '__main__':
    create_table_dynamod(USERS)