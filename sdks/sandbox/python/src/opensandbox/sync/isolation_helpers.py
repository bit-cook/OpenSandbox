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
Standalone sync convenience functions for isolated session lifecycle.
"""

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from opensandbox.models.execd import Execution
from opensandbox.models.execd_sync import ExecutionHandlersSync
from opensandbox.models.isolated import (
    CreateIsolatedSessionRequest,
    IsolatedRunOpts,
    IsolatedWorkspaceSpec,
)
from opensandbox.sync.services.isolated import (
    IsolationServiceSync,
    IsolationSessionSync,
)

logger = logging.getLogger(__name__)


def run_once_sync(
    service: IsolationServiceSync,
    code: str,
    *,
    workspace: str,
    workspace_mode: str | None = None,
    opts: IsolatedRunOpts | None = None,
    handlers: ExecutionHandlersSync | None = None,
    profile: str | None = None,
    share_net: bool | None = None,
) -> Execution:
    """Create an isolated session, run *code*, and delete the session."""
    request = CreateIsolatedSessionRequest(
        workspace=IsolatedWorkspaceSpec(path=workspace, mode=workspace_mode),
        profile=profile,
        share_net=share_net,
    )
    session = service.create(request)
    try:
        return session.run(code, opts=opts, handlers=handlers)
    finally:
        try:
            session.delete()
        except Exception:
            logger.warning("failed to delete isolated session %s", session.session_id)


@contextmanager
def isolation_session_sync(
    service: IsolationServiceSync,
    request: CreateIsolatedSessionRequest,
) -> Iterator[IsolationSessionSync]:
    """Context manager that creates an isolated session and deletes it on exit."""
    session = service.create(request)
    try:
        yield session
    finally:
        try:
            session.delete()
        except Exception:
            logger.warning("failed to delete isolated session %s", session.session_id)
