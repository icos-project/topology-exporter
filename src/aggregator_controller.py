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
Aggregator Controller
"""

# Importing necessary libraries
import os
from pydantic import BaseModel, OnErrorOmit
import typing
import requests

# Retrieving environment variables
AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "True").lower() not in [
    "false",
    "no",
    "0",
]
AGG_URL = os.environ["AGG_URL"]

if AUTH_ENABLED:
    from keycloak_client import get_token


# Defining models for application topologies
class AggWorkload(BaseModel):
    icos_app_component: str


class AggPod(BaseModel):
    workload: typing.Dict[str, OnErrorOmit[AggWorkload]]


class AggNode(BaseModel):
    pod: typing.Dict[str, OnErrorOmit[AggPod]]


class AggCluster(BaseModel):
    node: typing.Dict[str, OnErrorOmit[AggNode]]


class AggData(BaseModel):
    cluster: typing.Dict[str, OnErrorOmit[AggCluster]]


def poll() -> AggData:
    """Poll the Aggregator."""
    response = requests.get(
        url=AGG_URL,
        headers={"Authorization": f"Bearer {get_token()}"} if AUTH_ENABLED else {},  # type: ignore
    )
    return AggData.model_validate(response.json())
