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

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_sandbox_request_metadata import PatchSandboxRequestMetadata


T = TypeVar("T", bound="PatchSandboxRequest")


@_attrs_define
class PatchSandboxRequest:
    """JSON Merge Patch (RFC 7396) request body for partially updating a sandbox.

    Only the `metadata` field is mutable. The top-level object follows merge-patch
    semantics: `metadata` present replaces the metadata sub-object (merge-patched),
    `metadata` absent leaves it unchanged. Other top-level fields are rejected.

    Within `metadata`, the same merge-patch rules apply:
    - Present keys with non-null values add or replace
    - Keys with `null` values are deleted
    - Absent keys are left unchanged

        Attributes:
            metadata (PatchSandboxRequestMetadata | Unset): Metadata key-value pairs to merge into the sandbox's current
                metadata.
                Set a key's value to `null` to delete it.
                Keys with the `opensandbox.io/` prefix are reserved and rejected.
                 Example: {'project': 'new-project', 'team': None, 'environment': 'production'}.
    """

    metadata: PatchSandboxRequestMetadata | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patch_sandbox_request_metadata import PatchSandboxRequestMetadata

        d = dict(src_dict)
        _metadata = d.pop("metadata", UNSET)
        metadata: PatchSandboxRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = PatchSandboxRequestMetadata.from_dict(_metadata)

        patch_sandbox_request = cls(
            metadata=metadata,
        )

        return patch_sandbox_request
