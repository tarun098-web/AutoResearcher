import json
  import boto3
  import os
  import logging
  from botocore.exceptions import ClientError

  # Configure logging
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

  # Environment variables
  OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
  MODEL_ID = 'anthropic.claude-v2'

  def lambda_handler(event, context):
      try:
          # Extract input text from Step Functions input
          input_text = event.get('input_text', '')
          if not input_text:
              logger.error("No input_text provided")
              raise Exception("Input text is required")

          logger.info(f"Processing text: {input_text[:50]}...")

          # Summarize text using Bedrock
          bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
          prompt = f"Summarize the following text in 100 words or less:\n{input_text}"
          body = json.dumps({
              "prompt": f"\n\nHuman: {prompt}\n\nAssistant: Summary: ",
              "max_tokens_to_sample": 200,
              "temperature": 0.5
          })
          response = bedrock_client.invoke_model(
              modelId=MODEL_ID,
              body=body
          )
          summary = json.loads(response['body'].read())['completion']
          logger.info("Summary generated")

          # Save summary to S3
          s3_client = boto3.client('s3')
          summary_key = f"summaries/{context.aws_request_id}.txt"
          s3_client.put_object(
              Bucket=OUTPUT_BUCKET,
              Key=summary_key,
              Body=summary.encode('utf-8')
          )
          logger.info(f"Saved summary to {summary_key}")

          # Return summary for Step Functions
          return summary

      except ClientError as e:
          logger.error(f"Error processing text: {e}")
          raise e
      except Exception as e:
          logger.error(f"Unexpected error: {e}")
          raise e