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
"""
Standalone convenience functions for isolated session lifecycle.

These accept any ``IsolationService`` and handle create → run → delete
without modifying the service protocol.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from opensandbox.models.execd import Execution, ExecutionHandlers
from opensandbox.models.isolated import (
    CreateIsolatedSessionRequest,
    IsolatedRunOpts,
    IsolatedWorkspaceSpec,
)
from opensandbox.services.isolated import IsolationService, IsolationSession

logger = logging.getLogger(__name__)


async def run_once(
    service: IsolationService,
    code: str,
    *,
    workspace: str,
    workspace_mode: str | None = None,
    opts: IsolatedRunOpts | None = None,
    handlers: ExecutionHandlers | None = None,
    profile: str | None = None,
    share_net: bool | None = None,
) -> Execution:
    """Create an isolated session, run *code*, and delete the session."""
    request = CreateIsolatedSessionRequest(
        workspace=IsolatedWorkspaceSpec(path=workspace, mode=workspace_mode),
        profile=profile,
        share_net=share_net,
    )
    session = await service.create(request)
    try:
        return await session.run(code, opts=opts, handlers=handlers)
    finally:
        try:
            await session.delete()
        except Exception:
            logger.warning("failed to delete isolated session %s", session.session_id)


@asynccontextmanager
async def isolation_session(
    service: IsolationService,
    request: CreateIsolatedSessionRequest,
) -> AsyncIterator[IsolationSession]:
    """Context manager that creates an isolated session and deletes it on exit."""
    session = await service.create(request)
    try:
        yield session
    finally:
        try:
            await session.delete()
        except Exception:
            logger.warning("failed to delete isolated session %s", session.session_id)
