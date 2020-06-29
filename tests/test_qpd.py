# ==================================================================================
#       Copyright (c) 2020 AT&T Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================
import json
import time
from contextlib import suppress
from qpdriver import main, data
from ricxappframe.xapp_frame import Xapp, RMRXapp

mock_ts_xapp = None
mock_qp_xapp = None
# tox.ini sets env var to this value
config_file_path = "/tmp/config.json"

"""
 these tests are not currently parallelizable (do not use this tox flag)
 I would use setup_module, however that can't take monkeypatch fixtures
 Currently looking for the best way to make this better:
 https://stackoverflow.com/questions/60886013/python-monkeypatch-in-pytest-setup-module
"""


def init_config_file():
    with open(config_file_path, "w") as file:
        file.write('{ "example_int" : 0 }')


def write_config_file():
    # generate an inotify/config event
    with open(config_file_path, "w") as file:
        file.write('{ "example_int" : 1 }')


def test_init_xapp(monkeypatch, ue_metrics, cell_metrics_1, cell_metrics_2, cell_metrics_3, ue_metrics_with_bad_cell):
    # monkeypatch post_init to set the data we want in SDL
    # the metrics arguments are JSON (dict) objects

    _original_post_init = main.post_init

    def fake_post_init(self):
        _original_post_init(self)
        self.sdl_set(data.UE_NS, "12345", json.dumps(ue_metrics).encode(), usemsgpack=False)
        self.sdl_set(data.UE_NS, "8675309", json.dumps(ue_metrics_with_bad_cell).encode(), usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555001", json.dumps(cell_metrics_1).encode(), usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555002", json.dumps(cell_metrics_2).encode(), usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555003", json.dumps(cell_metrics_3).encode(), usemsgpack=False)

    # patch
    monkeypatch.setattr("qpdriver.main.post_init", fake_post_init)

    # establish config
    init_config_file()

    # start qpd
    main.start(thread=True)

    # wait a bit then update config
    time.sleep(3)
    write_config_file()


def test_rmr_flow(monkeypatch, qpd_to_qp, qpd_to_qp_bad_cell):
    """
    this flow mocks out the xapps on both sides of QP driver.
    It first stands up a mock qp, then it starts up a mock ts
    which will immediately send requests to the running qp driver.
    """

    expected_result = {}

    # define a mock qp predictor
    def mock_qp_default_handler(self, summary, sbuf):
        pass

    def mock_qp_predict_handler(self, summary, sbuf):
        nonlocal expected_result  # closures ftw
        pay = json.loads(summary["payload"])
        expected_result[pay["PredictionUE"]] = pay

    global mock_qp_xapp
    mock_qp_xapp = RMRXapp(mock_qp_default_handler, rmr_port=4666, use_fake_sdl=True)
    mock_qp_xapp.register_callback(mock_qp_predict_handler, 30001)
    mock_qp_xapp.run(thread=True)

    time.sleep(1)

    # define a mock traffic steering xapp
    def mock_ts_entry(self):

        # make sure a bad steering request doesn't blow up in qpd
        val = "notevenjson".encode()
        self.rmr_send(val, 30000)
        val = json.dumps({"bad": "tothebone"}).encode()  # json but missing UEPredictionSet
        self.rmr_send(val, 30000)

        # valid request body but missing cell id
        val = json.dumps({"UEPredictionSet": ["VOIDOFLIGHT"]}).encode()
        self.rmr_send(val, 30000)

        # good traffic steering request
        val = json.dumps({"UEPredictionSet": ["12345", "8675309"]}).encode()
        self.rmr_send(val, 30000)

        # should trigger the default handler and do nothing
        val = json.dumps({"test send 60001": 2}).encode()
        self.rmr_send(val, 60001)

    global mock_ts_xapp
    mock_ts_xapp = Xapp(entrypoint=mock_ts_entry, rmr_port=4564, use_fake_sdl=True)
    mock_ts_xapp.run()  # this will return since entry isn't a loop

    time.sleep(1)

    assert expected_result == {"12345": qpd_to_qp, "8675309": qpd_to_qp_bad_cell}
    assert main.get_stats() == {"DefCalled": 1, "SteeringRequests": 4}

    # break SDL and send traffic again
    def sdl_healthcheck_fails(self):
        return False
    monkeypatch.setattr("ricxappframe.xapp_sdl.SDLWrapper.healthcheck", sdl_healthcheck_fails)
    mock_ts_xapp.run()

    # restore SDL and send traffic once more
    def sdl_healthcheck_passes(self):
        return True
    monkeypatch.setattr("ricxappframe.xapp_sdl.SDLWrapper.healthcheck", sdl_healthcheck_passes)
    mock_ts_xapp.run()


def teardown_module():
    """
    this is like a "finally"; the name of this function is pytest magic
    safer to put down here since certain failures above can lead to pytest never returning
    for example if an exception gets raised before stop is called in any test function above,
    pytest will hang forever
    """
    with suppress(Exception):
        mock_ts_xapp.stop()
    with suppress(Exception):
        mock_qp_xapp.stop()
    with suppress(Exception):
        main.stop()
