# GenAI Flight App – Serverless Workshop Repo

Welcome to the **GenAI Flight App** workshop! In this hands-on session, you'll build and deploy a fully serverless application powered by AWS services and Generative AI.

---

## ✈️ What You'll Build
A simple flight booking web app where users can:
- Search for flights using a mock backend (AWS Lambda)
- “Purchase” tickets and generate a custom travel itinerary
- Adjust the "Adventurousness" level and number of passengers
- Deploy everything using CI/CD pipelines

---

## 🧱 Tech Stack
- **Frontend:** React + Vite + TypeScript
- **Backend:** AWS Lambda (Python)
- **API Gateway** (REST)
- **Bedrock** (for itinerary generation)
- **CI/CD:** GitHub Actions
- **Infrastructure:** Terraform (S3, Lambda, API Gateway, IAM)

---

## 🗂️ Project Structure
```
genai-flight-app/
├── frontend/                  # React app (Vite)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FlightSearchForm.tsx
│   │   │   ├── FlightResults.tsx
│   │   │   ├── ItineraryModal.tsx
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── searchLambda/         # Handles flight search (Python)
│   │   └── handler.py
│   └── itineraryLambda/      # Generates itineraries using Bedrock (Python)
│       └── handler.py
├── infrastructure/           # Terraform for AWS resources
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── .github/workflows/        # CI/CD pipeline
└── README.md
```

---

## 🚀 Workshop Setup

### 1. Prerequisites
- AWS Account with programmatic access (IAM user or role)
- Node.js 18+, npm or pnpm
- Terraform CLI
- GitHub account (to fork/clone)

### 2. Clone This Repo
```bash
git clone https://github.com/your-org/genai-flight-app.git
cd genai-flight-app
```

### 3. Frontend: Local Dev
```bash
cd frontend
npm install
npm run dev
```

### 4. Deploy Infrastructure
```bash
cd infrastructure/terraform
terraform init
terraform apply
```

This will provision:
- S3 bucket to host the frontend
- Two Lambda functions (search + itinerary)
- API Gateway with two endpoints
- IAM roles with least-privilege policies

### 5. CI/CD Pipeline
- Triggered on `push` or `pull_request`
- Runs tests, lint, security scans
- Deploys Lambdas & S3 bucket

> You'll connect your AWS credentials using GitHub Actions secrets:
> `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

---

## 🧪 Testing
- `npm run lint` – ESLint
- `npm run test` – Unit tests for React components
- Backend Lambdas include sample test files

---

## 🧠 Workshop Goals
By the end of this session, you'll:
- Understand serverless architecture fundamentals
- Deploy a GenAI-powered app using Bedrock
- Automate your pipeline using GitHub Actions
- Leave with a real, working project in your AWS account!

---

## 💻 Frontend Code Overview
The frontend is built with **React + Vite + TypeScript** and has three main parts:

### `FlightSearchForm.tsx`
- A form to select:
  - Departure city
  - Arrival city
  - Departure and return dates
  - Number of passengers
- Submits a request to `/search-flights` API endpoint

### `FlightResults.tsx`
- Displays a list of flight options returned by the backend
- Each option has a "Buy" button that triggers the itinerary modal

### `ItineraryModal.tsx`
- Pops up after "Buy" is clicked
- Asks user if they want an itinerary
- If yes:
  - Lets them select "Adventurousness" (slider 0–10)
  - Calls `/generate-itinerary` with all details
  - Displays AI-generated itinerary

### `App.tsx`
- Manages routes, state, and layout
- Passes props to all components

All API URLs should be injected via `.env` file (e.g., `VITE_API_BASE_URL`).

---

## 🔧 Backend Lambdas

### `searchLambda`
- Python-based AWS Lambda function
- Accepts POST body with:
  - origin
  - destination
  - departureDate
  - returnDate
  - passengers
- Returns mocked flight data (pre-defined list or generated objects)

### `itineraryLambda`
- Python-based Lambda connected to Amazon Bedrock
- Accepts POST body with:
  - destination
  - startDate
  - endDate
  - passengers
  - adventurousness (0–10)
- Calls Bedrock (e.g., Claude or Titan) with a prompt template
- Returns a JSON itinerary:
  ```json
  [
    {
      "day": 1,
      "title": "Historic City Tour",
      "description": "Explore famous landmarks and museums",
      "highlights": ["Old Town", "City Museum", "Central Market"]
    }
  ]
  ```

Next, we can scaffold the `searchLambda/handler.py` to return mocked flights.
