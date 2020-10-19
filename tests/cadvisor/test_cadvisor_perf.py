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
import json

EXPECTED_PERF_METRICS = ["cycles", "instructions",
                         "instructions_retired"]
EXPECTED_PERF_METRICS.sort()


def test_perf():
    cadvisor_port = os.environ.get("CADVISOR_PORT")
    resp = requests.get(f"http://127.0.0.1:{cadvisor_port}/api/v1.3/containers")
    stats = json.loads(resp.content)
    perf_stats = stats["stats"][0]["perf_stats"]
    assert perf_stats
    perf_metrics = []
    for perf_stat in perf_stats:
        perf_metrics.append(perf_stat["name"]) if perf_stat["name"] not in perf_metrics else None
    perf_metrics.sort()
    assert EXPECTED_PERF_METRICS == perf_metrics

