# End-to-End Deployment Simulation Guide for Email Contact Form Application

This guide simulates the complete deployment process for the email contact form application using DevOps tools. All commands are documented with their purposes and expected outcomes, without actual execution.

## 1. Infrastructure Provisioning Simulation

### Terraform Initialization and Planning

**Command:** `terraform init`  
**Purpose:** Initialize the Terraform working directory, download required providers (Azure provider), and set up the backend for state management.  
**Expected Outcome:** Terraform downloads the azurerm provider (~3.0), creates .terraform directory, and confirms initialization complete.

**Command:** `terraform plan -var-file=production.tfvars`  
**Purpose:** Generate an execution plan showing what resources will be created, modified, or destroyed.  
**Expected Outcome:** Detailed plan output showing:
- Creation of Azure Resource Group
- Creation of Azure Container Registry (ACR)
- Creation of Azure Kubernetes Service (AKS) cluster with default node pool
- Estimated costs and resource configurations

### Terraform Application

**Command:** `terraform apply -var-file=production.tfvars`  
**Purpose:** Execute the planned infrastructure provisioning on Azure.  
**Expected Outcome:**
- Resource Group created with specified name and location
- ACR created with Basic SKU and admin access enabled
- AKS cluster created with specified node count and VM size
- Output values displayed: resource group name, ACR login server, admin credentials (sensitive), AKS cluster name, kube config (sensitive), and FQDN

**Command:** `terraform output`  
**Purpose:** Display all output values from the deployed infrastructure.  
**Expected Outcome:** Structured output showing all infrastructure endpoints and credentials needed for subsequent deployment steps.

## 2. Container Registry Setup Simulation

### Azure CLI Authentication

**Command:** `az login`  
**Purpose:** Authenticate with Azure CLI using interactive browser login or service principal.  
**Expected Outcome:** Successful authentication confirmation with account details and subscription information.

### ACR Login

**Command:** `az acr login --name myacr`  
**Purpose:** Log in to the Azure Container Registry to enable Docker push operations.  
**Expected Outcome:** Login successful message, Docker client configured to authenticate with ACR.

### Docker Build

**Command:** `docker build -t myacr.azurecr.io/contact-app:v1.0 .`  
**Purpose:** Build the Docker image for the contact form application using the provided Dockerfile.  
**Expected Outcome:** Docker build process completes successfully, creating an image tagged with the ACR registry URL and version.

### Docker Push to ACR

**Command:** `docker push myacr.azurecr.io/contact-app:v1.0`  
**Purpose:** Push the built Docker image to Azure Container Registry.  
**Expected Outcome:** Image layers uploaded successfully, final confirmation of push completion with image digest.

### Verify Image in ACR

**Command:** `az acr repository list --name myacr --output table`  
**Purpose:** List repositories in the ACR to confirm the image was pushed successfully.  
**Expected Outcome:** Table output showing "contact-app" repository in the list.

**Command:** `az acr repository show-tags --name myacr --repository contact-app --output table`  
**Purpose:** Show available tags for the contact-app repository.  
**Expected Outcome:** Table output displaying "v1.0" tag and other metadata like creation time and size.

## 3. Kubernetes Deployment Simulation

### Configure kubectl for AKS

**Command:** `az aks get-credentials --resource-group myResourceGroup --name myAKSCluster`  
**Purpose:** Download and merge kubeconfig for the AKS cluster to enable kubectl commands.  
**Expected Outcome:** Merged kubeconfig into ~/.kube/config, kubectl context set to the AKS cluster.

### Verify Cluster Connection

**Command:** `kubectl cluster-info`  
**Purpose:** Verify connection to the AKS cluster and display cluster information.  
**Expected Outcome:** Cluster endpoint URL, Kubernetes version, and connection status confirmation.

### Deploy Application

**Command:** `kubectl apply -f kubernetes/deployment.yaml`  
**Purpose:** Create the Kubernetes deployment for the contact form application.  
**Expected Outcome:** Deployment "contact-app" created, with 1 replica pod specification applied.

**Command:** `kubectl apply -f kubernetes/service.yaml`  
**Purpose:** Create the LoadBalancer service to expose the application externally.  
**Expected Outcome:** Service "contact-app-service" created with LoadBalancer type and external IP allocation initiated.

### Monitor Deployment

**Command:** `kubectl get pods`  
**Purpose:** Check the status of deployed pods.  
**Expected Outcome:** Pod listing showing contact-app pod in Running state, ready status 1/1.

**Command:** `kubectl get services`  
**Purpose:** Check the status of services and obtain the external IP.  
**Expected Outcome:** Service listing showing contact-app-service with EXTERNAL-IP (initially pending, then assigned public IP).

**Command:** `kubectl logs -l app=contact-app`  
**Purpose:** View application logs to verify startup and health.  
**Expected Outcome:** Flask application startup logs showing successful initialization on port 5000.

## 4. CI/CD Pipeline Simulation

### Jenkins Pipeline Execution Flow

**Stage 1: Build**  
**Simulated Commands:**
- `docker.build('myacr.azurecr.io/myapp:${BUILD_NUMBER}', '.')`  
**Purpose:** Build Docker image with Jenkins build number as tag.  
**Expected Outcome:** Docker image built successfully with unique tag based on build number.

**Stage 2: Push to ACR**  
**Simulated Commands:**
- `docker.withRegistry("https://myacr.azurecr.io", "acr-credentials")`  
- `docker.image('myacr.azurecr.io/myapp:${BUILD_NUMBER}').push()`  
**Purpose:** Authenticate with ACR and push the built image.  
**Expected Outcome:** Image pushed to ACR with build-specific tag.

**Stage 3: Deploy to AKS**  
**Simulated Commands:**
- `withEnv(["KUBECONFIG=${KUBE_CONFIG}"])`  
- `sh 'ansible-playbook ansible/deploy.yml'`  
**Purpose:** Execute Ansible playbook to deploy to Kubernetes using stored kubeconfig.  
**Expected Outcome:** Ansible playbook runs successfully, applying Kubernetes manifests.

**Post-build Actions:**
- `docker system prune -f` (cleanup)  
**Purpose:** Remove unused Docker images and containers to free disk space.  
**Expected Outcome:** Docker system cleaned, disk space reclaimed.

### Pipeline Success/Failure Handling

**On Success:** Pipeline completes with "Pipeline completed successfully" message.  
**On Failure:** Pipeline fails with "Pipeline failed. Check logs for details" and stops execution.

## 5. Validation Simulation

### Infrastructure Validation

**Command:** `az resource list --resource-group myResourceGroup --output table`  
**Purpose:** List all resources in the resource group to verify provisioning.  
**Expected Outcome:** Table showing Resource Group, ACR, and AKS cluster resources with Succeeded provisioning state.

**Command:** `az acr show --name myacr --output table`  
**Purpose:** Verify ACR configuration and status.  
**Expected Outcome:** ACR details showing Basic SKU, admin enabled, and LoginServer URL.

**Command:** `az aks show --name myAKSCluster --resource-group myResourceGroup --output table`  
**Purpose:** Verify AKS cluster status and configuration.  
**Expected Outcome:** AKS cluster details showing Succeeded provisioning state and FQDN.

### Application Validation

**Command:** `kubectl get deployments`  
**Purpose:** Verify deployment status and replica count.  
**Expected Outcome:** contact-app deployment showing 1/1 ready replicas.

**Command:** `kubectl get services`  
**Purpose:** Verify service creation and external IP assignment.  
**Expected Outcome:** contact-app-service showing LoadBalancer type with assigned EXTERNAL-IP.

**Command:** `kubectl describe service contact-app-service`  
**Purpose:** Get detailed service information including endpoints.  
**Expected Outcome:** Service description showing LoadBalancer ingress IP and port mappings.

### Health Check Validation

**Command:** `curl -I http://<EXTERNAL-IP>`  
**Purpose:** Test HTTP connectivity to the application.  
**Expected Outcome:** HTTP 200 OK response with server headers.

**Command:** `kubectl exec -it <pod-name> -- curl http://localhost:5000`  
**Purpose:** Test internal application health from within the pod.  
**Expected Outcome:** Successful response from Flask application on port 5000.

## 6. Access and Testing Simulation

### Application Access

**Method 1: Direct IP Access**  
**URL:** `http://<EXTERNAL-IP>`  
**Purpose:** Access the contact form application via the LoadBalancer public IP.  
**Expected Outcome:** Contact form HTML page loads in browser.

**Method 2: DNS Access (if configured)**  
**URL:** `http://contact-app.example.com`  
**Purpose:** Access via custom domain (requires DNS configuration).  
**Expected Outcome:** Contact form loads with custom domain.

### API Testing

**Command:** `curl -X GET http://<EXTERNAL-IP>/`  
**Purpose:** Test the root endpoint returning the HTML form.  
**Expected Outcome:** HTML content of the contact form page.

**Command:** `curl -X POST http://<EXTERNAL-IP>/contact -H "Content-Type: application/json" -d '{"name":"Test User","email":"test@example.com","message":"Test message"}'`  
**Purpose:** Test the contact form submission endpoint.  
**Expected Outcome:** JSON response indicating successful email sending.

### Load Testing Simulation

**Command:** `ab -n 100 -c 10 http://<EXTERNAL-IP>/`  
**Purpose:** Perform basic load testing with Apache Bench.  
**Expected Outcome:** Performance metrics showing requests per second, response times, and success rate.

### Monitoring and Logs

**Command:** `kubectl logs -f deployment/contact-app`  
**Purpose:** Monitor real-time application logs.  
**Expected Outcome:** Continuous stream of Flask application logs showing requests and email sending activity.

**Command:** `kubectl top pods`  
**Purpose:** Monitor resource usage of application pods.  
**Expected Outcome:** CPU and memory usage statistics for running pods.

### Email Functionality Testing

**Manual Test:** Submit contact form through web interface with valid email address.  
**Expected Outcome:** Email received at configured RECIPIENT_EMAIL address with form data.

**SMTP Test:** Configure test SMTP server (e.g., MailHog) and verify email delivery.  
**Expected Outcome:** Email captured by test SMTP server with correct content and headers.

---

This simulation guide covers the complete DevOps pipeline from infrastructure provisioning through application deployment and validation. In a real deployment, each command would be executed in sequence, with proper error handling and rollback procedures in place for production environments.