#
# Copyright 2026 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.patch_sandbox_request import PatchSandboxRequest
from ...models.sandbox import Sandbox
from ...types import Response


def _get_kwargs(
    sandbox_id: str,
    *,
    body: PatchSandboxRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/sandboxes/{sandbox_id}".format(
            sandbox_id=quote(str(sandbox_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Sandbox | None:
    if response.status_code == 200:
        response_200 = Sandbox.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | Sandbox]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchSandboxRequest,
) -> Response[ErrorResponse | Sandbox]:
    r"""Patch sandbox metadata

     Update sandbox metadata using JSON Merge Patch semantics (RFC 7396).

    The request body is a partial Sandbox representation. Only `metadata` is
    mutable; other top-level fields are rejected with 400.

    **Merge Patch rules for `metadata`:**
    | Request body key/value | Behavior |
    |---|---|
    | `\"key\": \"value\"` | Add or replace the key |
    | `\"key\": null` | Delete the key (silently ignored if key does not exist) |
    | key absent | Keep current value (no change) |
    | Empty `{}` or `{\"metadata\": {}}` | No-op, returns current metadata |

    Metadata keys and values must comply with Kubernetes label rules:
    - Keys must be valid DNS label names or prefixed DNS subdomains
    - Keys with the `opensandbox.io/` prefix are reserved and rejected
    - Values must be 63 characters or less, matching `[A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?`

    This operation does not restart or recreate the sandbox container/pod.

    Args:
        sandbox_id (str):
        body (PatchSandboxRequest): JSON Merge Patch (RFC 7396) request body for partially
            updating a sandbox.

            Only the `metadata` field is mutable. The top-level object follows merge-patch
            semantics: `metadata` present replaces the metadata sub-object (merge-patched),
            `metadata` absent leaves it unchanged. Other top-level fields are rejected.

            Within `metadata`, the same merge-patch rules apply:
            - Present keys with non-null values add or replace
            - Keys with `null` values are deleted
            - Absent keys are left unchanged

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Sandbox]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchSandboxRequest,
) -> ErrorResponse | Sandbox | None:
    r"""Patch sandbox metadata

     Update sandbox metadata using JSON Merge Patch semantics (RFC 7396).

    The request body is a partial Sandbox representation. Only `metadata` is
    mutable; other top-level fields are rejected with 400.

    **Merge Patch rules for `metadata`:**
    | Request body key/value | Behavior |
    |---|---|
    | `\"key\": \"value\"` | Add or replace the key |
    | `\"key\": null` | Delete the key (silently ignored if key does not exist) |
    | key absent | Keep current value (no change) |
    | Empty `{}` or `{\"metadata\": {}}` | No-op, returns current metadata |

    Metadata keys and values must comply with Kubernetes label rules:
    - Keys must be valid DNS label names or prefixed DNS subdomains
    - Keys with the `opensandbox.io/` prefix are reserved and rejected
    - Values must be 63 characters or less, matching `[A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?`

    This operation does not restart or recreate the sandbox container/pod.

    Args:
        sandbox_id (str):
        body (PatchSandboxRequest): JSON Merge Patch (RFC 7396) request body for partially
            updating a sandbox.

            Only the `metadata` field is mutable. The top-level object follows merge-patch
            semantics: `metadata` present replaces the metadata sub-object (merge-patched),
            `metadata` absent leaves it unchanged. Other top-level fields are rejected.

            Within `metadata`, the same merge-patch rules apply:
            - Present keys with non-null values add or replace
            - Keys with `null` values are deleted
            - Absent keys are left unchanged

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Sandbox
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchSandboxRequest,
) -> Response[ErrorResponse | Sandbox]:
    r"""Patch sandbox metadata

     Update sandbox metadata using JSON Merge Patch semantics (RFC 7396).

    The request body is a partial Sandbox representation. Only `metadata` is
    mutable; other top-level fields are rejected with 400.

    **Merge Patch rules for `metadata`:**
    | Request body key/value | Behavior |
    |---|---|
    | `\"key\": \"value\"` | Add or replace the key |
    | `\"key\": null` | Delete the key (silently ignored if key does not exist) |
    | key absent | Keep current value (no change) |
    | Empty `{}` or `{\"metadata\": {}}` | No-op, returns current metadata |

    Metadata keys and values must comply with Kubernetes label rules:
    - Keys must be valid DNS label names or prefixed DNS subdomains
    - Keys with the `opensandbox.io/` prefix are reserved and rejected
    - Values must be 63 characters or less, matching `[A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?`

    This operation does not restart or recreate the sandbox container/pod.

    Args:
        sandbox_id (str):
        body (PatchSandboxRequest): JSON Merge Patch (RFC 7396) request body for partially
            updating a sandbox.

            Only the `metadata` field is mutable. The top-level object follows merge-patch
            semantics: `metadata` present replaces the metadata sub-object (merge-patched),
            `metadata` absent leaves it unchanged. Other top-level fields are rejected.

            Within `metadata`, the same merge-patch rules apply:
            - Present keys with non-null values add or replace
            - Keys with `null` values are deleted
            - Absent keys are left unchanged

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Sandbox]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: PatchSandboxRequest,
) -> ErrorResponse | Sandbox | None:
    r"""Patch sandbox metadata

     Update sandbox metadata using JSON Merge Patch semantics (RFC 7396).

    The request body is a partial Sandbox representation. Only `metadata` is
    mutable; other top-level fields are rejected with 400.

    **Merge Patch rules for `metadata`:**
    | Request body key/value | Behavior |
    |---|---|
    | `\"key\": \"value\"` | Add or replace the key |
    | `\"key\": null` | Delete the key (silently ignored if key does not exist) |
    | key absent | Keep current value (no change) |
    | Empty `{}` or `{\"metadata\": {}}` | No-op, returns current metadata |

    Metadata keys and values must comply with Kubernetes label rules:
    - Keys must be valid DNS label names or prefixed DNS subdomains
    - Keys with the `opensandbox.io/` prefix are reserved and rejected
    - Values must be 63 characters or less, matching `[A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?`

    This operation does not restart or recreate the sandbox container/pod.

    Args:
        sandbox_id (str):
        body (PatchSandboxRequest): JSON Merge Patch (RFC 7396) request body for partially
            updating a sandbox.

            Only the `metadata` field is mutable. The top-level object follows merge-patch
            semantics: `metadata` present replaces the metadata sub-object (merge-patched),
            `metadata` absent leaves it unchanged. Other top-level fields are rejected.

            Within `metadata`, the same merge-patch rules apply:
            - Present keys with non-null values add or replace
            - Keys with `null` values are deleted
            - Absent keys are left unchanged

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Sandbox
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            body=body,
        )
    ).parsed
