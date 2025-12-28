# Deployment Guide

## Overview

This document provides instructions for deploying the Learning Path Analyzer in different environments.

## Local Development

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Installation Steps

```bash
# Clone repository
git clone https://github.com/RoadToDestiny/learning-path-analyzer.git
cd learning-path-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run analysis
python src/main.py
```

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
```

### Build and Run

```bash
# Build image
docker build -t learning-path-analyzer:1.0.0 .

# Run container
docker run -v $(pwd)/data:/app/data -v $(pwd)/reports:/app/reports learning-path-analyzer:1.0.0
```

## GitHub Actions CI/CD

### Automatic Workflows

The project includes two pre-configured GitHub Actions workflows:

#### 1. Tests Workflow (tests.yml)
- Triggered on push to main/develop and PRs
- Runs tests on Python 3.8, 3.9, 3.10
- Performs linting and code formatting checks
- Reports coverage to Codecov

#### 2. Scheduled Analysis (scheduled-analysis.yml)
- Runs daily at 2 AM UTC
- Can be manually triggered
- Generates and commits analysis reports
- Uploads artifacts for 30 days

### Manual Workflow Trigger

```bash
# Via GitHub API
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_USERNAME/learning-path-analyzer/actions/workflows/scheduled-analysis.yml/dispatches \
  -d '{"ref":"main"}'
```

## Environment Variables

Create a `.env` file for configuration:

```bash
# Data paths
DATA_INPUT_PATH=data/lms_logs.csv
REPORTS_OUTPUT_PATH=reports/

# Logging
LOG_LEVEL=INFO

# Analysis settings
MIN_ACTIVITIES=5
TOP_STUDENTS_COUNT=5
```

## Production Deployment

### Prerequisites for Production

- Production-grade Python environment
- Database for storing results (optional)
- Regular backup strategy
- Monitoring and logging system

### Production Checklist

- [ ] Test all workflows in staging
- [ ] Configure proper error handling
- [ ] Set up monitoring and alerts
- [ ] Configure database connections
- [ ] Set up automated backups
- [ ] Document data retention policies
- [ ] Configure access controls
- [ ] Set up logging aggregation
- [ ] Create disaster recovery plan
- [ ] Document runbooks

### Kubernetes Deployment (Advanced)

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learning-path-analyzer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: learning-path-analyzer
  template:
    metadata:
      labels:
        app: learning-path-analyzer
    spec:
      containers:
      - name: analyzer
        image: learning-path-analyzer:1.0.0
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
        - name: reports-volume
          mountPath: /app/reports
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: data-pvc
      - name: reports-volume
        persistentVolumeClaim:
          claimName: reports-pvc
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
kubectl rollout status deployment/learning-path-analyzer
```

## Scheduled Execution

### Using Cron

```bash
# Add to crontab
0 2 * * * cd /path/to/project && python src/main.py
```

### Using Schedule Library

```python
import schedule
import time
from src.analyzer import LearningPathAnalyzer

def run_analysis():
    analyzer = LearningPathAnalyzer()
    analyzer.load_data('data/lms_logs.csv')
    # ... rest of analysis

schedule.every().day.at("02:00").do(run_analysis)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Monitoring

### Health Check Script

```bash
#!/bin/bash
# health_check.sh

if [ -f "reports/analysis_report.json" ]; then
    echo "Health: OK"
    exit 0
else
    echo "Health: FAILED"
    exit 1
fi
```

### Log Monitoring

```bash
# Monitor analysis logs
tail -f analysis.log | grep ERROR
```

## Troubleshooting

### Common Issues

**Issue**: ImportError when running analysis
```bash
# Solution: Install dependencies
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Issue**: Permission denied on reports directory
```bash
# Solution: Fix permissions
chmod -R 755 reports/
```

**Issue**: Out of memory with large datasets
```bash
# Solution: Process in chunks
# See src/analyzer.py for chunking options
```

## Backup and Recovery

### Backup Strategy

```bash
# Daily backup
tar -czf backups/reports-$(date +%Y%m%d).tar.gz reports/

# Keep 30 days of backups
find backups/ -mtime +30 -delete
```

### Recovery

```bash
# Restore from backup
tar -xzf backups/reports-20240110.tar.gz
```

## Performance Tuning

### Optimization Tips

1. **Data Processing**: Use chunking for large datasets
2. **Memory**: Monitor memory usage with large CSV files
3. **Speed**: Cache computed values between analysis runs
4. **Storage**: Archive old reports regularly

## Security Considerations

- [ ] Sanitize input data
- [ ] Validate file paths
- [ ] Restrict file permissions
- [ ] Use environment variables for sensitive data
- [ ] Enable audit logging
- [ ] Regular dependency updates
- [ ] Code scanning with security tools

## Scaling

### Horizontal Scaling

- Deploy multiple instances
- Use load balancer
- Share data via distributed storage

### Vertical Scaling

- Increase server resources
- Optimize code for efficiency
- Cache results

## Support

For deployment issues, open an issue on GitHub or contact the maintainers.

---

**Last Updated**: 2024-01-10
