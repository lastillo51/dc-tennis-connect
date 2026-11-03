variable "project_name" {
  description = "Name of the application project."
  type        = string
  default     = "DC Tennis Connect"

  validation {
    condition     = length(trimspace(var.project_name)) > 0
    error_message = "Project name cannot be empty."
  }
}

variable "environment" {
  description = "Target deployment environment."
  type        = string
  default     = "local"

  validation {
    condition     = contains(["local", "dev", "staging", "prod"], var.environment)
    error_message = "Environment must be local, dev, staging, or prod."
  }
}

variable "project_phase" {
  description = "Current development phase."
  type        = string
  default     = "Phase 6 - Terraform"
}

variable "enable_project_file" {
  description = "Whether Terraform should create the local project information file."
  type        = bool
  default     = true
}