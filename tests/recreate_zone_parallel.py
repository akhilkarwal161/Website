import subprocess
import json
import sys
import time

PROJECT_ID = "civic-source-463118-a0"
DOMAIN = "akhilkarwal.com."

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def create_zone(zone_id):
    zone_name = f"akhil-karwal-zone-{zone_id}"
    print(f"Creating zone {zone_name}...")
    run_cmd(f"gcloud dns managed-zones create {zone_name} --description=\"DNS zone {zone_id}\" --dns-name=\"{DOMAIN}\" --visibility=\"public\" --project={PROJECT_ID}")

def get_nameservers(zone_id):
    zone_name = f"akhil-karwal-zone-{zone_id}"
    res = run_cmd(f"gcloud dns record-sets list --zone={zone_name} --project={PROJECT_ID} --format=json")
    if res.returncode != 0:
        return []
    try:
        records = json.loads(res.stdout)
        for r in records:
            if r['type'] == 'NS':
                return r['rrdatas']
    except:
        pass
    return []

def delete_zone(zone_id):
    zone_name = f"akhil-karwal-zone-{zone_id}"
    print(f"Deleting zone {zone_name}...")
    run_cmd(f"gcloud dns record-sets delete {DOMAIN} --type=A --zone={zone_name} --project={PROJECT_ID} --quiet")
    run_cmd(f"gcloud dns record-sets delete {DOMAIN} --type=AAAA --zone={zone_name} --project={PROJECT_ID} --quiet")
    run_cmd(f"gcloud dns record-sets delete www.{DOMAIN} --type=CNAME --zone={zone_name} --project={PROJECT_ID} --quiet")
    run_cmd(f"gcloud dns managed-zones delete {zone_name} --project={PROJECT_ID} --quiet")

def add_records(zone_name):
    # Start transaction
    run_cmd(f"gcloud dns record-sets transaction start --zone={zone_name} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction add --name=\"{DOMAIN}\" --type=A --ttl=300 \"216.239.32.21\" \"216.239.34.21\" \"216.239.36.21\" \"216.239.38.21\" --zone={zone_name} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction add --name=\"{DOMAIN}\" --type=AAAA --ttl=300 \"2001:4860:4802:32::15\" \"2001:4860:4802:34::15\" \"2001:4860:4802:36::15\" \"2001:4860:4802:38::15\" --zone={zone_name} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction add --name=\"www.{DOMAIN}\" --type=CNAME --ttl=300 \"ghs.googlehosted.com.\" --zone={zone_name} --project={PROJECT_ID}")
    run_cmd(f"gcloud dns record-sets transaction execute --zone={zone_name} --project={PROJECT_ID}")

def main():
    # Clean up the single zone from earlier
    run_cmd(f"gcloud dns managed-zones delete akhil-karwal-zone --project={PROJECT_ID} --quiet")
    
    target_zone = None
    matched_id = None
    
    # Check up to 25 zones to guarantee finding B-series nameservers
    for i in range(1, 26):
        create_zone(i)
        ns = get_nameservers(i)
        print(f"Zone {i} Nameservers: {ns}")
        
        if ns and any("ns-cloud-b" in name for name in ns):
            print(f"MATCH FOUND in Zone {i}!")
            target_zone = f"akhil-karwal-zone-{i}"
            matched_id = i
            break
            
    if target_zone:
        # Delete all other non-matching zones created before match
        for j in range(1, matched_id):
            delete_zone(j)
            
        print(f"Configuring records in {target_zone}...")
        add_records(target_zone)
        print("Success! Your zone is configured and active with B-series nameservers!")
    else:
        print("No B-series found in 25 zones. Cleaning up all zones...")
        for i in range(1, 26):
            delete_zone(i)

if __name__ == "__main__":
    main()
