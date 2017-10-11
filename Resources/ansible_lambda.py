#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import subprocess
import os, sys


'''####################################
##### Global Variables ################
####################################'''

Name        = os.environ.get('Name', 'Wordpress Worker Node')


'''####################################
##### Main Function ###################
####################################'''

def main():

    command = [
                "ansible-playbook",
                "./test.yml",
                "-i",
                "./ec2_inventory.py"
            ]

    try:
        out = subprocess.check_output(
            command,
            env=dict(os.environ, Name=Name)
        )
    except subprocess.CalledProcessError, e:
        print e.output
        sys.exit()

    print(out)

    return out


'''####################################
### Program Specific Functions ########
####################################'''


'''####################################
##### Execution #######################
####################################'''

if __name__ == "__main__":
    main()


def execute_me_lambda(event, context):
    result  = main()
    return result
