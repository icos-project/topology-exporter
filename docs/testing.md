# Testing and validation

The Topology Exporter component contains several [unit tests](https://github.com/icos-project/topology-exporter/tree/release/tests/) to verify its proper behavior. To facilitate the verification of the component, the other component of the Meta-kernel layer on which the Topology Exporter depends (Aggregator) has been mocked and a new service that is able to return a pre-made topology has been developed. Upon a query for the status of the infrastructure, this mocked aggregator reads the desired status of the testbed from a file; therefore, by dynamically changing the content of the file, we can simulate the status of the infrastructure.

The unit tests for the component starts a docker compose that starts and creates several containers:

  1. Aggregator mock
  2. Topology Exporter
  3. Container to deploy Zenoh acting as the bus to report topology changes to the application
  4. Containers emulating a deployed application

These application containers subscribe to the bus for notifications on a specific application deployment and component, and whatever notification is received is printed to the standard output.

The conducted test deploys this testing infrastructure and submits several requests to the Topology Exporter, so it starts monitoring several applications. Once the test has been set up, it continues by changing several times the file read by the mock Aggregator, and, on every change, it checks the logs of the application containers to verify that they received the desired notifications.