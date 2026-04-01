# CI/CD Automation Project - Setup Guide

## Quick Start

### 1. Prerequisites
- AWS Account
- GitHub Account
- Docker & Docker Compose
- Python 3.11+
- Terraform 1.5.0+
- Git

### 2. Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start services
docker-compose -f docker/docker-compose.yml up -d

# Run tests
pytest tests/ -v

# Start app
uvicorn app.src.main:app --reload
```

### 3. AWS Deployment

```bash
# Configure AWS
aws configure

# Initialize Terraform
cd terraform/
terraform init
terraform plan
terraform apply

# Get outputs
terraform output
```

### 4. GitHub Configuration

1. Create GitHub secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `SLACK_WEBHOOK` (optional)

2. Push to repository to trigger pipeline

## Workflow

- **main branch**: Auto-deploy to production
- **develop branch**: Deploy to staging
- **Pull requests**: Run tests, code quality checks
- **Scheduled**: Daily tests, security audits

## File Structure

```
project/
├── .github/workflows/          # CI/CD workflows
├── app/src/                    # Application code
├── terraform/                  # Infrastructure
├── docker/                     # Docker configs
├── tests/                      # Test suites
├── scripts/                    # Utility scripts
└── requirements.txt            # Dependencies
```

## Monitoring

- CloudWatch: `/ecs/devops-automation-{env}`
- ALB: Check target health
- RDS: Database metrics
- ECR: Image scanning results

## Troubleshooting

1. **Pipeline fails**: Check GitHub Actions logs
2. **Deploy fails**: Check AWS permissions and CloudWatch logs
3. **Tests fail**: Run locally first with `pytest tests/ -v`
4. **Connection issues**: Verify security groups and VPC setup

## Security

- Store secrets in AWS Secrets Manager
- Use IAM roles for services
- Enable encryption (EBS, RDS)
- Regular security scans (Bandit, Safety)
- Network isolation with security groups

## Cost Optimization

- Use Fargate Spot for non-critical workloads
- Configure auto-scaling
- Set log retention policies
- Use reserved capacity for production

## Support

See README.md for detailed documentation.
