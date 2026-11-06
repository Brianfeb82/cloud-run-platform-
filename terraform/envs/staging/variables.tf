variable "service_name" {
  description = "Container name for staging service"
  type        = string
  default     = "platform-api-staging"
}

variable "image" {
  description = "Docker image to deploy"
  type        = string
  default     = "cloud-platform-api:test"
}

variable "external_port" {
  description = "Host port exposed for staging"
  type        = number
  default     = 8081
}

variable "app_version" {
  description = "Version tag or git commit"
  type        = string
  default     = "v0.1.0-staging"
}
