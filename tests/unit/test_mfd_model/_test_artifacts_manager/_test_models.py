# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Test models."""

import pytest

from mfd_const import Artifacts

from mfd_model.artifacts_manager import ArtifactRequest


class TestArtifactRequest:
    """Test ArtifactRequest model."""

    def test_artifact_cast(self):
        artifact_request = ArtifactRequest(artifact=Artifacts.eeupdate)
        assert artifact_request.artifact == "Tools-Eeupdate_Intel"

        artifact_request = ArtifactRequest(artifact="Tools-Eeupdate_Intel")
        assert artifact_request.artifact == "Tools-Eeupdate_Intel"

        with pytest.raises(ValueError):
            ArtifactRequest(artifact="InvalidArtifact")

    def test_os_cast(self):
        artifact_request = ArtifactRequest(artifact=Artifacts.eeupdate, os=Artifacts.COMMON_SUPPORTED_OS.win64e)
        assert artifact_request.os == "win64e"

        artifact_request = ArtifactRequest(artifact=Artifacts.eeupdate, os=Artifacts.eeupdate.os.win64e)
        assert artifact_request.os == "win64e"

        artifact_request = ArtifactRequest(artifact=Artifacts.eeupdate, os="win64e")
        assert artifact_request.os == "win64e"

        with pytest.raises(ValueError):
            ArtifactRequest(artifact=Artifacts.eeupdate, os="someWindows")
