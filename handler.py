import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def send_email(event, context):
    try:
        
        data = json.loads(event['body'])
        
        required_fields = ['receiver_email', 'subject', 'body_text']
        for field in required_fields:
            if field not in data:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Missing required field: {field}"})
                }

       
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Sender', os.environ['SMTP_USER']))
        msg['To'] = data['receiver_email']
        msg['Subject'] = data['subject']
        msg.attach(MIMEText(data['body_text'], 'plain'))

        
        with smtplib.SMTP(os.environ['SMTP_HOST'], int(os.environ['SMTP_PORT'])) as server:
            server.starttls()
            server.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
            server.send_message(msg)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format in request body"})
        }
    except smtplib.SMTPAuthenticationError:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "SMTP authentication failed"})
        }
    except smtplib.SMTPException as e:
        return {
            "statusCode": 502,
            "body": json.dumps({"error": f"SMTP error occurred: {str(e)}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal server error: {str(e)}"})
        }