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
Application Instance Component mock
"""

# Importing necessary libraries
import os
import json
import zenoh
from signal import pause

# Retrieving environment variables
ZENOH_EP = os.environ["ZENOH_EP"]
ICOS_APP_INSTANCE = os.environ["ICOS_APP_INSTANCE"]
ICOS_APP_COMPONENT = os.environ["ICOS_APP_COMPONENT"]

# Setting up Zenoh configuration
conf = zenoh.Config()

# Setting up Zenoh mode
conf.insert_json5("mode", json.dumps("client"))

# Setting up Zenoh endpoints
conf.insert_json5("connect/endpoints", json.dumps([ZENOH_EP]))

# Opening Zenoh session
session = zenoh.open(conf)


# Defining Zenoh subscriber handler
def listener(sample):
    print(sample.payload.to_string())


# Listening Application Instance Component messages from Zenoh bus
if __name__ == "__main__":
    sub = session.declare_subscriber(
        key_expr=ICOS_APP_INSTANCE + "/" + ICOS_APP_COMPONENT, handler=listener
    )

    try:
        pause()
    except KeyboardInterrupt:
        pass

    sub.undeclare()
    session.close()
