import json
  import boto3
  import logging
  import os

  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

  bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
  OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']

  def lambda_handler(event, context):
      try:
          logger.info(f"Received event: {json.dumps(event)}")

          summary = event.get("summary")
          if not summary:
              logger.error("Missing 'summary' input")
              raise ValueError("Missing 'summary' input")

          question = "What are the key points or practical uses mentioned?"
          prompt = f"\n\nHuman: Based on the following summary, answer this question: {question}\n\nSummary:\n{summary}\n\nAssistant:"

          response = bedrock_client.invoke_model(
              modelId='anthropic.claude-v2',
              body=json.dumps({
                  "prompt": prompt,
                  "max_tokens_to_sample": 200,
                  "temperature": 0.5,
                  "top_p": 1
              })
          )

          response_body = json.loads(response['body'].read())
          answer = response_body['completion'].strip()

          # Save answer to S3
          s3_client = boto3.client('s3')
          answer_key = f"qna/{context.aws_request_id}.txt"
          s3_client.put_object(
              Bucket=OUTPUT_BUCKET,
              Key=answer_key,
              Body=answer.encode('utf-8')
          )
          logger.info(f"Saved answer to {answer_key}")

          logger.info("Q&A generated successfully")

          return {
              'answer': answer
          }

      except Exception as e:
          logger.error(f"QnA Lambda error: {str(e)}")
          raise e