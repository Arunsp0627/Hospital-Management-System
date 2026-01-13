import json
import os

# This example uses boto3 to send email using AWS SES.
# For local testing with serverless-offline, this function will just echo back the payload.
try:
    import boto3
    from botocore.exceptions import ClientError
except Exception:
    boto3 = None

SES_REGION = os.getenv("SES_REGION", "us-east-1")

def send_email_ses(to_address, subject, body_text, body_html=None, source=None):
    if boto3 is None:
        # boto3 not installed in local test environment — stub
        print("boto3 not available; email not sent. Payload:", to_address, subject)
        return {"status": "stubbed", "to": to_address}
    client = boto3.client("ses", region_name=SES_REGION)
    if source is None:
        source = os.getenv("SES_SOURCE_EMAIL")
    try:
        response = client.send_email(
            Source=source,
            Destination={"ToAddresses": [to_address]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body_text}, "Html": {"Data": body_html or body_text}},
            },
        )
    except ClientError as e:
        return {"error": str(e)}
    return response

def send_email(event, context):
    # HTTP event (serverless-offline) -> body contains JSON
    body = event.get("body")
    if isinstance(body, str):
        payload = json.loads(body) if body else {}
    else:
        payload = body or {}
    to_address = payload.get("to")
    subject = payload.get("subject", "No Subject")
    message = payload.get("message", "")
    # In local development, for quick test just echo
    result = send_email_ses(to_address, subject, message)
    return {
        "statusCode": 200,
        "body": json.dumps({"result": result}),
        "headers": {"Content-Type": "application/json"},
    }