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
FastAPI Server
"""

# Importing necessary libraries
import os
from fastapi import FastAPI, Depends, HTTPException, status, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from pydantic import BaseModel, ValidationError
import typing
import yaml
from topology_exporter import topology_exporter
from uvicorn import run

# Retrieving environment variables
AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "True").lower() not in [
    "false",
    "no",
    "0",
]
PERM_REGISTER = os.environ.get("PERM_REGISTER", "app#Register")
PERM_READ = os.environ.get("PERM_READ", "app#Read")

# Working with Keycloak if Auth enabled
if AUTH_ENABLED:
    from keycloak_client import is_valid

# Initialising FastAPI app
app = FastAPI()

# Initialising security scheme for authentication
security = HTTPBearer()


# Check token permissions
async def user_authorization(
    security_scopes: SecurityScopes,
    auth_credentials: HTTPAuthorizationCredentials = Depends(security),
):
    logged, allowed = is_valid(auth_credentials.credentials, security_scopes.scopes)  # type: ignore
    if not logged:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )


# Defining route for health check
@app.get("/")
async def health_check():
    return {"message": "Topology Exporter is working properly"}


# Defining models for application descriptor
class AppComponent(BaseModel):
    name: str


class AppDescriptor(BaseModel):
    name: str
    components: typing.List[AppComponent]


# Defining route to start monitoring an application
@app.put(
    "/applications/{app_instance}",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/x-yaml": {"schema": AppDescriptor.model_json_schema()}
            },
            "required": True,
        }
    },
    dependencies=(
        [Security(user_authorization, scopes=[PERM_REGISTER])] if AUTH_ENABLED else []
    ),
)
async def update_application(app_instance: str, request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid YAML"
        )
    try:
        descriptor = AppDescriptor.model_validate(data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(include_url=False),
        )

    app_components = [component.name for component in descriptor.components]
    topology_exporter.update_app(app_instance, app_components)

    return {app_instance: app_components}


# Defining route to stop monitoring an application
@app.delete(
    "/applications/{app_instance}",
    dependencies=(
        [Security(user_authorization, scopes=[PERM_REGISTER])] if AUTH_ENABLED else []
    ),
)
async def delete_application(app_instance: str):
    topology_exporter.delete_app(app_instance)


# Defining route to get current monitored applications
@app.get(
    "/applications",
    dependencies=(
        [Security(user_authorization, scopes=[PERM_READ])] if AUTH_ENABLED else []
    ),
)
async def list_applications():
    return topology_exporter.list_apps()


# Running Topology Exporter and FastAPI app server
if __name__ == "__main__":
    topology_exporter.start()

    run(app=app, host="0.0.0.0", port=80)

    topology_exporter.stop()
