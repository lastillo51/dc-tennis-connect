module "project_info" {
  source = "../../modules/project-info"

  project_name        = var.project_name
  environment         = var.environment
  project_phase       = var.project_phase
  enable_project_file = var.enable_project_file

  output_directory = path.module
}