# Deployment

Topology Exporter can be executed in different ways:

## Python

**Requirements**: [python3.10](https://www.python.org/downloads/release/python-3100/) and [pip3](https://pip.pypa.io/en/stable/) dependencies:

  - [eclipse_zenoh](https://pypi.org/project/eclipse-zenoh/)
  - [fastapi](https://pypi.org/project/fastapi/)
  - [python-keycloak](https://pypi.org/project/python-keycloak/)
  - [pyyaml](https://pypi.org/project/PyYAML/)
  - [requests](https://pypi.org/project/requests/)
  - [uvicorn](https://pypi.org/project/uvicorn/)

**Entry point**: [fastapi_server.py](https://github.com/icos-project/topology-exporter/blob/release/src/fastapi_server.py)

## Docker Compose

**Requirement**: [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

**Example**: [compose.yaml](https://github.com/icos-project/topology-exporter/blob/release/tests/compose.yaml)

## Helm Chart

**Requirement**: [Helm](https://helm.sh/docs/intro/install/)

**Files**: [chart](https://github.com/icos-project/topology-exporter/tree/release/chart/)