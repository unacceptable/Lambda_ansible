#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import ec2_inventory

'''####################################
##### Global Variables ################
####################################'''

'''####################################
##### Main Function ###################
####################################'''

def ansible_execute():
    ec2_inventory.main('Wordpress Worker Node')
    return None


'''####################################
### Program Specific Functions ########
####################################'''


'''####################################
##### Execution #######################
####################################'''

if __name__ == "__main__":
    ansible_execute()


def execute_me_lambda(event, context):
    result  = ansible_execute()
    return result
