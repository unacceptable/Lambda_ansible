#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import boto3
import json
import sys, os

'''####################################
##### Global Variables ################
####################################'''

region  = 'us-west-2'
ec2     = boto3.client('ec2', region_name=region)

'''####################################
##### Main Function ###################
####################################'''

def get_inventory(iname):
    json_inventory = json.dumps(
        inventory_call(iname),
        sort_keys=True,
        indent=4
    )

    print(json_inventory)


'''####################################
### Program Specific Functions ########
####################################'''

def inventory_call(name):
    idata       = lookup_instance_data(name)
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

    if isinstance(ids, list):
        for id in ids:
            ip_address  = get_ip(id, jsondata)
            ssh_key     = get_ssh_key(id, jsondata)

            if meta:
                newmeta = {
                    id: {
                        'ansible_ssh_host': ip_address,
                        'ansible_ssh_user': 'ubuntu',
                        'ansible_ssh_private_key_file': '~/.ssh/AWS/' + ssh_key + '.pem'
                    }
                }
                meta.update(newmeta)
            else:
                meta = {
                    id: {
                        'ansible_ssh_host': ip_address,
                        'ansible_ssh_user': 'ubuntu',
                        'ansible_ssh_private_key_file': '~/.ssh/AWS/' + ssh_key + '.pem'
                    }
                }
    else:
        ip_address  = get_ip(ids, jsondata)
        ssh_key     = get_ssh_key(ids, jsondata)

        meta = {
            ids: {
                        'ansible_ssh_host': ip_address,
                        'ansible_ssh_user': 'ubuntu',
                        'ansible_ssh_private_key_file': '~/.ssh/AWS/' + ssh_key + '.pem'
            }
        }

    return meta


def get_ssh_key(id, jsondata):
    key_name = None

    for index in range(len(jsondata)):
        instance = jsondata[index]['Instances']

        for index in range(len(instance)):
            if instance[index]['InstanceId'] == id:
                key_name = instance[index]['KeyName']
                return key_name

    print("No key found.")
    sys.exit(1)


def get_ip(id, jsondata):
    ip = None

    for index in range(len(jsondata)):
        instance = jsondata[index]['Instances']

        for index in range(len(instance)):
            if instance[index]['InstanceId'] == id:
                ip = instance[index]['PublicIpAddress']
                return ip

    print( "No IP found for server: " + id )


def lookup_instance_data(name):
    data = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    name
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running'
                ]
            }
        ]
    )

    return data['Reservations']


'''####################################
##### Execution #######################
####################################'''

if __name__ == "__main__":
    iname = 'Blog'
    get_inventory(iname)


def execute_me_lambda(event, context):
    iname   = os.environ['iname']
    result  = get_inventory(iname)
    return result
