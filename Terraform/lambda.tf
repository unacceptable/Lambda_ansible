########################################
### Lambda Configs: ####################
########################################

# ansible_invenotry
####################

data "archive_file" "ansible_invenotry" {
    type            = "zip"

    source_file     = "${path.module}/../Resources/ansible_invenotry.py"
    output_path     = "${path.module}/../Resources/ansible_invenotry.zip"
}

resource "aws_lambda_function" "ansible_invenotry" {

    depends_on      = [
        "data.archive_file.ansible_invenotry"
    ]

    filename        = "${path.module}/../Resources/ansible_invenotry.zip"
    function_name   = "${lookup(var.lambda,"name")}"
    role            = "${aws_iam_role.lambda_ansible_invenotry.arn}"
    handler         = "ansible_invenotry.execute_me_lambda"
    runtime         = "python2.7"
    memory_size     = 128
    timeout         = 5
    environment {
        variables   = {
            region      = "${lookup(var.global,"region")}"
        }
    }
}
