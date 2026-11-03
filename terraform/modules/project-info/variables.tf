variable "project_name" {
  description = "Name of the application project."
  type        = string

  validation {
    condition     = length(trimspace(var.project_name)) > 0
    error_message = "Project name cannot be empty."
  }
}

variable "environment" {
  description = "Target environment."
  type        = string

  validation {
    condition = contains(
      ["local", "dev", "staging", "prod"],
      var.environment
    )
    error_message = "Invalid environment."
  }
}

variable "project_phase" {
  description = "Current project development phase."
  type        = string
}

variable "enable_project_file" {
  description = "Whether to create the project information file."
  type        = bool
  default     = true
}

variable "output_directory" {
  description = "Absolute directory where the generated file will be created."
  type        = string

  validation {
    condition     = length(trimspace(var.output_directory)) > 0
    error_message = "Output directory cannot be empty."
  }
}