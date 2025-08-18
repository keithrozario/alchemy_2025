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

provider "google-beta" {
  region = var.google_cloud_region
}
provider "google" {
  region = var.google_cloud_region
}

data "google_client_config" "this" {
  provider = google
}