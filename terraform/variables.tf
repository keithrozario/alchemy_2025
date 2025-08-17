variable "stack_name" {
    type=string
    description = "Description of purpose of resources deployed here. We will prepend the stack name to most resources deployed"
    default = "alchemy-loan"
}

variable "region" {
    type = string
    default = "us-central1"
}

variable "project_id" {
    type = string
    default = "default-krozario"
}

variable image_name_and_tag {
    type = string
    description = "Name of container image and tag to deploy CloudRun instance from"
    default = "alchemy-loan-app-keith:latest"
}
