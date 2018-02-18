########################################
### IAM Policies #######################
########################################

resource "aws_iam_policy" "lambda_ansible_invenotry" {
    name    = "lambda_ansible_invenotry"
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

resource "aws_iam_role" "lambda_ansible_invenotry" {
  name = "lambda_ansible_invenotry"

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

resource "aws_iam_policy_attachment" "expiry_attach" {
    name            = "expiry_attach"
    roles           = [
        "${aws_iam_role.lambda_ansible_invenotry.name}"
    ]
    policy_arn      = "${aws_iam_policy.lambda_ansible_invenotry.arn}"
}
