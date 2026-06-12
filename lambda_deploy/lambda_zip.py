import zipfile
import os

def create_lambda_zip():
    """Create the ZIP file for Lambda deployment"""
    with zipfile.ZipFile('lambda_deploy/sum_lambda_zip.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add __init__.py to make it a package
        zipf.writestr('run_lambda_launcher/__init__.py', '')
        # Add your Lambda handler code
        zipf.write('run_lambda_launcher/sum.py', arcname='run_lambda_launcher/sum.py')
    print("ZIP file created: lambda_deploy/sum_lambda_zip.zip")
    print("Contents:")
    print("  - run_lambda_launcher/")
    print("    - __init__.py")
    print("    - sum.py")


if __name__ == '__main__':
    create_lambda_zip()