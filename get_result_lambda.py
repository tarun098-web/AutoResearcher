import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3', region_name='us-east-1')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'autoresearcher-output-tarun')

def read_s3_file(bucket, key):
    try:
        logger.info(f"Reading file: {key}")
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        logger.warning(f"Could not read {key}: {str(e)}")
        return None

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        filename = body.get("filename", "").strip()

        if not filename.endswith(".txt"):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Filename must end with .txt"})
            }

        base = os.path.splitext(os.path.basename(filename))[0]
        summary_key = f"summaries/{filename}.summary.txt"
        simplified_key = f"simplified/{filename}.summary.txt"
        qna_key = f"qna/{base}.qna.txt"

        summary = read_s3_file(OUTPUT_BUCKET, summary_key)
        simplified = read_s3_file(OUTPUT_BUCKET, simplified_key)
        qna = read_s3_file(OUTPUT_BUCKET, qna_key)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "summary": summary or "Not available yet.",
                "simplified": simplified or "Not available yet.",
                "qa": qna or "Not available yet."
            })
        }

    except Exception as e:
        logger.error(f"Error retrieving result: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
