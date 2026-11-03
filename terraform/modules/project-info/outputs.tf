output "project_info_file" {
  description = "Path to the generated project information file."

  value = var.enable_project_file ? (
    local_file.project_info[0].filename
  ) : null
}