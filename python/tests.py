#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import argparse
import sys

from plano import *

def open_test_session(session):
    set_message_threshold("error")

def test_qpid_jms_connect(session):
    with TestServer() as server:
        call("qpid-jms/scripts/connect {}", server.connection_url)

def test_qpid_proton_cpp_connect(session):
    with TestServer() as server:
        call("qpid-proton-cpp/build/connect {}", server.connection_url)

def test_qpid_proton_python_connect(session):
    with TestServer() as server:
        call("qpid-proton-python/connect.py {}", server.connection_url)

def test_rhea_connect(session):
    with TestServer() as server:
        call("rhea/connect.js {}", server.connection_url)

class TestServer(object):
    def __init__(self):
        port = random_port()

        self.proc = start_process("qbroker --verbose --port {}", port)
        self.proc.connection_url = "amqp://127.0.0.1:{}".format(port) # XXX C++ fails with amqp: prefix here

    def __enter__(self):
        return self.proc

    def __exit__(self, exc_type, exc_value, traceback):
        stop_process(self.proc)
