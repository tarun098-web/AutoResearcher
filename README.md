# AutoResearcher: A Serverless AI Agent Ecosystem for Research Automation

A lightweight, serverless application built on AWS for generating research summaries, simplified explanations, and Q&A outputs from user-provided text.

## Features
- Modular AWS Lambda functions (summarizer, explainer, Q&A).
- Integrates Amazon Bedrock models (Claude v2, Titan Text Lite).
- Orchestrated with AWS Step Functions.
- Frontend hosted on S3 with API Gateway.

## Setup
1. Install dependencies: `npm install`
2. Deploy with Serverless Framework: `sls deploy`
3. Configure AWS credentials (not included in repo).

## Report
See [24141615_Dande_Tarun.pdf](24141615_Dande_Tarun.pdf) for full details.

## Architecture
<image-card alt="Architecture Diagram" src="architecture_diagram.png" >![Uploading image.png…]()
</image-card>  # Upload the architecture image from the PDF if possible
