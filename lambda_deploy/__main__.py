"""Main entry point for lambda_deploy package when run as a module."""
from lambda_deploy.create_lambda import deploy_lambda
from utils.aws_utils import get_aws_credentials
import boto3

if __name__ == '__main__':
    session = boto3.Session(**get_aws_credentials())
    lambda_client = session.client('lambda')
    lambda_name = 'sum_lambda'
    print("Deploying Lambda: ", lambda_name)
    deploy_lambda(lambda_client, lambda_name)
