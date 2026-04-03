# AI Travel Planner – Serverless Workshop Repo

Welcome to the **AI Travel Planner** workshop! In this hands-on session, you'll build and deploy a fully serverless application powered by AWS services and Generative AI.

---

## What You'll Build

A travel itinerary web app where users can:
- Enter a destination, travel dates, and number of passengers
- Adjust an "Adventurousness" level (1–10)
- Generate a custom AI-powered travel itinerary via Amazon Bedrock

---

## Tech Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** AWS Lambda (Python 3.12) with LangChain + Amazon Bedrock (Claude v2)
- **Delivery:** CloudFront (serves the frontend from S3 and proxies API requests to Lambda)
- **Storage:** DynamoDB (provisioned for trip data)
- **Infrastructure:** Terraform (S3, CloudFront, Lambda Function URL, DynamoDB, IAM, CloudWatch)

---

## Project Structure

```
supercharged-webforms-demo/
├── frontend/                  # React app (Vite + TypeScript)
│   ├── src/
│   │   └── App.tsx            # Main component: form + itinerary display
│   ├── .env.example           # Environment variable template
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   └── lambda.py              # Lambda handler: calls Bedrock to generate itinerary
├── infrastructure/            # Terraform for all AWS resources
│   ├── main.tf                # Root module wiring
│   ├── variables.tf
│   ├── outputs.tf             # Outputs: cloudfront_url, function_url
│   ├── terraform.tfvars       # project_name, owner, region
│   └── modules/
│       ├── lambda/            # Lambda function + Function URL + IAM + CloudWatch
│       ├── static/            # S3 bucket + CloudFront distribution
│       └── dynamodb/          # DynamoDB table
└── README.md
```

---

## Workshop Setup

### 1. Prerequisites

- AWS Account with programmatic access (IAM user or role)
- Node.js 18+ and Yarn
- Terraform CLI
- AWS CLI configured (`aws configure`)

### 2. Clone This Repo

```bash
git clone https://github.com/your-org/supercharged-webforms-demo.git
cd supercharged-webforms-demo
```

### 3. Frontend: Local Dev

```bash
cd frontend
yarn install
yarn dev
```

The frontend reads `VITE_API_URL` from a `.env` file. Copy the example to get started:

```bash
cp .env.example .env
```

Update `VITE_API_URL` with your CloudFront URL after deploying infrastructure (step 4).

### 4. Deploy Infrastructure

```bash
cd infrastructure
terraform init
terraform apply
```

This provisions:
- **S3 bucket** to host the compiled frontend
- **CloudFront distribution** serving the frontend and proxying `/generate-itinerary` to the Lambda
- **Lambda function** (Python 3.12) with a Function URL
- **DynamoDB table** for trip data
- **IAM roles** with least-privilege policies (Bedrock, DynamoDB, CloudWatch)
- **CloudWatch log group** for Lambda logs

After `terraform apply`, Terraform outputs:

```
cloudfront_url = "https://<id>.cloudfront.net"
function_url   = "https://<id>.lambda-url.us-east-1.on.aws/"
```

Set `VITE_API_URL` in `frontend/.env` to the `cloudfront_url` value.

### 5. Build and Upload Frontend

```bash
cd frontend
yarn build
aws s3 sync dist/ s3://<your-bucket-name>/ --delete
```

---

## How It Works

### Frontend (`App.tsx`)

A single-page form that collects:
- Destination
- Start and end dates
- Number of passengers (tickets)
- Adventurousness level (slider 1–10)

On submit, it POSTs to `${VITE_API_URL}/generate-itinerary` and displays the AI-generated itinerary text.

### Backend (`lambda.py`)

Python Lambda that:
1. Parses the POST body (`destination`, `startDate`, `endDate`, `tickets`, `adventurousness`)
2. Builds a LangChain prompt and invokes Amazon Bedrock (`anthropic.claude-v2`)
3. Returns the generated itinerary text as a JSON response

### Infrastructure Flow

```
User Browser
    └── CloudFront
            ├── /* → S3 (React app)
            └── /generate-itinerary → Lambda Function URL
```

---

## Terraform Variables

Edit `infrastructure/terraform.tfvars` to set:

```hcl
project_name = "supercharged-webforms-demo"
owner        = "your-name"
region       = "us-east-1"   # optional, defaults to us-east-1
```

---

## Workshop Goals

By the end of this session, you'll:
- Understand serverless architecture fundamentals
- Deploy a GenAI-powered app using Amazon Bedrock
- Use CloudFront to unify static hosting and API delivery
- Leave with a real, working project in your AWS account
