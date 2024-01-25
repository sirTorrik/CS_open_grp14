import json
import boto3
from email.message import EmailMessage
import ssl
import smtplib
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "grp14/email"  
    region_name = "eu-central-1"     

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        raise e
    else:
        # Decrypts secret and returns the secret value
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            return secret
        else:
            print("Error: Secret not found.")
            return "Error: Secret not found."
            
secret = get_secret()
password = secret['password']

def lambda_handler(event, context):
    try:
        # Check if 'body' exists in the event, indicating API Gateway invocation
        if 'body' in event:
            data = json.loads(event['body'])  
        else:
            data = event 

    
        port = data.get('port')
        email_address = data.get('email')
        ip_address = '44.198.22.227'  

        
        if not port or not email_address:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid request. Missing port or email information.'})}

        
        subject = 'Port Information'
        body = f'Selected port: {port}\nHost IP address: {ip_address}'
        send_email(subject, body, email_address)

        return {'statusCode': 200, 'body': json.dumps({'message': 'Port information received and email sent successfully'})}

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': f'Error: {str(e)}'})}


def send_email(subject, body, recipient):
    em = EmailMessage()
    em['From'] = 'group14jda@gmail.com'
    em['To'] = recipient
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login('group14jda@gmail.com', password)  
        smtp.sendmail('group14jda@gmail.com', recipient, em.as_string())
