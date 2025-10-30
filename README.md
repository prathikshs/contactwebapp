# Automated Deployment of Email Contact Form using DevOps Tools

## Project Overview

This project implements an automated deployment pipeline for a simple email contact form application using modern DevOps practices. The application consists of a Flask-based backend API that handles contact form submissions and sends emails via SMTP, with a basic HTML frontend for user interaction.

The DevOps pipeline leverages GitHub Actions/Jenkins for CI/CD, Docker for containerization, Terraform for infrastructure provisioning on Azure, Ansible for configuration management, and Kubernetes for orchestration.

## Architecture

### DevOps Pipeline Architecture Diagram

```
Developer
    |
    v
GitHub Repository
    |
    v
CI/CD Tool (Jenkins/GitHub Actions)
    |           |
    |           v
    |       Docker Build
    |           |
    |           v
    |       Azure Container Registry (ACR)
    |           |
    |           v
    |       Terraform Provisioning
    |           |
    |           v
    |       Azure Kubernetes Service (AKS)
    |           |
    |           v
    |       Ansible Configuration
    |           |
    |           v
    v
User
```

### Infrastructure Diagram

```
User Browser
    |
    v
Load Balancer (Public IP)
    |
    v
Azure Kubernetes Service (AKS) Cluster
    |           |
    |           v
    |       Application Pods (Contact Form)
    |           |
    |           v
    |       Email Service Integration
    |
    v
Azure Container Registry (ACR)
    |
    v
Container Images
```

## Project Structure

```
contact-form-project/
├── .github/
│   ├── workflows/
│   │   ├── ci-cd.yml
│   │   └── deploy.yml
├── ansible/
│   ├── playbooks/
│   │   ├── deploy.yml
│   │   └── configure.yml
│   ├── roles/
│   │   ├── webapp/
│   │   │   ├── tasks/
│   │   │   │   └── main.yml
│   │   │   ├── templates/
│   │   │   │   └── nginx.conf.j2
│   │   │   └── vars/
│   │       └── main.yml
│   │   └── email-service/
│   │       ├── tasks/
│   │       │   └── main.yml
│   │       └── vars/
│   │           └── main.yml
│   └── inventory/
│       ├── staging
│       └── production
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── modules/
│   │   │   ├── aks/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── acr/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   └── networking/
│   │   │       ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   └── environments/
│   │       ├── staging/
│   │       │   ├── main.tf
│   │       │   └── terraform.tfvars
│   │       └── production/
│   │           ├── main.tf
│   │           └── terraform.tfvars
├── src/
│   ├── backend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── config.py
│   │   ├── models/
│   │   │   └── contact.py
│   │   ├── routes/
│   │   │   └── contact.py
│   │   ├── services/
│   │   │   └── email_service.py
│   │   └── tests/
│   │       ├── test_contact.py
│   │       └── test_email.py
│   ├── frontend/
│   │   ├── public/
│   │   │   ├── index.html
│   │   │   └── favicon.ico
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── ContactForm.js
│   │   │   │   └── Header.js
│   │   │   ├── pages/
│   │   │   │   └── Home.js
│   │   │   ├── App.js
│   │   │   ├── index.js
│   │   │   └── styles/
│   │   │       └── main.css
│   │   ├── package.json
│   │   └── tests/
│   │       ├── ContactForm.test.js
│   │       └── App.test.js
│   └── shared/
│       ├── utils/
│       │   └── validation.js
│       └── config/
│           └── constants.js
├── scripts/
│   ├── build.sh
│   ├── deploy.sh
│   └── test.sh
├── docs/
│   ├── README.md
│   ├── architecture.md
│   ├── deployment-guide.md
│   └── api-docs.md
├── .gitignore
├── Jenkinsfile
├── docker-compose.override.yml
├── Makefile
└── requirements-dev.txt
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Azure CLI
- Terraform
- Ansible
- kubectl

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd contact-form-project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your SMTP credentials
   ```

5. Run the application locally:
   ```bash
   python app/app.py
   ```

6. Access the application at `http://localhost:5000`

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t contact-form .
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up
   ```

## Deployment Steps

### 1. Infrastructure Provisioning

1. Navigate to the terraform directory:
   ```bash
   cd terraform
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Plan the deployment:
   ```bash
   terraform plan -var-file=staging.tfvars
   ```

4. Apply the changes:
   ```bash
   terraform apply -var-file=staging.tfvars
   ```

### 2. Application Deployment

1. Build and push Docker image to ACR:
   ```bash
   az acr build --registry <acr-name> --image contact-form:v1 .
   ```

2. Deploy to AKS:
   ```bash
   kubectl apply -f kubernetes/
   ```

### 3. Configuration Management

1. Run Ansible playbook:
   ```bash
   ansible-playbook -i ansible/inventory/staging ansible/deploy.yml
   ```

## Usage Guide

### Submitting a Contact Form

1. Open the application in your web browser
2. Fill in the contact form fields (name, email, message)
3. Click "Submit"
4. The form data will be emailed to the configured recipient

### API Endpoints

- `GET /`: Returns the contact form HTML page
- `POST /contact`: Accepts JSON payload with contact form data and sends email

Example API request:
```bash
curl -X POST http://localhost:5000/contact \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "message": "Hello!"}'
```

## Configuration

The application uses the following environment variables for SMTP configuration:

- `SMTP_SERVER`: SMTP server hostname (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (default: 587)
- `SMTP_USERNAME`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `RECIPIENT_EMAIL`: Email address to receive contact form submissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
