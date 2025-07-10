# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Test data_structures."""

import pytest
from pydantic import ValidationError

from mfd_model.nvm import NVMParams, NVMUploadParams, FourPartID, Release


class TestDataStructures:
    eetrack = "123ABC00"
    release = "1.0.0"
    replaces = ["123ABC01", "123ABC02", "123ABC03"]
    family = "Columbiaville"
    url = "http://example.com"
    devicename = "some name"
    vendor = "8080"
    subvendor = "8081"
    device = "8082"
    subdevice = "8083"
    milestone = "Alpha"
    drop = "2.0"
    checksum = "1234567890"

    def test_nvm_params_creation(self):
        NVMParams(
            eetrackid=self.eetrack,
            replaces=self.replaces,
            family=self.family,
            url=self.url,
            devicename=self.devicename,
            md5_checksum=self.checksum,
            four_part_id=FourPartID(
                vendor=self.vendor,
                subvendor=self.subvendor,
                device=self.device,
                subdevice=self.subdevice,
            ),
            release=[
                Release(
                    release=self.release,
                    milestone=self.milestone,
                    drop=self.drop,
                )
            ],
        )

    def test_nvm_upload_params_creation(self):
        NVMUploadParams(
            eetrackid=self.eetrack,
            replaces=self.replaces,
            family=self.family,
            devicename=self.devicename,
            four_part_id=FourPartID(
                vendor=self.vendor,
                subvendor=self.subvendor,
                device=self.device,
                subdevice=self.subdevice,
            ),
            release=[
                Release(
                    release=self.release,
                    milestone=self.milestone,
                    drop=self.drop,
                )
            ],
        )

    def test_params_creation_defaults(self):
        params = NVMUploadParams(
            eetrackid=self.eetrack,
            family=self.family,
            devicename=self.devicename,
            four_part_id=FourPartID(
                vendor=self.vendor,
                subvendor=self.subvendor,
                device=self.device,
                subdevice=self.subdevice,
            ),
            release=[
                Release(
                    release=self.release,
                )
            ],
        )
        assert params.release[0].milestone is None
        assert params.release[0].drop is None
        assert len(params.replaces) == 0

        params = NVMParams(
            eetrackid=self.eetrack,
            family=self.family,
            url=self.url,
            devicename=self.devicename,
            md5_checksum=self.checksum,
            four_part_id=FourPartID(
                vendor=self.vendor,
                subvendor=self.subvendor,
                device=self.device,
                subdevice=self.subdevice,
            ),
            release=[
                Release(
                    release=self.release,
                )
            ],
        )
        assert params.release[0].milestone is None
        assert params.release[0].drop is None
        assert len(params.replaces) == 0

    def test_nvm_params_creation_family_unsupported(self):
        with pytest.raises(ValidationError):
            NVMParams(
                eetrackid=self.eetrack,
                replaces=self.replaces,
                family="NotRealFamilyHere",
                url=self.url,
                devicename=self.devicename,
                md5_checksum=self.checksum,
                four_part_id=FourPartID(
                    vendor=self.vendor,
                    subvendor=self.subvendor,
                    device=self.device,
                    subdevice=self.subdevice,
                ),
                release=[
                    Release(
                        release=self.release,
                        milestone=self.milestone,
                        drop=self.drop,
                    )
                ],
            )

    def test_nvm_upload_params_creation_family_unsupported(self):
        with pytest.raises(ValidationError):
            NVMUploadParams(
                eetrackid=self.eetrack,
                replaces=self.replaces,
                family="NotRealFamilyHere",
                devicename=self.devicename,
                four_part_id=FourPartID(
                    vendor=self.vendor,
                    subvendor=self.subvendor,
                    device=self.device,
                    subdevice=self.subdevice,
                ),
                release=[
                    Release(
                        release=self.release,
                        milestone=self.milestone,
                        drop=self.drop,
                    )
                ],
            )

    def test_nvm_upload_params_missing_mandatory_fields(self):
        with pytest.raises(ValueError):
            NVMUploadParams(eetrackid=self.eetrack, replaces=self.replaces)

    def test_params_creation_string(self):
        params = NVMParams.validate_to_json(
            '{"eetrackid":"ABCDEFAA","release":[{"drop":"5.0","milestone":"Beta","release":"Important 1.0"}],'
            '"replaces":["ABCDEFA9"],"family":"Linkville","devicename":"Quad Port",'
            '"url":"https://artifactory-server/file.bin",'
            '"four_part_id":{"device":"AAAA","subdevice":"0003","vendor":"8086","subvendor":"8086"},"pldm_header":true,'
            '"signed":true,"md5_checksum":"aabe476d6b6aaaaa28799f638bdd6f8f","metadata":{}}'
        )
        assert params.release[0].milestone == "Beta"
        assert params.release[0].drop == "5.0"
        assert len(params.replaces) == 1

    def test_uppercase(self):
        params = NVMParams(
            four_part_id=FourPartID(vendor="8086", subvendor="8086", device="57b0", subdevice="0003"),
            eetrackid="AAAABBBC",
            replaces=["AAAABBBA", "AAAABBBB"],
        )
        assert params.eetrackid == "AAAABBBC"
        assert params.replaces == ["AAAABBBA", "AAAABBBB"]
        assert params.four_part_id.vendor == "8086"
        assert params.four_part_id.subvendor == "8086"
        assert params.four_part_id.device == "57B0"
        assert params.four_part_id.subdevice == "0003"
