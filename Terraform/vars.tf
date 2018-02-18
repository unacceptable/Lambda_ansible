########################################
### Variables ##########################
########################################

variable "global" {
    type    = "map"
    default = {
        region  = "us-west-2"
        tags    = "Staging"
    }
}

variable "lambda" {
    type    = "map"
    default = {
        name    = "ansible_inventory"
    }
}
