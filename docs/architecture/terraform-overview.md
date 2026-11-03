# DC Tennis Connect — Terraform Architecture

## 1. Purpose

This document describes the Terraform Infrastructure as Code architecture introduced during Phase 6.

The initial implementation focuses on local infrastructure management, reusable Terraform modules, and automated security validation.

The architecture is designed to support future cloud deployment without requiring major restructuring.

## 2. Current Implementation

| Component | Implementation |
|---|---|
| Infrastructure Tool | Terraform |
| Configuration Language | HashiCorp Configuration Language (HCL) |
| Current Environment | Local Ubuntu development VM |
| Terraform Provider | HashiCorp Local |
| State Backend | Local |
| Reusable Module | `project-info` |
| Security Scanner | Trivy |
| CI/CD | GitHub Actions |
| Cloud Infrastructure | Not yet provisioned |

## 3. Repository Structure

```text
terraform/
├── environments/
│   ├── local/
│   ├── dev/
│   ├── prod/
│   └── cloud/
└── modules/
    └── project-info/
```

### Environment Directories

- `local/` contains the current Terraform root configuration.
- `dev/` is reserved for future development infrastructure.
- `prod/` is reserved for future production infrastructure.
- `cloud/` is reserved for cloud infrastructure experimentation.

The relationship between `cloud/`, `dev/`, and `prod/` will be refined when a cloud provider and deployment architecture are selected.

### Reusable Modules

The `modules/` directory contains reusable Terraform components.

The initial `project-info` module creates a local project information file using configurable inputs.

Future modules may manage cloud networking, application hosting, databases, and other infrastructure.

## 4. Root Module

The local root module is located at:

`terraform/environments/local/`

It is responsible for:

- Defining provider requirements.
- Selecting environment-specific variables.
- Calling reusable modules.
- Exposing relevant outputs.
- Maintaining Terraform state.

## 5. Project Information Module

The reusable module is located at:

`terraform/modules/project-info/`

### Inputs

| Variable | Purpose |
|---|---|
| `project_name` | Application project name |
| `environment` | Target environment |
| `project_phase` | Development phase |
| `enable_project_file` | Controls whether the resource exists |
| `output_directory` | Directory for the generated file |

### Outputs

| Output | Purpose |
|---|---|
| `project_info_file` | Path to the generated project information file |

The module was tested using multiple environment values.

## 6. Terraform State Management

The current implementation uses local Terraform state.

State files and generated provider directories are excluded from Git.

The provider dependency lock file is tracked for reproducibility.

Terraform state may contain sensitive resource attributes and must be protected.

Before cloud deployment, the project will evaluate remote state storage with appropriate encryption, access controls, locking, and recovery capabilities.

## 7. Infrastructure Lifecycle

The following Terraform operations were tested:

1. `terraform init`
2. `terraform fmt`
3. `terraform validate`
4. `terraform plan`
5. `terraform apply`
6. `terraform state list`
7. `terraform output`
8. `terraform destroy`

All demonstration resources were removed after verification.

## 8. Security Controls

The current implementation includes:

- Terraform formatting checks.
- Terraform configuration validation.
- Trivy infrastructure configuration scanning.
- Git exclusions for state and local variable files.
- Manual review of infrastructure changes.
- Automated validation through GitHub Actions.

Trivy IaC findings are currently report-only.

Security enforcement thresholds will be reviewed as cloud infrastructure is introduced.

## 9. GitHub Actions Integration

The existing security CI workflow includes a Terraform IaC job.

The job performs:

- Terraform installation.
- Formatting verification.
- Provider and module initialization.
- Configuration validation.
- Trivy IaC security scanning.

The CI workflow does not provision or destroy infrastructure.

Cloud credentials are not required for the current configuration.

## 10. Known Limitations

- No cloud infrastructure has been provisioned.
- The current module manages only a demonstration local file.
- Terraform state is stored locally.
- Terraform modules have not yet been used to provision cloud resources.
- Infrastructure security checks do not guarantee production readiness.
- Public application hosting and HTTPS are not yet configured.

## 11. Future Enhancements

Planned improvements include:

- Selecting a cloud hosting provider.
- Defining cloud infrastructure modules.
- Introducing environment-specific configurations.
- Implementing secure remote state management.
- Adding infrastructure deployment approval controls.
- Evaluating automated infrastructure deployment.
- Integrating cloud infrastructure with the application.
- Expanding infrastructure security scanning.
- Implementing public HTTPS access and monitoring.

## 12. Related Documentation

- `README.md`
- `docs/architecture/system-overview.md`
- `docs/architecture/kubernetes-overview.md`
- `docs/security/security-policy.md`
- `docs/runbooks/security-findings.md`
- `.github/workflows/security-ci.yml`