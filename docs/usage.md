# Usage

An [API HTTP REST](api.md) is implemented to manage the communication and the work of the Topology Exporter. 

All URIs are relative to the container address.

Rather than discovering applications and components during the parsing of the response and notifying all of them, the component does some filtering of this information and monitors only some specific applications. In order to start/stop monitoring an application, the Topology Exporter offers a REST API consisting of three methods:

## API endpoints

<table>
<tr style="background-color: blue; color: white">
<td><strong>Endpoint</strong></td>
<td><strong>HTTP Method</strong></td>
<td><strong>Request Body</strong></td>
<td><strong>Description</strong></td>
</tr>
<tr>
<td>/</td>
<td>GET</td>
<td></td>
<td>Healthcheck test</td>
</tr>
<tr>
<td>/applications/</td>
<td>GET</td>
<td></td>
<td>List of monitored applications</td>
</tr>
<tr>
<td>/applications/{app_id}</td>
<td>PUT</td>
<td>Application Manifest</td>
<td>Starts monitoring a new application</td>
</tr>
<tr>
<td>/applications/{app_id}</td>
<td>DELETE</td>
<td></td>
<td>Stops monitoring an application</td>
</tr>
</table>

## Topology changes notification to the application

The next sequence diagram illustrates how the ICOS meta-kernel layer notifies applications so they can react and be reconfigured automatically when there is any change on the deployment of the application.

Distributed applications may span across multiple clusters, either under the domain of one single controller or many. Although we could implement a protocol to share this information directly among ICOS Agents, potential race conditions during the deployment of the containers may complicate the solution. A simpler alternative to this coherence protocol is to control this information at the Controller level. 

Within the Controller, there are two potential sources from where to obtain this information. The first option is that every time that the Job Manager orders the deployment of some component, it notifies the change to the application. However, if there’s any error during the deployment, the information may be inconsistent. The second source of information that can be used is the Aggregator which gathers all the information collected through the telemetry infrastructure. Despite the delay for gathering the data, if the information is in the Aggregator, the components have already been deployed. Our solution leverages the information from the Aggregator.

![Sequence diagram](assets/images/diagram.svg "Sequence diagram")

The Aggregator is a reactive component; it collects the data and responds to queries done by other components; therefore, it won’t be aware of any changes in application deployments. In order to overcome this lack of proactiveness of the Aggregator a new component has been added to the ICOS Controller: the Topology Exporter. This component queries the application topology from the Aggregator and notifies the application about its current configuration.

To reduce the number of applications whose topology is being monitored, the Job Manager lets the Topology Exporter know when a new application is being deployed so it starts monitoring. Likewise, when the user requests to stop an application, it also notifies the Topology Exporter, so it stops monitoring the application deployment.

For exposing metaOS level information at application level, we created a data bus where the Topology Exporter publishes the deployed elements. Not all the applications require to know the topology of its deployment. Thus, it makes sense that application changes are only notified on a subscription basis. When a container of an application requiring to know that information starts, it can subscribe to a specific topic on this bus to receive the notifications.