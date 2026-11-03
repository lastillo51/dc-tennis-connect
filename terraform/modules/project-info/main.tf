resource "local_file" "project_info" {
  count = var.enable_project_file ? 1 : 0

  filename = "${var.output_directory}/dc-tennis-project-info.txt"

  content = <<-EOT
    ${var.project_name}
    Terraform Local Infrastructure Exercise

    Project: ${var.project_name}
    Environment: ${var.environment}
    Managed By: Terraform
    Purpose: Infrastructure as Code Learning
    Project Phase: ${var.project_phase}
  EOT

  file_permission = "0644"
}