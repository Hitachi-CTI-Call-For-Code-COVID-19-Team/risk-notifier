
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

import json
from datetime import datetime
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant import cloudant
import sys


def main(dict):

    dbname_NotitificationTemplate = "a_notification_template"
    docId_notificationTemplate = "notification-template-v02"

    dbname_Asset_staff = "assets_staff"

    inputVal = dict["docs"]
    staffdata = inputVal if type(inputVal) == list else [inputVal]
    staffdata0 = staffdata[0]
    staffId = staffdata0["id"]
    severity = staffdata0["severity"]

    relatedDoc = sendQuery(dbname_Asset_staff, staffId)["doc"]
    deviceId = relatedDoc["deviceId"]

    notificaionTemplateDoc = sendQuery(
        dbname_NotitificationTemplate, docId_notificationTemplate)["doc"]

    language = "en"                         # en, jp
    notTempDict = notificaionTemplateDoc["notifications"][language]

    # preparing Text
    note_text = notTempDict[staffdata0["code"]["target"]
                            ][staffdata0["code"]["kind"]][staffdata0["code"]["number"]]
    note_title = makeTitle(staffdata)

    db_riskNotification = "log_risk_notifier"

    apnstype = "SILENT"

    variables = getVariables(staffdata0["variables"])

    # {
    #     "apnsType": "SILENT",
    #     "targetDeviceIds": ["E9B0E15F-19D0-4721-A7E4-DB6C0B220FB4"],
    #     "messageText": "Its been > 20 min please wash/clean your hands",
    #     "apnstitle": "Current Risk: high"
    # }

    pushInput = {
        "messageText": note_text.format(**variables),
        "apnstitle": note_title,
        "targetDeviceIds": deviceId if type(deviceId) is list else [deviceId],
        # imput your device Id for connection format ["<id>"] --> ["D8AA1D5F-A10E-4C09-98BA-BD481709E11D"]
        "apnsType": apnstype
    }

    return pushInput


def getVariables(data):

    var = {"peopleC": "A lot",
           "objectO": "hand wash",
           "timeT": "long time",
           "areaA": "Floor-shop A ",
           "usageS": "multiple times",
           "staffS": "you",
           "riskType": "st"}

    returnVar = {}
    for each in var:
        if each in data:
            returnVar[each] = data[each]
        else:
            returnVar[each] = var[each]

    return returnVar


def makeTitle(dict0):

    print(len(dict0))
    if len(dict0) == 0:
        return None

    if len(dict0) == 1:

        isFirstnotification = True

        title = "Risk changed observed: Level " + dict0[0]["severity"]

    else:

        isFirstnotification = False

        if dict0[0]["severity"] == dict0[1]["severity"]:
            change = False
            title = "Current Risk: " + dict0[1]["severity"]

        else:
            change = True
            title = "Risk changed observed: " + \
                dict0[1]["severity"] + " to " + dict0[0]["severity"]

    return title


def sendQuery(dbname00, docName):

    username_cloudant = ""                    #   "INPUT YOUR CLOUDANT CREDENTIALS"
    apikey_cloudant = ""                      #   "INPUT YOUR CLOUDANT CREDENTIALS"
    client = Cloudant.iam(username_cloudant, apikey_cloudant)
    client.connect()

    my_database = client[dbname00]
    doc = my_database[docName]

    return {"doc": doc}

 # push notification Input
    # {
    #     "text":"" from template
    #     "title":"" short title
    #     "targetDevices": ["D8AA1D5F-A10E-4C09-98BA-BD481709E11D"]
    #     "apnsType":""

    #         }

    # notificationOutput = {
    #     "timestamp": (datetime.now()).strftime('%Y-%m-%dT%H:%M:%SZ'), # current time stamp
    #     "id": _id,
    #     "causes": reason + ", risk is "+ str(_riskLevel),
    #     "severity": _riskLevel,
    #     "variables":dictForm,
    #     "code": {
    #         "target": n_toWhom,     #_toWhom
    #         "kind": n_category,     #_kind
    #         "number": n_number      #_type
    # }
    # }
