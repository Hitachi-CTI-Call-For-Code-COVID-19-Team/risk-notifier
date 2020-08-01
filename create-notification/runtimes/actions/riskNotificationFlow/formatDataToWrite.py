
# Copyright 2020 Hitachi Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

import sys


def main(dict):

    inputSample = dict["write_value"]

    if inputSample == None:
        return {"error": "Forced Stopped, is empty"}

    # checking for data valdity
    checkObject = inputSample["code"]
    isEmpty = checkObject["kind"] == "" or checkObject["number"] == "" or checkObject["target"] == ""
    if isEmpty:
        return {"error": "Forced Stop, missing values in notification output"}

    return {'doc': dict["write_value"],
            "dbname": "log_risk_notifier"}
