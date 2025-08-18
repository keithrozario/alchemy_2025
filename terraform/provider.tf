# Backend is in a separate project
terraform {
  required_providers {
    google-beta = {
      source = "hashicorp/google-beta"
      version = "6.32.0"
    }
    google = {
      source = "hashicorp/google"
      version = "6.32.0"
    }
  }
}
data "google_project" "project" {}

provider "google-beta" {
  region  = var.region
  project = var.project_id
}
provider "google" {
  region  = var.region
  project = var.project_id
}

data "google_client_config" "this" {
  provider = google
}

