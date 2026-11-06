output "service_name" {
  description = "Production service container name"
  value       = module.prod_app.service_name
}

output "endpoint" {
  description = "Production service endpoint URL"
  value       = module.prod_app.endpoint
}
