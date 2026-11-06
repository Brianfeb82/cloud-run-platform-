# Incident Runbook: Production Service Degradation & Outage

This runbook defines the triage, diagnosis, and rollback procedures for the Production container service.

---

## 1. Alert Identification

### Alert: `Production Service DOWN / Unhealthy`
- **Trigger**: 2 consecutive failed health checks against `/health` or 5xx responses.
- **Impact**: Production traffic is failing or returning server errors.
- **Severity**: P1 / Critical.

---

## 2. Diagnosis Steps

### Step 1: Check Container Health & Status
```bash
docker ps -f "name=platform-api-prod"
```
Look at the `STATUS` column:
- `Up (unhealthy)`: The process is up but failing HTTP health checks.
- `Restarting`: The container process crashed and is looping.
- Missing / Exited: The container stopped.

### Step 2: Inspect Container Logs
```bash
docker logs --tail 100 platform-api-prod
```
Check for:
- Python tracebacks / Unhandled exceptions
- Missing environment variables or configuration errors
- Port binding or startup crashes

### Step 3: Test Endpoint Directly
```bash
curl -i http://127.0.0.1:8080/health
curl -i http://127.0.0.1:8080/
```

---

## 3. Rollback Procedure

When an unfixable defect or breaking change is deployed, roll back to the previously verified stable version.

### Option A: Instant Rollback via Terraform (Recommended)
Pass the last known good image version tag back into the production Terraform environment:
```bash
cd terraform/envs/prod
terraform apply -auto-approve -var="app_version=v0.1.0-prod" -var="image=cloud-platform-api:test"
```

### Option B: Rollback via GitHub Actions
1. Open GitHub repository Actions: **Deploy Production**.
2. Click **Run workflow**.
3. In the `image_tag` input, specify the previously healthy Git SHA.
4. Approve the production deployment gate.

---

## 4. Failure Drill Record (MTTR Verification)

| Drill Date | Injected Fault | Time to Detect | Time to Recover (MTTR) | Verified By |
|---|---|---|---|---|
| 2026-11-06 | Broken revision deployed (500 on `/health`) | 4 seconds | ~12 seconds | Brianfeb82 |
