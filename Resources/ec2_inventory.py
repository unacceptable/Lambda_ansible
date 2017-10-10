#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import boto3
import json
import sys, os

'''####################################
##### Global Variables ################
####################################'''

region      = 'us-west-2'
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
    idata       = lookup_instance_data(filters)
    ids         = get_ids(idata)

    json_data = {
        'all': {
            'children': [
                region
            ],
            'vars': {},
        },
        '_meta': {
            'hostvars': get_meta(ids, idata)
        }
        ,
        region: ids
    }

    return json_data


def get_ids(jsondata):
    ids = None

    for index in range(len(jsondata)):
        match = jsondata[index]['Instances']

        for index in range(len(match)):
            id = match[index]['InstanceId']

            if ids:
                ids = [ids, id]
            else:
                ids = id

    if not isinstance(ids, list):
        ids = [ids]

    return ids


def get_meta(ids, jsondata):

    meta = None

    for id in ids:
        ip_address      = get_info(id, jsondata, 'PublicIpAddress')
        ssh_key_name    = get_info(id, jsondata, 'KeyName')

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


def get_info(id, jsondata, search):
    info = None

    for index in range(len(jsondata)):
        instance = jsondata[index]['Instances']

        for index in range(len(instance)):
            if instance[index]['InstanceId'] == id:
                info = instance[index][search]
                return info

    print(search + " not found.")
    sys.exit(1)


def lookup_instance_data(filters):
    data = ec2.describe_instances(Filters=filters)

    return data['Reservations']


'''####################################
##### Execution #######################
####################################'''

if __name__ == "__main__":
    try:
        iname   = os.environ['iname']
    except KeyError:
        iname   = ''
    get_inventory(iname)


def execute_me_lambda(event, context):
    iname   = os.environ['iname']
    result  = get_inventory(iname)
    return result
