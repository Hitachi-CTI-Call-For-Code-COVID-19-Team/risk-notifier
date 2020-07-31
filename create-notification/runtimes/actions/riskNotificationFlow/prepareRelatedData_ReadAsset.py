
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

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant import cloudant
import pandas as pd
import json


def main(dict):

    idValue = dict["id"]

    if dict["id"] == "TOTAL":
        idValue = "imaginary-shopping-mall"

    relatedAsset = sendQuery(idValue)
    # print(relatedAsset)
    relevantData = {

        "rc_id": idValue,
        "rc_riskValue": dict["risk"]["value"],
        "rc_riskCumValue": dict["risk"]["cumValue"],
        "rc_riskLevel": dict["risk"]["level"],
        "rc_riskType": dict["risk"]["type"],

        "a_isType": relatedAsset.get("type", ""),
        "a_isSubType": relatedAsset.get("subType", ""),
        "a_isBelongs": relatedAsset.get("belongs", ""),
        "a_belongings": relatedAsset.get("belongings", ""),
        "a_isCoordinate": relatedAsset.get("mapCoordinate", {})

    }

    # {'data' : relatedAssetData,"riskCalculatorData": riskData}
    return relevantData


def sendQuery(id0):

    username_cloudant = "3c30e71f-1f5a-4498-af74-06860a23e042-bluemix"
    apikey_cloudant = "t7Lf7KxBAiqFOq6T_EW1dCQC1l1bZCP98q1YnBHxJUn4"
    client = Cloudant.iam(username_cloudant, apikey_cloudant)
    client.connect()

    if "st00" in id0:
        database_name1 = "assets_staff"
        my_database = client[database_name1]
        doc = my_database[id0]

    else:
        database_name1 = "assets"
        my_database = client[database_name1]
        relatedAsset = my_database.get_query_result(
            selector={"id": {"$eq": id0}})
        print(type(relatedAsset), relatedAsset)
        doc = relatedAsset.all()[0]  # my_database[id0]

    client.disconnect()

    return doc
