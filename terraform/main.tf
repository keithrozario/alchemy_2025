variable image_name {
    type = string
    default = "alchemy-loan-app"
}

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "${var.stack_name}-cloudrun-app"
  description   = "Cloudrun Repository for ${var.stack_name}"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false ## allows us to redeploy :latest over and over
  }

  provisioner "local-exec" {
    command = "gcloud builds submit --tag ${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.docker_repo.name}/${var.image_name}"
    working_dir = "../"
  }
}

output registry_name {
    value = google_artifact_registry_repository.docker_repo.name
}

data "google_artifact_registry_docker_image" "cloud_run_image" {
  depends_on    = [google_artifact_registry_repository.docker_repo]
  location      = google_artifact_registry_repository.docker_repo.location
  repository_id = google_artifact_registry_repository.docker_repo.repository_id
  image_name    = "${var.image_name}:latest"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "${var.stack_name}-cloudrun-service"
  location = var.region
  deletion_protection = false
  # Allow external load balancer access
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = data.google_artifact_registry_docker_image.cloud_run_image.self_link
      ports {
        container_port = 8080
      }
    }

  }
}