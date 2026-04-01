# DevOps CI/CD Automation Project

Complete DevOps automation project with CI/CD pipeline for AWS deployment using GitHub Actions, Terraform, Docker, and comprehensive testing.

## Project Structure

```
.
├── .github/workflows/              # GitHub Actions workflows
│   ├── ci-cd-pipeline.yml         # Main CI/CD pipeline
│   ├── manual-deployment.yml      # Manual deployment workflow
│   ├── infrastructure.yml         # Terraform infrastructure
│   └── scheduled-tests.yml        # Scheduled testing
├── app/                            # Application code
│   └── src/                        # Source code
│       ├── main.py                # FastAPI application
│       ├── database.py            # Database configuration
│       └── config.py              # App configuration
├── terraform/                      # Infrastructure as Code
│   ├── main.tf                    # Main Terraform config
│   ├── variables.tf               # Variables
│   ├── vpc.tf                     # VPC configuration
│   ├── ecs.tf                     # ECS configuration
│   ├── rds.tf                     # RDS configuration
│   └── outputs.tf                 # Outputs
├── docker/                         # Docker configuration
│   ├── Dockerfile                 # Production Dockerfile
│   ├── Dockerfile.multistage      # Multi-stage Dockerfile
│   └── docker-compose.yml         # Docker Compose
├── tests/                          # Test suites
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── smoke/                     # Smoke tests
│   └── conftest.py                # Pytest configuration
├── k8s/                            # Kubernetes manifests (optional)
├── scripts/                        # Utility scripts
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
└── README.md                       # This file
```

## Features

### CI/CD Pipeline (`ci-cd-pipeline.yml`)
- **Code Quality**: Pylint, Flake8, Black formatting
- **Unit Tests**: PyTest with coverage reports
- **Integration Tests**: Database and service integration tests
- **Security Scanning**: Bandit security analysis, dependency vulnerability checks
- **Docker Build**: Multi-stage build with ECR push
- **Infrastructure**: Terraform plan and validation
- **Deployment**: AWS ECS deployment with health checks
- **Smoke Tests**: Post-deployment validation
- **Notifications**: Slack notifications

### Infrastructure (Terraform)
- **VPC**: Complete VPC with public/private subnets
- **Security**: Security groups, NAT gateways, proper network isolation
- **ECS**: Fargate container orchestration with auto-scaling
- **ALB**: Application Load Balancer with health checks
- **RDS**: PostgreSQL database with encrypted storage
- **ECR**: Docker image repository with lifecycle policies
- **Monitoring**: CloudWatch logs and Container Insights
- **Secrets**: AWS Secrets Manager for sensitive data

### Application
- **FastAPI**: Modern Python web framework
- **RESTful API**: Complete CRUD operations
- **Health Checks**: Kubernetes-ready health endpoints
- **Logging**: Structured logging
- **Configuration**: Environment-based settings
- **Database**: SQLAlchemy ORM integration

### Testing
- **Unit Tests**: API endpoint testing
- **Integration Tests**: Database and service integration
- **Smoke Tests**: Post-deployment validation
- **Coverage Reports**: Code coverage metrics
- **Performance Tests**: Load and performance testing

## Prerequisites

- AWS Account with appropriate permissions
- GitHub repository with Actions enabled
- Docker and Docker Compose (local development)
- Python 3.11+
- Terraform 1.5.0+
- Git

## Setup Instructions

### 1. Local Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start services with Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# Run tests
pytest tests/unit/ -v

# Start application
python -m uvicorn app.src.main:app --reload
```

### 2. AWS Setup

```bash
# Configure AWS credentials
aws configure

# Set up S3 bucket for Terraform state (optional)
aws s3 mb s3://your-terraform-state-bucket
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### 3. GitHub Secrets Configuration

Set the following secrets in GitHub repository settings:

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `SLACK_WEBHOOK`: Slack webhook URL (optional)

### 4. Terraform Deployment

```bash
cd terraform/

# Initialize Terraform
terraform init

# Plan infrastructure
terraform plan -out=tfplan

# Apply infrastructure
terraform apply tfplan

# Get outputs
terraform output
```

## Workflow Triggers

### CI/CD Pipeline
- Automatically triggered on:
  - Push to `main` or `develop` branches
  - Pull requests to `main` or `develop`
  - Manual trigger via `workflow_dispatch`

### Manual Deployment
- Triggered via GitHub Actions UI with options:
  - Environment selection (staging/production)
  - Docker image tag
  - Option to skip tests

### Infrastructure Changes
- Triggered when changes to `terraform/` directory
- Auto-applies on `main` branch
- Requires approval on pull requests

### Scheduled Tests
- Daily at 2 AM UTC
- Weekly on Sunday at midnight UTC
- Includes performance tests, health checks, and security audits

## Deployment Flow

1. **Code Commit** → Push to GitHub
2. **Trigger Pipeline** → GitHub Actions starts
3. **Code Quality** → Pylint, Flake8, Black
4. **Tests** → Unit & Integration tests
5. **Security** → Bandit, Safety, pip-audit
6. **Build** → Docker image created
7. **Infrastructure** → Terraform validation
8. **Deploy** → ECS service update (main branch only)
9. **Verify** → Health checks and smoke tests
10. **Notify** → Slack notification

## Testing

```bash
# Run all tests
pytest -v

# Run specific test suite
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/smoke/ -v

# Run with coverage
pytest --cov=app/src --cov-report=html

# Run specific test
pytest tests/unit/test_main.py::TestItems::test_create_item -v
```

## Monitoring

### CloudWatch
- Log group: `/ecs/devops-automation-{environment}`
- Retention: 7 days
- Container Insights enabled

### Metrics
- Access metrics endpoint: `GET /metrics`
- CPU and memory utilization via CloudWatch
- ALB target health status

### Alarms
Configure in CloudWatch dashboard:
- High CPU utilization
- Service unavailability
- Failed deployments
- Database connection issues

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `ENVIRONMENT`: dev/staging/prod
- `DATABASE_URL`: PostgreSQL connection string
- `AWS_REGION`: AWS region for resources
- `LOG_LEVEL`: Logging level

## Troubleshooting

### Pipeline Failures

1. **Code Quality Issues**
   - Review Pylint/Flake8 output
   - Run `black --check app/src/`

2. **Test Failures**
   - Check database connectivity
   - Review test logs in GitHub Actions

3. **Deployment Issues**
   - Verify AWS credentials
   - Check ECS service logs in CloudWatch
   - Review Terraform state

### Common Issues

- **Import errors**: Ensure all dependencies are in `requirements.txt`
- **Database connection**: Check `DATABASE_URL` and network connectivity
- **AWS permissions**: Verify IAM role permissions
- **Docker build fails**: Check Dockerfile and build context

## Security Best Practices

1. **Secrets Management**
   - Use AWS Secrets Manager for sensitive data
   - Never commit secrets to repository
   - Rotate credentials regularly

2. **Network Security**
   - Use security groups to restrict access
   - Enable encryption in transit and at rest
   - Use NAT gateways for private subnets

3. **Code Security**
   - Run Bandit for code vulnerabilities
   - Use pip-audit for dependency vulnerabilities
   - Enable security scanning on ECR

4. **Access Control**
   - Use IAM roles and policies
   - Enable MFA for AWS accounts
   - Restrict GitHub Actions permissions

## Scaling

### Horizontal Scaling
- ECS service auto-scaling based on CPU/memory
- ALB distributes traffic across tasks
- Multi-AZ deployment for high availability

### Database Scaling
- RDS read replicas for read-heavy workloads
- Connection pooling with Redis
- Automated backups and point-in-time recovery

## Cost Optimization

- Use Fargate Spot instances for non-critical workloads
- Auto-scaling to reduce idle resources
- Reserved capacity for stable workloads
- CloudWatch log retention policies

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add your feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Create Pull Request with description

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check GitHub Issues
2. Review CloudWatch logs
3. Check GitHub Actions workflow logs
4. Contact development team

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated**: April 1, 2026
**Version**: 1.0.0
