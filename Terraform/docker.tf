provider "docker" {
    host = "unix:///var/run/docker.sock"
}

resource "null_resource" "build_image" {
    provisioner "local-exec" {
        command = "cd ../Docker && docker build -t 'name:lambda_ansible' .;"
    }
}

resource "docker_container" "amazon_linux" {
    depends_on = [
        "null_resource.build_image"
    ]
    image = "name:lambda_ansible"
    name  = "lambda_ansible_container"
}

resource "null_resource" "get_zip" {
    provisioner "local-exec" {
        command = "docker cp ${docker_container.amazon_linux.name}:/Ansible.zip ../Resources"
    }
}
