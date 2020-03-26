"""
qpdriver entrypoint module
"""
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
from ricxappframe.xapp_frame import RMRXapp


"""
This is only a stencil for now, will be filled in!
What is currently here was only for initial skeleton and test creation.
"""

"""
RMR Messages
 #define TS_UE_LIST 30000
 #define TS_QOE_PRED_REQ 30001
30000 is the message QPD receives, sends out 30001 to QP
"""


def post_init(self):
    self.def_hand_called = 0
    self.traffic_steering_requests = 0


def default_handler(self, summary, sbuf):
    self.def_hand_called += 1
    print(summary)
    self.rmr_free(sbuf)


def steering_req_handler(self, summary, sbuf):
    """
    This is the main handler for this xapp, which handles the traffic steering requests.
    Traffic steering requests predictions on a set of UEs.
    QP Driver (this) fetches a set of data, merges it together in a deterministic way, then sends a new message out to the QP predictor Xapp.

    The incoming message that this function handles looks like:
        {“UEPredictionSet” : [“UEId1”,”UEId2”,”UEId3”]}
    """
    self.traffic_steering_requests += 1
    print(summary)
    self.rmr_free(sbuf)


# obv some of these flags have to change
rmr_xapp = RMRXapp(default_handler, post_init=post_init, rmr_port=4562, use_fake_sdl=True)
rmr_xapp.register_callback(steering_req_handler, 30000)


def start(thread=False):
    rmr_xapp.run(thread)


def stop():
    """can only be called if thread=True when started"""
    rmr_xapp.stop()


def get_stats():
    # hacky for now, will evolve
    return {"DefCalled": rmr_xapp.def_hand_called, "SteeringRequests": rmr_xapp.traffic_steering_requests}
