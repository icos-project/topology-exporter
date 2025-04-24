# Topology Exporter tests

This folder contains all the necessary scripts and source code for testing the functionality of the Topology Exporter.

The respository is organized in 4 main directories:

- `components/`: folder containing the mocks for other components:
    - **Aggregator**: expose the content of a JSON file to a REST API path.
    - **Application**: subscribes to an application instance component Zenoh key and prints what receives to the standard output.
- `descriptors/`: application descriptor YAMLs used for the tests.
- `topologies/`: deployment topologies for the Aggregator used for the tests.
- `results/`: expected outputs from the different application instance component pods of the tests.

## Unit test

To verify the correctness of the Topology Exporter, execute the following:

```bash
./tests.sh
```

This bash script will run different tests to verify if Topology Exporter meets its functional requirements.  
If any test fails, it will exit prematurely, printing the expected and the actual results of the pertinent application component replica.

## Custom test

To run a simple custom test, you can follow these steps:

### 1. Deploy services

```bash
docker compose up --build; docker compose down
```

Docker Compose will build and run into containers those Docker images defined in the `compose.yaml` file.  
Whenever you want to quit, just press `Ctrl+C` and it will stop and remove all the containers.

### 2. Set topology

```bash
cp topologies/aggregator.json components/aggregator/aggregator.json
```

On another shell, change the content of the JSON file that Aggregator mock reads.

### 3. Start monitoring an application

```bash
curl localhost/applications/app_instance --upload-file descriptors/application.yaml
```

Upload to the Topology Exporter the application descriptor of the instance you want to monitor.  
Whenever you want to stop monitoring an application instance, just run:

```bash
curl -X DELETE localhost/applications/app_instance
```

### 4. Check applications outputs

Check on the shell running the services (*see step 1*) if they are printing what you expected.  
In this case, `application-1` should print the same as `results/output.json` file content.