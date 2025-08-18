variable "google_cloud_region"{
    type=string
    description="Region to deploy into"
    default="us-central1"
}

variable "stack_name" {
    type=string
    description = "We will prepend the stack name to most resources deployed"
    default = "alchemy-loan"
}

variable image_name_and_tag {
    type = string
    description = "Name of container image and tag to deploy CloudRun instance from"
    default = "alchemy-loan:latest"
}
