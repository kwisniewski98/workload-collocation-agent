# Copyright (c) 2020 Intel Corporation
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
import pytest
from tests.scheduler.data_providers.test_cluster_score_data_provider import APPS_PROFILE

from wca.scheduler.algorithms.score import _get_app_node_type
from wca.scheduler.data_providers.score import NodeType

SCORE_TARGET = -2.0


@pytest.mark.parametrize('apps_profile, app_name, score_target, result', [
    (APPS_PROFILE, 'memcached-mutilate-big', None, NodeType.PMEM),
    (APPS_PROFILE, 'sysbench-memory-small', None, NodeType.DRAM),
    (APPS_PROFILE, 'sysbench-memory-big', SCORE_TARGET, NodeType.DRAM),
    (APPS_PROFILE, 'sysbench-memory-small', SCORE_TARGET, NodeType.DRAM),
    (APPS_PROFILE, 'sysbench-memory-medium', SCORE_TARGET, NodeType.DRAM),
    (APPS_PROFILE, 'stress-stream-big', SCORE_TARGET, NodeType.DRAM),
    (APPS_PROFILE, 'stress-stream-medium', SCORE_TARGET, NodeType.DRAM),
    (APPS_PROFILE, 'stress-stream-small', SCORE_TARGET, NodeType.DRAM),
    (APPS_PROFILE, 'memcached-mutilate-big', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'mysql-hammerdb-small', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'memcached-mutilate-small', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'redis-memtier-medium', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'redis-memtier-small', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'redis-memtier-big', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'memcached-mutilate-medium', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'specjbb-preset-big-120', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'memcached-mutilate-big-wss', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'specjbb-preset-small', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'redis-memtier-big-wss', SCORE_TARGET, NodeType.PMEM),
    (APPS_PROFILE, 'specjbb-preset-medium', SCORE_TARGET, NodeType.PMEM),
    ([], '', None, NodeType.DRAM),
    ])
def test_get_app_node_type(apps_profile, app_name, score_target, result):
    assert _get_app_node_type(apps_profile, app_name, score_target) == result


@pytest.mark.parametrize('', [
    (),
    ])
def test_reschedule():
    pass
