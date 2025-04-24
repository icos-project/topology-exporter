# Topology Exporter architecture

The Topology Exporter is a component of the Meta-Kernel layer of ICOS. Its purpose is to notify application-level containers about events related to the deployment of the application. Thus, application components can react to those events and change their configuration. This is especially needed for distributed computing libraries with no automatic resource discovery.

Rather than keeping an internal representation of the topology of each application and updating it upon being notified of the elements deployed or undeployed for each application, the Topology Exporter periodically obtains the topology of the system from the Aggregator. Upon receiving the response for the topology query, the Topology Exporter parses its content to discover the list of deployed elements corresponding to each component of each monitored instance of the application. When the whole response has been parsed, the list of elements is published through a Zenoh bus so that any application subscribed onto it can be notified about changes in its topology. Rather than discovering applications and components during the parsing of the response and notifying all of them, the component does some filtering of this information and monitors only some specific applications.

The language used for implementing the Topology Exporter component is Python, and it's composed of 5 modules.

## Modules

Brief description of the modules that make up the Topology Exporter architecture:

- **Topology Exporter**: contains the main class that is responsible of polling the Aggregator and sending the locations of each monitored application instance components through the Zenoh bus.
- **FastAPI Server**: defines a REST API for starting and stopping monitoring application instances and listing them all.
- **Aggregator Controller**: requests the Aggregator for the whole deployment topology and parses their response.
- **Zenoh Client**: puts into Zenoh bus the location of the pods of an application instance component.
- **Keycloak Client**: manage the authentication of the component and the verification of user tokens inside the ecosystem.