output registry_name {
    value = google_artifact_registry_repository.docker_repo.name
}

output cloud_run_url {
    value = google_cloud_run_v2_service.default.uri
}

output user_upload_bucket {
    value = google_storage_bucket.user_upload_bucket.name
}

output project_id {
  value = data.google_client_config.this.project
}

output region {
  value = data.google_client_config.this.region
}

