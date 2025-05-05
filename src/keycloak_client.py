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
Keycloak Client
"""

# Importing necessary libraries
import os
from keycloak import KeycloakOpenID
from time import time

# Retrieving environment variables
IAM_URL = os.environ["IAM_URL"]
IAM_REALM = os.environ["IAM_REALM"]
IAM_ID = os.environ["IAM_ID"]
IAM_SECRET = os.environ["IAM_SECRET"]
INTERVAL = float(os.environ.get("INTERVAL", "10"))

# Initializing Keycloak OpenID
keycloak_openid = KeycloakOpenID(
    server_url=IAM_URL,
    realm_name=IAM_REALM,
    client_id=IAM_ID,
    client_secret_key=IAM_SECRET,
    verify="/etc/ssl/certs/icos-extra-certs.crt",
)

# Initializing expire time
expire_time = 0


def is_valid(token: str, permissions: list[str]) -> tuple[bool, bool]:
    """Validate token and its permissions."""
    status = keycloak_openid.has_uma_access(token, permissions)
    return status.is_logged_in, status.is_authorized


def get_token() -> str:
    """Get current token."""
    global token, expire_time
    if time() > expire_time:
        token = keycloak_openid.token(grant_type="client_credentials")
        expires_in = float(token["expires_in"])
        expire_time = time() + expires_in
        if INTERVAL < expires_in:
            expire_time -= INTERVAL
    return token["access_token"]  # type: ignore
