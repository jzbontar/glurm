import argparse
import subprocess
import re

### config
project = 'tesorai-390809'
zone = 'us-central1-a'

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd')
    parser.add_argument('--machine-type', default='e2-micro')
    args = parser.parse_args()

    instances = get_instances()
    for i in range(1, 1_000):
        if i not in instances:
            break
    subprocess.call(create_instance_cmd(f'glurm-{i}', args.machine_type), shell=True)

def cancel():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', nargs='+', type=int)
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    all_instances = get_instances()
    if args.all:
        instances = all_instances.values()
    else:
        instances = [all_instances[i] for i in args.id]
    names = ' '.join(i['name'] for i in instances)
    zones = [i['zone'] for i in instances]
    assert len(set(zones)) == 1
    subprocess.call(f'gcloud compute instances delete {names} --zone {zones[0]} -q', shell=True)

def queue():
    subprocess.call('gcloud compute instances list --filter glurm-', shell=True)

def get_instances():
    output = subprocess.check_output('gcloud compute instances list --filter glurm- --format "csv(name,zone)"', shell=True)
    instances = dict()
    for line in output.decode().splitlines()[1:]:
        name, zone = line.split(',')
        id = int(re.search('glurm-(\d+)', name).group(1))
        instances[id] = dict(id=id, name=name, zone=zone)
    return instances

def create_instance_cmd(name, machine_type):
    return f'''gcloud compute instances create {name} \
    --project={project} \
    --zone={zone} \
    --machine-type={machine_type} \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=898400494316-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --create-disk=auto-delete=yes,boot=yes,device-name=instance-1,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230615,mode=rw,size=10,type=projects/tesorai-390809/zones/us-central1-a/diskTypes/pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any'''
