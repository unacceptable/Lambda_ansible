########################################
### IAM Policies #######################
########################################

resource "aws_iam_policy" "lambda_ansible_inventory" {
    name    = "lambda_ansible_inventory"
    path    = "/"
    policy  = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        }
    ]
}
POLICY
}

resource "aws_iam_policy" "lambda_ansible_execution" {
    name    = "lambda_ansible_execution"
    path    = "/"
    policy  = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "*"
        }
    ]
}
POLICY
}

########################################
### IAM Roles ##########################
########################################

resource "aws_iam_role" "lambda_ansible_inventory" {
  name = "lambda_ansible_inventory"

  assume_role_policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
POLICY
}

resource "aws_iam_role" "lambda_ansible_execution" {
  name = "lambda_ansible_execution"

  assume_role_policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
POLICY
}

########################################
### IAM Policy Attachments #############
########################################

resource "aws_iam_policy_attachment" "lambda_ansible_inventory" {
    name            = "ansible_inventory"
    roles           = [
        "${aws_iam_role.lambda_ansible_inventory.name}"
    ]
    policy_arn      = "${aws_iam_policy.lambda_ansible_inventory.arn}"
}

resource "aws_iam_policy_attachment" "lambda_ansible_execution" {
    name            = "ansible_execution"
    roles           = [
        "${aws_iam_role.lambda_ansible_execution.name}"
    ]
    policy_arn      = "${aws_iam_policy.lambda_ansible_execution.arn}"
}
