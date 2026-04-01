# DevOps Project - Architecture Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                    │
│  ┌─────────────────────────────────────────────────────┐│
│  │  GitHub Actions - CI/CD Pipeline                   ││
│  │  ├── Code Quality & Tests                          ││
│  │  ├── Security Scanning                             ││
│  │  ├── Docker Build & Push                           ││
│  │  ├── Terraform Plan & Apply                        ││
│  │  └── ECS Deployment                                ││
│  └─────────────────────────────────────────────────────┘│
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │     AWS Infrastructure           │
    │                                  │
    │  ┌────────────────────────────┐ │
    │  │    VPC (10.0.0.0/16)       │ │
    │  │                            │ │
    │  │ ┌──────────────────────┐  │ │
    │  │ │  Public Subnets      │  │ │
    │  │ │  ┌────────────────┐  │  │ │
    │  │ │  │      ALB       │  │  │ │
    │  │ │  └────────────────┘  │  │ │
    │  │ └──────────────────────┘  │ │
    │  │           ▼                │ │
    │  │ ┌──────────────────────┐  │ │
    │  │ │  Private Subnets     │  │ │
    │  │ │  ┌────────────────┐  │  │ │
    │  │ │  │  ECS Cluster   │  │  │ │
    │  │ │  │  ┌──────────┐  │  │  │ │
    │  │ │  │  │ Fargate  │  │  │  │ │
    │  │ │  │  │ Tasks    │  │  │  │ │
    │  │ │  │  └──────────┘  │  │  │ │
    │  │ │  └────────────────┘  │  │ │
    │  │ └──────────────────────┘  │ │
    │  │           ▼                │ │
    │  │ ┌──────────────────────┐  │ │
    │  │ │  RDS PostgreSQL      │  │ │
    │  │ │  (Multi-AZ)          │  │ │
    │  │ └──────────────────────┘  │ │
    │  └────────────────────────────┘ │
    │                                  │
    │  ┌────────────────────────────┐ │
    │  │  Supporting Services       │ │
    │  │  ├── ECR (Docker Registry) │ │
    │  │  ├── CloudWatch (Logs)     │ │
    │  │  ├── Secrets Manager       │ │
    │  │  └── IAM (Access Control)  │ │
    │  └────────────────────────────┘ │
    └──────────────────────────────────┘
```

## Deployment Flow

```
Code Push
    │
    ▼
GitHub Actions Trigger
    │
    ├─→ Code Quality & Linting
    │   ├── Pylint
    │   ├── Flake8
    │   └── Black
    │
    ├─→ Unit Tests
    │   └── pytest
    │
    ├─→ Integration Tests
    │   ├── Database
    │   └── Services
    │
    ├─→ Security Scanning
    │   ├── Bandit
    │   └── Safety
    │
    ├─→ Docker Build
    │   ├── Build image
    │   ├── ECR Push
    │   └── Security scan
    │
    ├─→ Terraform Plan
    │   ├── Validate
    │   ├── Plan
    │   └── Check format
    │
    ├─→ Deploy (main only)
    │   ├── ECS Update
    │   ├── Rolling deploy
    │   └── Health check
    │
    ├─→ Smoke Tests
    │   └── Post-deploy validation
    │
    └─→ Notifications
        └── Slack notification
```

## Component Details

### Application Layer (FastAPI)
- **Framework**: FastAPI for async API
- **Server**: Uvicorn with Gunicorn workers
- **Port**: 8000
- **Health Checks**: /health, /ready, /live

### Database Layer (RDS)
- **Engine**: PostgreSQL 15
- **Backup**: Daily automated backups
- **Multi-AZ**: High availability
- **Encryption**: At rest and in transit
- **Connection**: SQLAlchemy ORM

### Container Orchestration (ECS)
- **Launch Type**: Fargate
- **Scaling**: Auto-scaling based on CPU/memory
- **Placement**: Multiple AZs
- **Load Balancing**: Application Load Balancer
- **Health Checks**: Target health monitoring

### Network Architecture
- **VPC**: Custom VPC with public/private subnets
- **Routing**: Internet Gateway for public, NAT for private
- **Security**: Security groups for each tier
- **DNS**: ALB DNS endpoint

### Monitoring & Logging
- **Logs**: CloudWatch Logs
- **Metrics**: Container Insights
- **Alarms**: CloudWatch Alarms
- **Dashboards**: Custom CloudWatch dashboard

## Data Flow

```
Client Request
    │
    ▼
DNS Resolution
    │
    ▼
Application Load Balancer
    │
    ▼
Target Group Health Check
    │
    ▼
ECS Task (Fargate)
    │
    ├─→ Application Logic
    │   └── FastAPI
    │
    └─→ Database Query
        └── RDS PostgreSQL
            │
            ├─→ Read/Write
            └─→ Return Result
    │
    ▼
Response to Client
```

## Scaling Strategy

### Horizontal Scaling
- ECS Service: Auto-scale tasks based on metrics
- ALB: Distribute load across tasks
- Multi-AZ: Spread across availability zones

### Vertical Scaling
- Task CPU/Memory: Adjust task definition
- RDS: Modify instance class
- Storage: Increase allocated storage

## High Availability

1. **Multi-AZ Deployment**
   - Tasks spread across AZs
   - RDS standby in different AZ
   - NAT Gateways in each AZ

2. **Auto-Recovery**
   - ECS health checks
   - Task replacement
   - RDS automated failover

3. **Load Balancing**
   - ALB distributes traffic
   - Connection draining
   - Health-based routing

## Disaster Recovery

1. **Backup Strategy**
   - RDS automated backups (7 days)
   - Point-in-time recovery
   - Cross-region replication (optional)

2. **Recovery Procedures**
   - RDS restore from backup
   - Terraform recreate infrastructure
   - Docker images in ECR

## Security Layers

```
Client
   │
   ├─→ Security Group (ALB)
   │
   ▼
Internet Gateway
   │
   ├─→ Security Group (ECS)
   │
   ▼
ECS Task
   │
   ├─→ Security Group (RDS)
   │
   ▼
RDS Database
```

## CI/CD Pipeline Stages

1. **Stage 1: Validation**
   - Code checkout
   - Dependency installation

2. **Stage 2: Quality**
   - Linting (Pylint, Flake8)
   - Formatting (Black)
   - Security (Bandit)

3. **Stage 3: Testing**
   - Unit tests
   - Integration tests
   - Code coverage

4. **Stage 4: Build**
   - Docker build
   - Image push to ECR
   - Image scanning

5. **Stage 5: Infrastructure**
   - Terraform validate
   - Terraform plan
   - Apply changes (main only)

6. **Stage 6: Deploy**
   - Update ECS service
   - Rolling deployment
   - Health checks

7. **Stage 7: Verification**
   - Smoke tests
   - Endpoint validation
   - Health monitoring

8. **Stage 8: Notification**
   - Slack alerts
   - Email notifications
   - Deployment summary

## Configuration Management

- **Environment Variables**: Via AWS Systems Manager Parameter Store
- **Secrets**: AWS Secrets Manager
- **Configuration Files**: terraform/variables.tf
- **Application Settings**: pydantic BaseSettings

## Performance Metrics

- **Response Time**: < 500ms target
- **Throughput**: 1000+ requests/minute
- **Availability**: 99.9% uptime
- **Error Rate**: < 0.1%

---

For detailed information, refer to README.md and individual component documentation.
