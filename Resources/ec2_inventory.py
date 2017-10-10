#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import boto3
import json
import os

'''####################################
##### Global Variables ################
####################################'''

try:
    region  = os.environ['region']
except KeyError:
    region  = 'us-east-1'

ec2         = boto3.client('ec2', region_name=region)
key_path    = '~/.ssh/AWS/'

'''####################################
##### Main Function ###################
####################################'''

def get_inventory(iname):
    if iname:
        filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    iname
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running'
                ]
            }
        ]
    else:
        filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running'
                ]
            }
        ]

    ansible_inventory = json.dumps(
        inventory_call(filters),
        sort_keys=True,
        indent=4
    )

    print(ansible_inventory)

    return ansible_inventory


'''####################################
### Program Specific Functions ########
####################################'''

def inventory_call(filters):
    instances   = lookup_instance_data(filters)
    ids         = get_ids(instances)

    json_data = {
        'all': {
            'children': [
                region
            ],
            'vars': {},
        },
        '_meta': {
            'hostvars': get_meta(instances)
        }
        ,
        region: ids
    }

    return json_data


def get_ids(instances):
    ids = [i['InstanceId'] for i in instances]

    return ids


def get_meta(instances):
    meta = None

    for data in instances:
        # This will be replaced with 'PrivateIpAddress' or 'PrivateDnsName' after testing
        ip_address      = data['PublicIpAddress']
        ssh_key_name    = data['KeyName']
        id              = data['InstanceId']

        if meta:
            newmeta = {
                id: {
                    'ansible_ssh_host': ip_address,
                    'ansible_ssh_user': 'ubuntu',
                    'ansible_ssh_private_key_file': key_path + ssh_key_name + '.pem'
                }
            }
            meta.update(newmeta)
        else:
            meta = {
                id: {
                    'ansible_ssh_host': ip_address,
                    'ansible_ssh_user': 'ubuntu',
                    'ansible_ssh_private_key_file': key_path + ssh_key_name + '.pem'
                }
            }

    return meta


def lookup_instance_data(filters):
    data = ec2.describe_instances(Filters=filters)
    instances = [i for s in [r['Instances'] for r in data['Reservations']] for i in s]

    return instances


'''####################################
##### Execution #######################
####################################'''

if __name__ == "__main__":
    try:
        Name    = os.environ['Name']
    except KeyError:
        Name    = ''

    get_inventory(Name)


def execute_me_lambda(event, context):
    try:
        Name    = os.environ['Name']
    except KeyError:
        Name    = ''

    result  = get_inventory(Name)
    return result
