output "container_id" {
  description = "Docker container ID"
  value       = docker_container.app.id
}

output "service_name" {
  description = "Service name"
  value       = docker_container.app.name
}

output "endpoint" {
  description = "Local HTTP endpoint"
  value       = "http://127.0.0.1:${var.external_port}"
}
