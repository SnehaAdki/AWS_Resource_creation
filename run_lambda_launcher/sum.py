
def lambda_handler(event, context):
    # Extract the numbers from the event
    num1 = event.get('num1', 0)
    num2 = event.get('num2', 0)
    
    # Calculate the sum
    result = num1 + num2
    print("Welcome... via IAC")
    print("number1: ", num1)
    print("number2: ", num2)
    print("result: ", result)
    # Return the result
    return {
        'statusCode': 200,
        'body': {
            'result': result
        }
    }

if __name__ == '__main__':
    # Test the lambda handler with a sample event
    test_event = {
        'num1': 5,
        'num2': 10
    }
    print(lambda_handler(test_event, None))
