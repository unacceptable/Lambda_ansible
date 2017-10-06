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

def main(iname):
    json_inventory = json.dumps(
        inventory(iname),
        sort_keys=True,
        indent=4
    )

    print(json_inventory)


def inventory(name):
    idata       = lookup_instance_data(name)

    ip_address  = parse_data_for_ips(idata)

    if not ip_address:
        print('No IPs found.')
        sys.exit(1)

    json_data = {
        'all': {
            'children': [
                region
            ],
            'vars': {},
        },
        '_meta': {
            'hostvars': {
                name: {
                    'ansible_ssh_host': ip_address[0],
                    'ansible_ssh_user': 'ubuntu',
                    'ansible_ssh_private_key_file': '~/.ssh/AWS/Blog.pem'
                }
            },
        },
        region: [name]
    }

    return json_data


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


def parse_data_for_ips(list):
    ips = None

    for index in range(len(list)):
        match = list[index]['Instances']

        for index in range(len(match)):
            ip = match[index]['PublicIpAddress']
            if ips:
                ips = [ips, ip]
            else:
                ips = [ip]

    return ips



'''####################################
##### Execution #######################
####################################'''

if __name__ == "__main__":
    iname = 'Blog'
    main(iname)


def execute_me_lambda(event, context):
    iname   = os.environ['iname']
    result  = main(iname)
    return result
