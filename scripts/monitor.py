import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

TARGET_URL = "http://127.0.0.1:8080/health"
POLL_INTERVAL_SEC = 2
FAILURE_THRESHOLD = 2


def log(msg):
    print(msg, flush=True)


def check_health():
    start = time.time()
    try:
        req = urllib.request.Request(TARGET_URL, headers={"User-Agent": "Platform-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            status_code = resp.getcode()
            body = resp.read().decode("utf-8")
            latency_ms = round((time.time() - start) * 1000, 2)
            return status_code == 200, status_code, latency_ms, body
    except urllib.error.HTTPError as e:
        latency_ms = round((time.time() - start) * 1000, 2)
        return False, e.code, latency_ms, str(e)
    except Exception as e:
        latency_ms = round((time.time() - start) * 1000, 2)
        return False, 0, latency_ms, str(e)


def main():
    log(f"[{datetime.now().isoformat()}] Starting Production Uptime Monitor on {TARGET_URL}")
    consecutive_failures = 0
    in_alert_state = False
    alert_start_time = None

    try:
        while True:
            ok, code, latency, msg = check_health()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if ok:
                if in_alert_state and alert_start_time is not None:
                    recovery_duration = round(time.time() - alert_start_time, 2)
                    log(
                        f"\n[{now}] [RESOLVED] Service recovered! "
                        f"Status: {code} | Latency: {latency}ms | Incident duration: {recovery_duration}s\n"
                    )
                    in_alert_state = False
                    alert_start_time = None
                    consecutive_failures = 0
                else:
                    log(f"[{now}] [HEALTHY] Status: {code} | Latency: {latency}ms")
                    consecutive_failures = 0
            else:
                consecutive_failures += 1
                log(
                    f"[{now}] [WARNING] Health check failed ({consecutive_failures}/{FAILURE_THRESHOLD}) | "
                    f"Code: {code} | Error: {msg}"
                )
                if consecutive_failures >= FAILURE_THRESHOLD and not in_alert_state:
                    in_alert_state = True
                    alert_start_time = time.time()
                    log("\n" + "=" * 60)
                    log(f"[{now}] >>> ALERT TRIGGERED: Production Service DOWN! <<<")
                    log(f"Target: {TARGET_URL}")
                    log(f"Action: Check logs and initiate rollback per docs/incident-runbook.md")
                    log("=" * 60 + "\n")

            time.sleep(POLL_INTERVAL_SEC)
    except KeyboardInterrupt:
        log("\nMonitor stopped.")


if __name__ == "__main__":
    main()
