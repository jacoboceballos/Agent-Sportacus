# 🚀 AWS App Runner Deployment Guide

## Step 1: Push to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit for AWS App Runner"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/Agent-Sportacus.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to AWS App Runner

### Option A: AWS Console (Recommended)

1. **Go to AWS App Runner Console**
   - Navigate to: https://console.aws.amazon.com/apprunner/
   - Click "Create service"

2. **Configure Source**
   - Source: "Source code repository"
   - Connect to GitHub (first time setup required)
   - Repository: Select your Agent-Sportacus repo
   - Branch: main
   - Configuration file: "Use configuration file" (apprunner.yaml)

3. **Service Settings**
   - Service name: `agent-sportacus`
   - Virtual CPU: 0.25 vCPU
   - Memory: 0.5 GB
   - Auto scaling: 1-10 instances

4. **Deploy**
   - Click "Create & deploy"
   - Wait 5-10 minutes for deployment

### Option B: AWS CLI

```bash
# Install AWS CLI and configure credentials first
aws apprunner create-service \
  --service-name "agent-sportacus" \
  --source-configuration '{
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/YOUR_USERNAME/Agent-Sportacus",
      "SourceCodeVersion": {
        "Type": "BRANCH",
        "Value": "main"
      },
      "CodeConfiguration": {
        "ConfigurationSource": "REPOSITORY"
      }
    },
    "AutoDeploymentsEnabled": true
  }' \
  --instance-configuration '{
    "Cpu": "0.25 vCPU",
    "Memory": "0.5 GB"
  }'
```

## Step 3: Access Your App

After deployment completes:
- App Runner provides a URL like: `https://abc123.us-east-1.awsapprunner.com`
- Your app will be available at: `https://YOUR_URL/auth.html`

## Step 4: Configure Environment Variables (Optional)

In App Runner console:
- Go to your service → Configuration → Environment variables
- Add:
  - `AWS_DEFAULT_REGION`: us-east-1
  - `JWT_SECRET_KEY`: your-secure-secret-key

## Troubleshooting

### Build Fails
- Check build logs in App Runner console
- Ensure all dependencies are in requirements.txt
- Verify apprunner.yaml syntax

### App Won't Start
- Check application logs
- Verify the start command path
- Ensure port 8000 is used

### Database Issues
- SQLite database will be created automatically
- Data persists during app lifecycle
- For production, consider RDS integration

## Cost Estimate
- **0.25 vCPU, 0.5 GB**: ~$5-10/month
- **Auto-scaling**: Pay only for active instances
- **Free tier**: 2000 build minutes/month

## Next Steps
1. Set up custom domain (optional)
2. Configure SSL certificate (automatic)
3. Monitor with CloudWatch
4. Set up CI/CD for automatic deployments