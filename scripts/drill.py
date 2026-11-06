import subprocess
import time

print("=" * 60)
print("PRODUCTION FAILURE DRILL: DETECT -> ALERT -> RECOVER")
print("=" * 60)

print("\n[Phase 1] Launching Uptime Monitor...")
monitor = subprocess.Popen(["python3", "-u", "scripts/monitor.py"])
time.sleep(3)

print("\n[Phase 2] Simulating Incident: Stopping Production Container...")
subprocess.run(["docker", "stop", "platform-api-prod"], check=True)
time.sleep(6)

print("\n[Phase 3] Executing Terraform Rollback / Recovery...")
t0 = time.time()
subprocess.run(["terraform", "apply", "-auto-approve", "-no-color"], cwd="terraform/envs/prod", check=True)
t_recover = time.time() - t0
print(f"Terraform completed in {round(t_recover, 2)}s")

time.sleep(4)

monitor.terminate()
print("\n" + "=" * 60)
print("FAILURE DRILL COMPLETED SUCCESSFULLY")
print("=" * 60)
