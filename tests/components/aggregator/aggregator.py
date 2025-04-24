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
Aggregator mock
"""

# Importing necessary libraries
import os
from fastapi import FastAPI
import json
from uvicorn import run

# Retrieving environment variables
JSON_FILE = os.environ.get("JSON_FILE", "aggregator.json")

# Initializing FastAPI app
app = FastAPI()


# Defining default route
@app.get("/")
async def default():
    with open(JSON_FILE, "r") as file:
        return json.load(file)


# Running FastAPI app
if __name__ == "__main__":
    run(app=app, host="0.0.0.0")
