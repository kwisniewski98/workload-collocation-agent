# Copyright (C) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
#
#
# SPDX-License-Identifier: Apache-2.0

import os
import requests
from glob import glob
from pytest import mark

CADVISOR_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
ERROR_TOLERATION = 0.3
EXPECTED_RESCTRL_METRICS = ["mbm_total_bytes", "mbm_local_bytes"]


@mark.parametrize("metric", EXPECTED_RESCTRL_METRICS)
def test_rdt_mb(metric):
    use_control_group = os.getenv("USE_CONTROL_GROUP")
    cadvisor_port = os.environ.get("CADVISOR_PORT")
    with open("pmbench_container_id_rdt.txt") as f:
        control_group = f.read().strip("\n").replace("/", "-")
    resp = requests.get(
        f"http://127.0.0.1:{cadvisor_port}/api/v1.3/subcontainers"
    ).json()
    for container in resp:
        if container["name"] == f"/docker/{control_group}":
            container_stats = container["stats"]
            break
    stats = container_stats[-1]
    assert stats
    cadvisor_resctrl_mb_values = stats["resctrl"]["memory_bandwidth"]
    if use_control_group == "True":
        group = control_group
    else:
        group = os.getenv("GROUP_NAME")
    resctrl_mb_values = read_rdt_value(metric, group, use_control_group)

    assert resctrl_mb_values and cadvisor_resctrl_mb_values

    print(f"resctl: {resctrl_mb_values}")
    print(f"cadvisor: {cadvisor_resctrl_mb_values}")
    for stat in zip(resctrl_mb_values, cadvisor_resctrl_mb_values):
        if metric not in stat[1].keys():
            assert stat[0] == 0
            continue
        assert (
            stat[0] * (1 - ERROR_TOLERATION)
            < stat[1][metric]
            < stat[0] * (1 + ERROR_TOLERATION)
        )


def read_rdt_value( metric, group, use_cgroup):
    if use_cgroup == "True":
        mon_dirs = glob(f"/sys/fs/resctrl/mon_groups/docker-{group}/mon_data/*/")
    else:
        mon_dirs = glob(f"/sys/fs/resctrl/{group}/mon_data/*/")
    values = []
    for mon_dir in mon_dirs:
        with open(os.path.join(mon_dir, metric)) as f:
            values.append(int(f.read()))
    return values
