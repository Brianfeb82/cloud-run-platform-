# Production-Style Container Deployment Platform

[![Deploy Staging](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/deploy-staging.yml/badge.svg)](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/deploy-staging.yml)
[![Deploy Production](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/deploy-prod.yml/badge.svg)](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/deploy-prod.yml)
[![CI Pipeline](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/ci.yml/badge.svg)](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/ci.yml)
[![Terraform Plan](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/terraform-plan.yml/badge.svg)](https://github.com/Brianfeb82/cloud-run-platform-/actions/workflows/terraform-plan.yml)

> A production-grade, GitOps-driven deployment platform built with **FastAPI**, **Docker**, **Terraform (IaC)**, and **GitHub Actions**. Features multi-environment staging & production isolation, automated smoke testing, manual production approval gates, and synthetic uptime monitoring with a verified **7.02s Mean Time to Recovery (MTTR)**.

---

## Architecture Overview

![Platform Architecture](docs/architecture.svg)

### Pipeline Flow

```text
Developer (Git Push / PR)
    │
    ▼
[CI Pipeline]
  ├── Pytest Unit Tests
  ├── Dockerfile Build Check
  └── Terraform fmt & validate
    │
    ▼ (Merge to main)
[Deploy Staging]
  ├── Build Immutable Image (Tagged by Git SHA)
  ├── Terraform Apply (Staging Environment, Port 8081)
  └── Automated Smoke Test (curl /health -> 200 OK)
    │
    ▼ (Deployment Succeeded)
[Production Gate (GitHub Environment: production)]
  ├── Manual Reviewer Approval Required (@Brianfeb82)
  │
  ▼ (Approved)
[Deploy Production]
  ├── Promotes the EXACT Staging Image SHA (No Rebuilds)
  ├── Terraform Apply (Prod Environment, Port 8080)
  └── Automated Production Smoke Test
    │
    ▼
[Monitoring & Incident Recovery]
  └── Synthetic Health Probe (2s interval) -> Alert on Failure -> 7s Rollback
```

---

## Key Features

1. **Immutable Deployments**: The production environment promotes the exact image artifact validated in staging. Images are tagged with the Git SHA—never `latest`.
2. **Infrastructure as Code (IaC)**: Zero manual infrastructure provisioning. Every container, port mapping, restart policy, and environment variable is declared across modular Terraform configurations (`terraform/modules/container-service/`).
3. **Manual Approval Gate**: Production deployments enforce the `production` GitHub Environment protection rule with required reviewers.
4. **Self-Healing & Drift Detection**: Terraform tracks container state; stopped or deleted containers are automatically re-provisioned to match desired state.
5. **Zero Cloud Cost ($0 / Free Tier)**: Designed with 100% free and open-source tooling. No credit card required.

---

## Repository Structure

```
cloud-run-platform/
├── app/
│   ├── main.py                     # FastAPI application
│   ├── requirements.txt             # Pinned dependencies
│   ├── Dockerfile                  # Multi-stage/slim container build (non-root)
│   └── tests/
│       └── test_main.py            # Unit tests for health & root endpoints
├── terraform/
│   ├── modules/
│   │   └── container-service/      # Reusable container module (lifecycle, ports, env)
│   └── envs/
│       ├── staging/                # Staging env (port 8081, restart unless-stopped)
│       └── prod/                   # Production env (port 8080, restart always)
├── .github/workflows/
│   ├── ci.yml                      # PR testing & Docker dry-run build
│   ├── terraform-plan.yml          # Automated Terraform lint & plan on PRs
│   ├── deploy-staging.yml          # Automated staging deployment on push to main
│   └── deploy-prod.yml             # Protected manual-approval production promotion
├── scripts/
│   ├── monitor.py                  # Synthetic uptime monitoring & latency probe
│   └── drill.py                    # Automated failure drill execution
├── docs/
│   ├── architecture.svg            # Architecture diagram
│   └── incident-runbook.md         # Production incident & rollback runbook
├── .gitignore
└── README.md
```

---

## Quickstart: Running Locally

### 1. Prerequisites
- Docker Engine (`docker --version`)
- Terraform (`terraform version >= 1.5.0`)
- Python 3.12+

### 2. Build and Test the Application
```bash
# Build the container image
docker build -t cloud-platform-api:test -f app/Dockerfile app/

# Run unit tests inside the container
docker run --rm cloud-platform-api:test pytest -v
```

### 3. Deploy Staging & Production via Terraform
```bash
# Deploy Staging (Port 8081)
cd terraform/envs/staging
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply -auto-approve

# Deploy Production (Port 8080)
cd ../prod
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply -auto-approve
```

### 4. Verify Endpoints
```bash
# Staging endpoint
curl -s http://127.0.0.1:8081/
curl -s http://127.0.0.1:8081/health

# Production endpoint
curl -s http://127.0.0.1:8080/
curl -s http://127.0.0.1:8080/health
```

---

## Production Failure Drill & Recovery (MTTR)

To verify the platform's resilience, an automated incident drill was executed using `scripts/drill.py`:

```bash
python3 scripts/drill.py
```

### Live Drill Results:
```text
[2026-11-06 23:13:46] [HEALTHY] Status: 200 | Latency: 6.13ms
[Phase 2] Simulating Incident: Stopping Production Container...
[2026-11-06 23:13:48] [WARNING] Health check failed (1/2) | Connection refused
[2026-11-06 23:13:53] [WARNING] Health check failed (2/2) | Connection timed out

============================================================
>>> ALERT TRIGGERED: Production Service DOWN! <<<
Target: http://127.0.0.1:8080/health
Action: Check logs and initiate rollback per docs/incident-runbook.md
============================================================

[Phase 3] Executing Terraform Rollback / Recovery...
Terraform detected drift: module.prod_app.docker_container.app has been deleted
Terraform recreated container in 3.76s.

[2026-11-06 23:14:00] [RESOLVED] Service recovered! Status: 200 | Latency: 20.72ms | Incident duration: 7.02s
```

- **Detection Time**: 4 seconds (2 consecutive failed synthetic probes).
- **Remediation Time**: 3.76 seconds (Terraform state reconciliation).
- **Verified MTTR**: **7.02 seconds**.

For full diagnosis and rollback instructions, see [`docs/incident-runbook.md`](docs/incident-runbook.md).

---

## Teardown (Clean State)

To destroy all running resources and avoid idle resource usage:

```bash
# Destroy Staging
cd terraform/envs/staging
terraform destroy -auto-approve

# Destroy Production
cd ../prod
terraform destroy -auto-approve
```

---

## Lessons Learned
- **Never rebuild containers for production**: Building once during CI and promoting the identical image SHA eliminates the "works on staging but fails in prod" class of bugs.
- **Drift detection as a self-healing mechanism**: Using Terraform state reconciliation allows instant recovery from dropped containers or modified runtime environments.
- **Automated synthetic probes**: Continuous active health polling detects degradation before end users experience catastrophic outages.
