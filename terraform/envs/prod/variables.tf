variable "service_name" {
  description = "Container name for production service"
  type        = string
  default     = "platform-api-prod"
}

variable "image" {
  description = "Docker image to deploy"
  type        = string
  default     = "cloud-platform-api:test"
}

variable "external_port" {
  description = "Host port exposed for production"
  type        = number
  default     = 8080
}

variable "app_version" {
  description = "Version tag or git commit"
  type        = string
  default     = "v0.1.0-prod"
}
