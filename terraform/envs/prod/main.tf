terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

module "prod_app" {
  source = "../../modules/container-service"

  service_name   = var.service_name
  image          = var.image
  internal_port  = 8080
  external_port  = var.external_port
  environment    = "prod"
  app_version    = var.app_version
  restart_policy = "always"
}
