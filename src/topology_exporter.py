#!/usr/bin/env python3
#
#  Topology Exporter
#  Copyright © 2022-2025 Barcelona Supercomputing Center (BSC)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  This work has received funding from the European Union's HORIZON research
#  and innovation programme under grant agreement No. 101070177.
#
# -*- coding: utf-8 -*-

"""
Topology Exporter
"""

# Importing necessary libraries
import os
from threading import Thread, Event
from aggregator_controller import poll
import json
from zenoh_client import send

# Retrieving environment variables
INTERVAL = float(os.environ.get("INTERVAL", "10"))


class TopologyExporter(Thread):
    """Class to make periodic polls to the Aggregator and send through the Zenoh bus the location of the pods of each monitored application."""

    def __init__(self):
        self._applications = {}
        self._end = Event()
        super().__init__()

    def update_app(self, app_instance: str, app_components: list[str]):
        self._applications[app_instance] = {
            app_component: {} for app_component in app_components
        }

    def delete_app(self, app_instance: str):
        del self._applications[app_instance]

    def list_apps(self) -> dict[str, list[str]]:
        return {
            app_instance: list(app_components)
            for app_instance, app_components in self._applications.items()
        }

    def run(self):
        while not self._end.is_set():
            data = poll()

            # print("Aggregator data:")
            # print(data.model_dump_json(indent=2))

            for cluster_id, cluster in data.cluster.items():
                for node_id, node in cluster.node.items():
                    for pod_id, pod in node.pod.items():
                        for app_instance, workload in pod.workload.items():
                            if app_instance in self._applications:
                                self._applications[app_instance][
                                    workload.icos_app_component
                                ].setdefault(cluster_id, []).append(pod_id)

            # print("Monitored application topologies:")
            # print(json.dumps(self._applications, indent=2))

            for app_instance, app_components in self._applications.items():
                for app_component, clusters in app_components.items():
                    send(app_instance, app_component, clusters)
                    clusters.clear()

            self._end.wait(INTERVAL)

    def stop(self):
        self._end.set()


# Initializing the TopologyExporter instance
topology_exporter = TopologyExporter()
