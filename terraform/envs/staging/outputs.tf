output "service_name" {
  description = "Staging service container name"
  value       = module.staging_app.service_name
}

output "endpoint" {
  description = "Staging service endpoint URL"
  value       = module.staging_app.endpoint
}
