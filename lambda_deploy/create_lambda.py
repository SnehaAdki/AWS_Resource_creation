import boto3
from botocore.exceptions import ClientError
from utils.aws_utils import get_aws_credentials

LAMBDA_CONFIG = {
    'sum_lambda': {
        'function_name': 'sum_lambda',
        'handler': 'run_lambda_launcher.sum.lambda_handler'
    }
}

def get_lambda_function(lambda_client, function_name):
    try:
        func_data = lambda_client.get_function(FunctionName=function_name)
        print(func_data)
        print('Lambda function %s exists' % function_name)
        return func_data
    except ClientError as err:
        if err.response['Error']['Code'] == "ResourceNotFoundException":
            print('Lambda function %s does not exists' % function_name)
            return False
        raise


def deploy_lambda(lambda_client, lambda_name):
    func_data = LAMBDA_CONFIG[lambda_name]
    function_exist = get_lambda_function(lambda_client, func_data['function_name'])
    if not function_exist:
        print("Creation initiated.....")
        lambda_client.create_function(
            FunctionName = func_data['function_name'],
            Handler = func_data['handler'],
            Runtime = 'python3.8',
            Role = 'arn:aws:iam::381491950741:role/lambda_to_access_s3',
            Code = {
                'ZipFile': open('lambda_deploy/sum_lambda_zip.zip', 'rb').read()
            },
            Environment = {
                'Variables': {
                    'ENV': 'dev'
                }
            }
        )
        print("Lambda Creation completed.....")
    else:
        print("Lambda function already exists. Updating code.....")
        lambda_client.update_function_code(
            FunctionName = func_data['function_name'],
            ZipFile = open('lambda_deploy/sum_lambda_zip.zip', 'rb').read()
        )
        print("Lambda update completed.....")



if __name__ == '__main__':
    session = boto3.Session(**get_aws_credentials())
    lambda_client = session.client('lambda')
    lambda_name = 'sum_lambda'
    print("Deploying Lambda: ", lambda_name)
    deploy_lambda(lambda_client, lambda_name)