import json
import boto3
import logging
import os

# Configure clients
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def invoke_bedrock_claude(prompt, max_tokens=300):
    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-v2",
        body=json.dumps({
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": max_tokens,
            "temperature": 0.5,
        })
    )
    return json.loads(response["body"].read())["completion"]

def invoke_bedrock_titan(prompt):
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-text-lite-v1",
        body=json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 300,
                "temperature": 0.5
            }
        })
    )
    return json.loads(response["body"].read())["results"][0]["outputText"]

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        input_text = body.get("text", "")

        if not input_text.strip():
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Text input is required."})
            }

        logger.info("Starting summarization...")
        summary = invoke_bedrock_claude(f"Summarize the following in 100 words or less:\n{input_text}")
        
        logger.info("Starting simplification...")
        simplified = invoke_bedrock_titan(f"Rewrite this in simpler language:\n{summary}")
        
        logger.info("Starting Q&A...")
        question = "What are the key points or practical uses mentioned?"
        qa = invoke_bedrock_claude(f"Based on the following summary, answer: {question}\n\nSummary:\n{summary}")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "summary": summary.strip(),
                "simplified": simplified.strip(),
                "qa": qa.strip()
            })
        }

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
