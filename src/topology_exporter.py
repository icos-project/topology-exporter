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
import logging
from threading import Thread, Event
from aggregator_controller import poll
import json
from zenoh_client import send

# Retrieving environment variables
LOG_LEVEL = os.environ.get("LOG_LEVEL", "warning")
INTERVAL = float(os.environ.get("INTERVAL", "10"))

# Setting up logger
logging.basicConfig(level=LOG_LEVEL.upper())
logger = logging.getLogger(__name__)


class TopologyExporter(Thread):
    """Class to make periodic polls to the Aggregator and send through the Zenoh bus
    the deployment information of the pods of each monitored application."""

    def __init__(self):
        self._applications = {}
        self._end = Event()
        super().__init__()

    def update_app(self, app_instance: str, application: dict):
        self._applications[app_instance] = {
            app_component: {"application": application["name"], "clusters": {}}
            for app_component in application["components"]
        }

    def delete_app(self, app_instance: str):
        del self._applications[app_instance]

    def list_apps(self) -> dict:
        return {
            app_instance: {
                "name": next(iter(app_components.values()))["application"],
                "components": list(app_components),
            }
            for app_instance, app_components in self._applications.items()
        }

    def run(self):
        while not self._end.is_set():
            data = poll()

            logger.debug("Aggregator data:")
            logger.debug(data.model_dump_json(indent=2))

            for cluster_id, cluster in data.cluster.items():
                for node_id, node in cluster.node.items():
                    for pod_id, pod in node.pod.items():
                        for app_instance, workload in pod.workload.items():
                            if app_instance in self._applications:
                                self._applications[app_instance][
                                    workload.icos_app_component
                                ]["clusters"].setdefault(
                                    cluster_id,
                                    {"name": cluster.name, "pods": {}},
                                )[
                                    "pods"
                                ][
                                    pod_id
                                ] = {
                                    # pod.name = "app_instance__pod_name"
                                    "name": pod.name[len(app_instance) + 2 :],
                                    "ip": pod.ip,
                                }
                                if (
                                    pod.name[len(app_instance) : len(app_instance) + 2]
                                    != "__"
                                ):
                                    logger.warning(
                                        f"The \"name\" of the pod {pod_id} in the Aggregator must follow the format: 'app_instance__pod_name'."
                                    )

            logger.debug("Monitored application topologies:")
            logger.debug(json.dumps(self._applications, indent=2))

            for app_instance, app_components in self._applications.items():
                for app_component, deployment in app_components.items():
                    send(app_instance, app_component, deployment)
                    deployment["clusters"].clear()

            self._end.wait(INTERVAL)

    def stop(self):
        self._end.set()


# Initializing the TopologyExporter instance
topology_exporter = TopologyExporter()
