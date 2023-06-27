import argparse
import subprocess
import re

### config
project = 'tesorai-390809'
zone = 'us-central1-a'

def run():
    parser = argparse.ArgumentParser()
    # parser.add_argument('cmd')
    parser.add_argument('--machine-type', default='e2-micro')
    args = parser.parse_args()

    instances = get_instances()
    for i in range(1, 1_000):
        if i not in instances:
            break
    subprocess.call(create_instance_cmd(f'glurm-{i}', args.machine_type), shell=True)

def cancel():
    parser = argparse.ArgumentParser()
    parser.add_argument('id')
    args = parser.parse_args()

    instances = get_instances()
    if args.id == 'all':
        names = ' '.join(f'glurm-{id}' for id in instances)
    else:
        names = f'glurm-{args.id}'
    subprocess.call(f'gcloud compute instances delete {names} --quiet', shell=True)

def queue():
    subprocess.call('gcloud compute instances list --filter glurm-', shell=True)

def get_instances():
    output = subprocess.check_output('gcloud compute instances list --filter glurm- --format "table(name)"', shell=True)
    instances = set()
    for name in output.decode().splitlines()[1:]:
        instances.add(int(re.search('glurm-(\d+)', name).group(1)))
    return instances

def create_instance_cmd(name, machine_type):
    return f'gcloud compute instances create {name} --project={project} --zone={zone} --machine-type={machine_type} --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=898400494316-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --create-disk=auto-delete=yes,boot=yes,device-name=instance-1,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230615,mode=rw,size=10,type=projects/tesorai-390809/zones/us-central1-a/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=goog-ec-src=vm_add-gcloud --reservation-affinity=any'
