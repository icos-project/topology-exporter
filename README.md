# Topology Exporter

This repository contains source code of the Topology Exporter component for the Meta-kernel layer of the ICOS project. The purpose of this component is to notify application-level containers about events related to the deployment of the application. Thus, application components can react to those events and change their configuration. This is especially needed for distributed computing libraries with no automatic resource discovery.

## Repository organization

The repository contains the following directories and files:

- `chart/`: files describing the Helm Chart of the component.
- `docs/`: files for building the documentation of the component.
- `src/`: source code of the component.
- `tests/`: source code, configuration files and scripts necessary to create a deployment that allows to validate the behaviour of the component.
- `Dockerfile`: instructions to build a docker image of the component.
- `icos-certificate.crt`: ICOS CA root certificate.
- `LICENSE`: conditions to use, change and distribute the software included in this repository.
- `README.md`: this guide.

Find further information regarding the source code and the testing process in the `README.md` files within the corresponding folder.

## Service deployment

You can use Docker to run the service. Follow these commands:

```bash
docker build -t icos/topology-exporter .
docker run --env-file <path-to-env-file> -p <host-port>:80 icos/topology-exporter
```

This will build a Docker image tagged as *topology-exporter* and run a container with the component.

The container offers several environment variables to configure the component general setup:

- **ZENOH_EP**: Zenoh endpoint where to publish the topology of the applications.  
- **AGG_URL**: Aggregator address where to query topology data.  
- **INTERVAL**: time lapse in seconds between topology updates (*default*: `10`).  
- **LOG_LEVEL**: level of logging (*options*: `debug`, `info`, `warning`, `error`, `critical`; *default*: `warning`).  
- **AUTH_ENABLED**: enable authentication and authorizarion (*options*: `True`, `False`; *default*: `True`).  

When authentication and authorizarion are enabled, other environment variables come into play:

- **PERM_REGISTER**: permission scope for registering and unregistering application monitorization (*default*: `app#Register`).  
- **PERM_READ**: permission scope for listing current monitoring applications (*default*: `app#Read`).  
- **IAM_URL**: Keycloak server address where to validate tokens and check their permissions.  
- **IAM_REALM**: Keycloak realm name.  
- **IAM_ID**: Keycloak client identificator.  
- **IAM_SECRET**: Keycloak secret key.  

Remember to replace the `icos-certificate.crt` file with the ICOS CA root certificate.

## REST API

### Healthcheck

- **Path**: `/`
- **Method**: GET

### Start monitoring application

- **Path**: `/applications/{app_instance_id}`
- **Method**: PUT
- **Payload**: application descriptor

### Stop monitoring application

- **Path**: `/applications/{app_instance_id}`
- **Method**: DELETE

### List monitored applications

- **Path**: `/applications`
- **Method**: GET

## ICOS integration

Sequence diagram showing the behaviour of the Topology Exporter component inside the Meta-kernel layer of the ICOS project:

![Sequence diagram](docs/assets/images/diagram.svg "Sequence diagram")

# Legal

The Topology Exporter is released under the Apache 2.0 license.
Copyright © 2022-2025 Barcelona Supercomputing Center (BSC). All rights reserved.

🇪🇺 This work has received funding from the European Union's HORIZON research and innovation programme under grant agreement No. 101070177.