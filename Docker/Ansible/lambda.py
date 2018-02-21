#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import subprocess
import os, sys


#######################################
##### Global Variables ################
#######################################

hosts       = os.environ.get('hosts', 'all')
playbook    = os.environ.get('playbook', 'playbooks/test.yml')

#######################################
##### Main Function ###################
#######################################

def main():
    command = [
                "ansible-playbook",
                playbook,
                '--limit',
                hosts
            ]

    try:
        out = subprocess.check_output(
            command,
            env=dict(os.environ, hosts=hosts)
        )
    except subprocess.CalledProcessError, e:
        print e.output
        sys.exit()

    print(out)

    return out


#######################################
### Program Specific Functions ########
#######################################


#######################################
##### Execution #######################
#######################################

if __name__ == "__main__":
    main()


def execute_me_lambda(event, context):
    result  = main()
    return result
