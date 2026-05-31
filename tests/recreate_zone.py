import subprocess
import json
import time
import sys

ZONE_NAME = "akhil-karwal-zone"
PROJECT_ID = "civic-source-463118-a0"
DOMAIN = "akhilkarwal.com."

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

def get_nameservers():
    res = run_cmd(f"gcloud dns record-sets list --zone={ZONE_NAME} --project={PROJECT_ID} --format=json")
    if res.returncode != 0:
        return []
    try:
        records = json.loads(res.stdout)
        for r in records:
            if r['type'] == 'NS':
                return r['rrdatas']
    except Exception as e:
        print(f"Failed to parse NS: {e}", file=sys.stderr)
    return []

def delete_zone():
    # Delete A, AAAA, CNAME first if they exist
    run_cmd(f"gcloud dns record-sets delete {DOMAIN} --type=A --zone={ZONE_NAME} --project={PROJECT_ID} --quiet")
    run_cmd(f"gcloud dns record-sets delete {DOMAIN} --type=AAAA --zone={ZONE_NAME} --project={PROJECT_ID} --quiet")
    run_cmd(f"gcloud dns record-sets delete www.{DOMAIN} --type=CNAME --zone={ZONE_NAME} --project={PROJECT_ID} --quiet")
    # Delete zone
    run_cmd(f"gcloud dns managed-zones delete {ZONE_NAME} --project={PROJECT_ID} --quiet")

def create_zone():
    run_cmd(f"gcloud dns managed-zones create {ZONE_NAME} --description=\"DNS zone for portfolio\" --dns-name=\"{DOMAIN}\" --visibility=\"public\" --project={PROJECT_ID}")

def add_records():
    # Delete transaction file if exists
    run_cmd("del transaction.yaml")
    # Start transaction
    run_cmd(f"gcloud dns record-sets transaction start --zone={ZONE_NAME} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction add --name=\"{DOMAIN}\" --type=A --ttl=300 \"216.239.32.21\" \"216.239.34.21\" \"216.239.36.21\" \"216.239.38.21\" --zone={ZONE_NAME} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction add --name=\"{DOMAIN}\" --type=AAAA --ttl=300 \"2001:4860:4802:32::15\" \"2001:4860:4802:34::15\" \"2001:4860:4802:36::15\" \"2001:4860:4802:38::15\" --zone={ZONE_NAME} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction add --name=\"www.{DOMAIN}\" --type=CNAME --ttl=300 \"ghs.googlehosted.com.\" --zone={ZONE_NAME} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction execute --zone={ZONE_NAME} --project={PROJECT_ID}")

def main():
    attempt = 1
    while attempt <= 30: # Prevent infinite loop, limit to 30 attempts
        print(f"--- Attempt {attempt} ---")
        ns = get_nameservers()
        print(f"Current Nameservers: {ns}")
        
        # Check if they match B-series
        if ns and any("ns-cloud-b" in name for name in ns):
            print("MATCH FOUND! Allocated B-series nameservers.")
            add_records()
            print("Successfully configured A, AAAA, and CNAME records under B-series zone!")
            break
        
        print("Mismatched series. Deleting and recreating zone...")
        delete_zone()
        create_zone()
        attempt += 1
        time.sleep(1)

if __name__ == "__main__":
    main()
