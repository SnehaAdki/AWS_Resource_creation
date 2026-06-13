from Tables.dynamo_table import USERS, ORDERS, PRODUCTS
import boto3
from botocore.exceptions import ClientError
from utils.aws_utils import get_aws_credentials

session = boto3.Session(**get_aws_credentials())
DYNAMO_CLIENT = session.client('dynamodb')

TABLE_CONFIGURATIONS = {
    USERS: {
        "TableName": USERS,
        "KeySchema": [{"AttributeName": "customer_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "customer_id", "AttributeType": "S"}],
    },
    ORDERS: {
        "TableName": ORDERS,
        "KeySchema": [{"AttributeName": "order_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "order_id", "AttributeType": "S"}],
    },
    PRODUCTS: {
        "TableName": PRODUCTS,
        "KeySchema": [{"AttributeName": "product_id", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "product_id", "AttributeType": "S"}],
    },
}


def table_exists(table_name):
    try:
        DYNAMO_CLIENT.describe_table(TableName=table_name)
        return True
    except ClientError as err:
        error_code = err.response.get("Error", {}).get("Code")
        if error_code == "ResourceNotFoundException":
            return False


def delete_table(table_name):
    print(f"Table already exists: {table_name}. Deleting for re-creation...")
    DYNAMO_CLIENT.delete_table(TableName=table_name)
    waiter = DYNAMO_CLIENT.get_waiter("table_not_exists")
    waiter.wait(TableName=table_name)
    print(f"Deleted existing table {table_name}.")


def create_table_dynamod(table_details):
    table_name = table_details["TableName"]

    if table_exists(table_name):
        delete_table(table_name)
    try:
        print(f"Creating table {table_name}....")
        DYNAMO_CLIENT.create_table(
            TableName=table_details["TableName"],
            KeySchema=table_details["KeySchema"],
            AttributeDefinitions=table_details["AttributeDefinitions"],
            BillingMode="PAY_PER_REQUEST",
        )
        print("Table creation succeeded.")
    except ClientError as err:
        print(f"Exception occured {err}")
        raise Exception(f"Failed at table creation {table_name}")


if __name__ == "__main__":
    TABLE_NAME = [USERS, ORDERS, PRODUCTS]
    for each_table in TABLE_NAME:
        create_table_dynamod(TABLE_CONFIGURATIONS[each_table])