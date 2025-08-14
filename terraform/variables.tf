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