resource "google_artifact_registry_repository" "docker_repo" {
  location      = data.google_client_config.this.region
  repository_id = "${var.stack_name}-cloudrun-app"
  description   = "Repository for ${var.stack_name}"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false ## allows us to redeploy :latest over and over
  }

  provisioner "local-exec" {
    command = <<EOF
    gcloud builds submit \
    --tag ${data.google_client_config.this.region}-docker.pkg.dev/${data.google_client_config.this.project}/${google_artifact_registry_repository.docker_repo.name}/${var.image_name_and_tag} \
    --region ${data.google_client_config.this.region}
    EOF
    working_dir = "../"
  }
}

data "google_artifact_registry_docker_image" "cloud_run_image" {
  depends_on    = [google_artifact_registry_repository.docker_repo]
  location      = google_artifact_registry_repository.docker_repo.location
  repository_id = google_artifact_registry_repository.docker_repo.repository_id
  image_name    = "${var.image_name_and_tag}"
}

resource "random_string" "random" {
  length           = 8
  upper            = false
  special          = false
}

 resource "google_storage_bucket" "user_upload_bucket" {
    name          = "${var.stack_name}-${random_string.random.result}"
    location      = data.google_client_config.this.region
    uniform_bucket_level_access = true
    force_destroy = true 
}

/*
Creates a Service account with the right permissions for Cloudrun
*/

resource "google_service_account" "cloudrun_service_account" {
  account_id   = "${var.stack_name}-service-account"
  display_name = "Service Account for Alchemy"
  description  = "This service account is used by My Application."
}

resource "google_project_iam_member" "cloudrun_service_account" {
  for_each = toset([
    "roles/storage.objectCreator",
    "roles/aiplatform.user",
    "roles/bigquery.dataEditor"
  ])
  project = data.google_client_config.this.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloudrun_service_account.email}"
}


/*
Deploys CloudRun instance and enables a public access over the internet UNauthenticated
*/

resource "google_cloud_run_v2_service" "default" {
  name     = "${var.stack_name}-webapp"
  location = data.google_client_config.this.region
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.cloudrun_service_account.email
    scaling {
      min_instance_count = 1 ## keep 1 always on.
      max_instance_count = 2 
    }
    containers {
      image = data.google_artifact_registry_docker_image.cloud_run_image.self_link
      resources {
        limits = {
          "cpu" = "1"
          "memory" = "2Gi"
        }
      }
      ports {
        container_port = 8080
      }
      env {
        name = "GOOGLE_CLOUD_PROJECT"
        value = data.google_client_config.this.project
      }
      env {
        name = "LOAN_GCS_BUCKET"
        value = google_storage_bucket.user_upload_bucket.name
      }
      env {
        name = "BQ_TABLE"
        value = "placeholder" # currently we don't have a BQ table
      }
      env {
        name = "GRPC_VERBOSITY"
        value = "ERROR"
      }
      env {
        name = "GLOG_minloglevel"
        value = "2"
      }
      env {
        name = "GOOGLE_GENAI_USE_VERTEXAI"
        value = "TRUE"
      }
      env {
        name = "GOOGLE_CLOUD_LOCATION"
        value = data.google_client_config.this.region
      }
    }
    max_instance_request_concurrency = 2
  }
}

resource "google_cloud_run_service_iam_binding" "default" {
  location = google_cloud_run_v2_service.default.location
  service  = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}
