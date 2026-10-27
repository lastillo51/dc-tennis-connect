# DC Tennis Connect — Kubernetes Architecture

## 1. Purpose

This document describes the Kubernetes architecture used to deploy DC Tennis Connect during Phase 5.

The current environment uses a local kind cluster inside an Ubuntu VMware virtual machine.

The architecture is designed to support future application functionality and cloud deployment.

## 2. Current Environment

| Component | Configuration |
|---|---|
| Operating System | Ubuntu Desktop 26.04.1 LTS |
| Virtualization | VMware Workstation Pro |
| Kubernetes Distribution | kind |
| Cluster Name | dc-tennis |
| Cluster Nodes | One control-plane node |
| Container Runtime | containerd inside kind |
| Application | Python FastAPI |
| Application Replicas | One |
| Service Type | ClusterIP |
| Database | PostgreSQL remains in the local Docker Compose environment |

## 3. Kubernetes Components

### Deployment

The `dc-tennis-api` Deployment manages the FastAPI application.

Current configuration:

- One desired replica.
- Container image: `dc-tennis-connect:k8s-v1`.
- Container port: 8000.
- Readiness and liveness probes using `/health`.
- CPU and memory requests and limits.
- Restricted container security settings.

### Service

The `dc-tennis-api` Service provides stable internal networking.

- Type: ClusterIP.
- Service port: 8000.
- Target container port: 8000.
- Selector: `app=dc-tennis-api`.

### ConfigMap

The `dc-tennis-config` ConfigMap contains non-sensitive application settings.

Current settings:

- `APP_NAME`
- `APP_ENV`
- `LOG_LEVEL`
- `DEFAULT_TIMEZONE`

Not all settings are currently consumed by the FastAPI application.

### Secrets

Kubernetes Secret creation and deletion were tested during Phase 5.

The demonstration Secret was removed after verification.

No production credentials are stored in Kubernetes for the current application.

## 4. Security Architecture

The Deployment applies:

- Non-root execution with explicit numeric UID and GID.
- Disabled privilege escalation.
- Dropped Linux capabilities.
- RuntimeDefault seccomp profile.
- CPU and memory resource constraints.
- Health probes.

Additional security controls will be evaluated before public deployment.

## 5. Networking

The application uses a ClusterIP Service for internal access.

Local browser access is provided through temporary `kubectl port-forward` sessions.

The application is not publicly accessible through Kubernetes.

Future cloud deployment will require external routing, HTTPS, DNS, and appropriate network security.

## 6. Container Image Management

The FastAPI image is built locally using Docker and loaded into kind.

Current image tag:

`dc-tennis-connect:k8s-v1`

Future improvements include:

- Immutable image versioning.
- Container registry integration.
- Automated image publishing.
- Image digest pinning.
- Automated deployment workflows.

## 7. Database Architecture

PostgreSQL currently runs through Docker Compose and is not integrated with the Kubernetes Deployment.

Database integration will be addressed in a future development phase.

Future Kubernetes database options must consider persistence, backups, security, and operational complexity.

## 8. Repository Structure

```text
kubernetes/
├── kind/
│   └── cluster-config.yaml
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    └── local/
```

The base directory contains reusable Kubernetes resources.

Future overlays will support environment-specific configuration.

## 9. Operational Verification

The deployment has been verified using:

- Kubernetes node readiness.
- Deployment rollout status.
- Pod readiness.
- Service EndpointSlices.
- Container logs.
- Non-root execution checks.
- ConfigMap environment variable inspection.
- Port forwarding and API endpoint tests.
- Existing Pytest regression tests.

## 10. Known Limitations

- The cluster is local and not highly available.
- Only one application replica is deployed.
- The application is not publicly accessible.
- PostgreSQL is not integrated with the Kubernetes application.
- Authentication and player scheduling are not yet implemented.
- Container images are not automatically published to a registry.
- Kubernetes security scanning is not yet integrated into CI.
- Outstanding container vulnerability findings remain documented separately.

## 11. Future Enhancements

Potential improvements include:

- Kustomize environment overlays.
- Kubernetes namespace isolation.
- Kubernetes RBAC.
- NetworkPolicies.
- Read-only container filesystems.
- Automated manifest validation and security scanning.
- PostgreSQL integration.
- Cloud Kubernetes deployment.
- HTTPS ingress or Gateway API.
- Monitoring and observability.

## 12. Related Documentation

- `docs/architecture/system-overview.md`
- `docs/security/security-policy.md`
- `docs/runbooks/security-findings.md`
- `.github/workflows/security-ci.yml`
- `docker/Dockerfile`