variable "service_name" {
  description = "Name of the container service"
  type        = string
}

variable "image" {
  description = "Docker image name and tag"
  type        = string
}

variable "internal_port" {
  description = "Port the container listens on internally"
  type        = number
  default     = 8080
}

variable "external_port" {
  description = "Host port mapped to the container"
  type        = number
}

variable "environment" {
  description = "Environment name (e.g. staging, prod)"
  type        = string
}

variable "app_version" {
  description = "Version string or Git commit SHA"
  type        = string
  default     = "0.1.0-dev"
}

variable "restart_policy" {
  description = "Container restart policy"
  type        = string
  default     = "unless-stopped"
}
