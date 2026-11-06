terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

resource "docker_container" "app" {
  name    = var.service_name
  image   = var.image
  restart = var.restart_policy

  ports {
    internal = var.internal_port
    external = var.external_port
  }

  env = [
    "ENVIRONMENT=${var.environment}",
    "SERVICE_NAME=${var.service_name}",
    "APP_VERSION=${var.app_version}",
    "PORT=${var.internal_port}"
  ]

  # Labels for tracking and monitoring
  labels {
    label = "environment"
    value = var.environment
  }
  labels {
    label = "managed_by"
    value = "terraform"
  }
}
