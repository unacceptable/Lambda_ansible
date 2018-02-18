#!/usr/bin/env python
# Written by:   Robert J.
#               Robert@scriptmyjob.com

import boto3
import os

#######################################
##### Global Variables ################
#######################################

region      = os.environ.get('region', 'us-west-2')
function    = os.environ.get('function', 'lambda_shutdown_ec2')
aws_lambda  = boto3.client("lambda", region_name=region)

#######################################
##### Main Function ###################
#######################################

def main():
    out = aws_lambda.invoke(FunctionName=function)
    data = out['Payload'].read()
    print(data)

    return out


#######################################
### Execution #########################
#######################################

if __name__ == "__main__":
    main()

def execute_me_lambda(event, context):
    out = main()
    return out
