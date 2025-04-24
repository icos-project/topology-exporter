# Topology Exporter

## Overwiew

The Topology Exporter is a component of the Meta-kernel layer architecture. Its purpose is to notify application-level containers about events related to the deployment of the application. Thus, application components can react to those events and change their configuration. This is especially needed for distributed computing libraries with no automatic resource discovery. An example of this kind of library is the distributed and parallel execution component. Its agent-based runtime system orchestrates the execution of many tasks on top of a distributed infrastructure; however, the neighbouring agents must be manually set up by the application deployer.

Rather than keeping an internal representation of the topology of each application and updating it upon being notified of the elements deployed or undeployed for each application, the Topology Exporter periodically obtains the topology of the system from the Aggregator. Upon receiving the response for the topology query, the Topology Exporter parses its content to discover the list of deployed elements corresponding to each component of each monitored instance of the application. When the whole response has been parsed, the list of elements is published through a Zenoh bus so that any application subscribed onto it can be notified about changes in its topology.

## Development

Topology Exporter documentation shows how to [use](usage.md) it, different ways to [deploy](deployment.md) the component, and how to [test and validate](testing.md) its correctness.