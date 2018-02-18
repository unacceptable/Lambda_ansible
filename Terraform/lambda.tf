########################################
### Lambda Configs: ####################
########################################

# ansible_inventory
####################

data "archive_file" "ansible_inventory" {
    type            = "zip"

    source_file     = "${path.module}/../Resources/ansible_inventory/ansible_inventory.py"
    output_path     = "${path.module}/../Resources/ansible_inventory/ansible_inventory.zip"
}

resource "aws_lambda_function" "ansible_inventory" {

    depends_on      = [
        "data.archive_file.ansible_inventory"
    ]

    filename        = "${path.module}/../Resources/ansible_inventory/ansible_inventory.zip"
    function_name   = "${lookup(var.lambda,"name")}"
    role            = "${aws_iam_role.lambda_ansible_inventory.arn}"
    handler         = "ansible_inventory.execute_me_lambda"
    runtime         = "python2.7"
    memory_size     = 128
    timeout         = 5
    environment {
        variables   = {
            region      = "${lookup(var.global,"region")}"
        }
    }
}
