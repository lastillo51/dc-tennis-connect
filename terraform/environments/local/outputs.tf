output "project_info_file" {
  description = "Path to the generated project information file."
  value       = module.project_info.project_info_file
}

output "deployment_environment" {
  description = "Environment selected for this deployment."
  value       = var.environment
}

output "project_name" {
  description = "Configured project name."
  value       = var.project_name
}