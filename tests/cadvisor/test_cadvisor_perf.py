# Copyright (C) 2020 Intel Corporation
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
from datetime import datetime, timedelta
import csv
from io import StringIO

CADVISOR_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
EXPECTED_PERF_METRICS = ["cycles"]

#
# def test_perf_api():
#     cadvisor_port = os.environ.get("CADVISOR_PORT")
#     resp = requests.get(f"http://127.0.0.1:{cadvisor_port}/api/v1.3/containers")
#     perf_stats = resp.json()["stats"][0]["perf_stats"]
#     assert perf_stats
#     perf_metrics = []
#     for perf_stat in perf_stats:
#         perf_metrics.append(perf_stat["name"]) if perf_stat[
#             "name"
#         ] not in perf_metrics else None
#     perf_metrics.sort()
#     assert EXPECTED_PERF_METRICS == perf_metrics
#


def test_perf_run():
    cadvisor_port = os.environ.get("CADVISOR_PORT")
    with open("pmbench_container_id.txt") as f:
        cgroup = f.read().strip("\n")
    with open("perf_result.txt") as f:
        perf_results = f.read().strip("\n")
    with open("perf_ending_timestamp.txt") as f:
        end_timestamp = f.read().strip("\n")
    end_date = datetime.fromtimestamp(int(end_timestamp))
    resp = requests.get(f"http://127.0.0.1:{cadvisor_port}/api/v1.3/docker").json()
    container_stats = resp[f"/docker/{cgroup}"]["stats"]
    container_stats.reverse()
    assert container_stats
    for i, stats in enumerate(container_stats):
        cadvisor_date = datetime.strptime(
            stats["timestamp"][:-4], CADVISOR_TIMESTAMP_FORMAT
        )
        # we look for the closest timestamp after timestamp gotten from env
        if cadvisor_date - end_date < timedelta(0):
            selected_stats_index = i
            break
    if (
        abs(
            datetime.strptime(
                container_stats[selected_stats_index]["timestamp"][:-4],
                CADVISOR_TIMESTAMP_FORMAT,
            )
            - end_date
        ).total_seconds()
    ) < (
        abs(
            datetime.strptime(
                container_stats[selected_stats_index - 1]["timestamp"][:-4],
                CADVISOR_TIMESTAMP_FORMAT,
            )
            - end_date
        ).total_seconds()
    ):
        stats = container_stats[selected_stats_index]
    else:
        stats = container_stats[selected_stats_index-1]
    assert stats
    perf_output = parse_perf_output(perf_results)
    for metric in EXPECTED_PERF_METRICS:
        cadvisor_perf_value = sum([float(stat["value"]) for stat in stats["perf_stats"] if stat["name"] == metric])
        assert cadvisor_perf_value * 0.95 < float(perf_output[metric]) < cadvisor_perf_value * 1.05


def parse_perf_output(output: str) -> map:
    reader = csv.reader(StringIO(output))
    stats = {}
    for row in reader:
        stats[row[2]] = float(row[0])
    return stats
