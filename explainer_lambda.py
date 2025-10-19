import json
import boto3
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
MODEL_ID = 'amazon.titan-text-lite-v1'

def lambda_handler(event, context):
    try:
        # Extract summary from Step Function input
        summary = event.get('summary', '')
        if not summary:
            raise ValueError("Missing 'summary' in input")

        # Simplify using Bedrock
        bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        prompt = f"Rewrite the following text in simple language:\n{summary}"
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5
            }
        })

        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            body=body
        )

        simplified_text = json.loads(response['body'].read())['results'][0]['outputText']
        logger.info("Simplified text generated successfully")

        # Return both summary and simplified version
        return {
            'statusCode': 200,
            'summary': summary,
            'simplified': simplified_text
        }

    except Exception as e:
        logger.error(f"Error simplifying summary: {str(e)}")
        return {
            'statusCode': 500,
            'error': str(e)
        }
