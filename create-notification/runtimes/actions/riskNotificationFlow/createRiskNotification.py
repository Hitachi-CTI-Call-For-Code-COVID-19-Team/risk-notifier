
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


# createRiskNotification
# all logic assumed


from datetime import datetime
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant import cloudant
import pandas as pd
import json


def main(dict):

    returnVal = None

    # if dict.get("rc_riskLevel","") == "high":               #dict.get("rc_riskLevel","") == "acceptable" or
    returnVal = createSuggestions(dict)["out"]

    return {"write_value": returnVal}


def createSuggestions(data0):

    # {
    #   "a_belongings": [],
    #   "a_isBelongs": "imaginary-shopping-mall-1st-floor",
    #   "a_isSubType": "shop",
    #   "a_isType": "area",
    #   "rc_id": "congestion-270-1860",
    #   "rc_riskCumValue": 0.8,
    #   "rc_riskLevel": "high",
    #   "rc_riskType": "c",
    #   "rc_riskValue": 0.8
    # }

    _id = data0["rc_id"]
    _riskValue = data0["rc_riskValue"]
    _riskCumValue = data0["rc_riskCumValue"]
    _riskLevel = data0["rc_riskLevel"]
    riskType = data0["rc_riskType"]

    isType = data0["a_isType"]
    isBelongs = data0["a_isBelongs"]
    issubType = data0["a_isSubType"]
    isMapLoc = data0.get("a_isCoordinate", {})

    suggestionList = {}

    # VARIABLES for notifications
    sg = ""
    peopleC = 0
    objectO = ""
    timeT = ""
    areaA = ""
    usageS = 0
    riskR = 0
    staffS = ""
    frequencyF = 0

    n_toWhom = ""
    n_category = ""
    n_number = ""

    # gathering Suggestion lists based on risk values

    reason = ""

    df_All = pd.DataFrame(getMappings()).T

    for index, df in df_All.iterrows():

        tempRisk = 0

        match_riskType = riskType in df["riskType"]
        match_riskValue = _riskValue <= df["riskScore"] if _riskValue < 0 else _riskValue >= df["riskScore"]
        match_riskLevel = _riskLevel in df["riskLevel"]

        match_isType = isType in df["isType"] or df["isType"] in isType

        if df["isSubtype"] == "":
            match_isSubType = True
        else:
            match_isSubType = issubType in df["isSubtype"] or df["isSubtype"] in issubType
        #     match_isBelongs = isBelongs in df["isBelongs"] or  df["isBelongs"] in isBelongs

        # print(match_riskType, match_riskValue,
            #   match_riskLevel, match_isType, match_isSubType)

        if match_riskType and match_riskValue and match_riskLevel and match_isType and match_isSubType:

            if tempRisk < _riskValue:
                tempRisk = _riskValue

                n_toWhom = df["toWhom"]
                n_category = df["kind"]
                n_number = "0" + \
                    str(df["number"]) if df["number"] < 10 else str(
                        df["number"])

    dictForm = {}

    if objectO != "":
        dictForm["objectO"] = objectO
    if areaA != "":
        dictForm["areaA"] = areaA
    if peopleC != "":
        dictForm["peopleC"] = peopleC
    if riskType != "":
        dictForm["riskType"] = riskType

    notificationOutput = {
        # current time stamp
        "timestamp": (datetime.now()).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "id": _id,
        "causes": reason + ", risk is " + str(_riskLevel),
        "severity": _riskLevel,
        "variables": dictForm,
        "code": {
            "target": n_toWhom,  # _toWhom
            "kind": n_category,  # _kind
            "number": n_number  # _type
        }
    }

    return {"out": notificationOutput}


def getMappings():

    # Folloeing dict is created based on notification template ( check cloudant DB)

    relationMap_json = {
        "1": {
            "riskType": "c",
            "riskScore": 0.5,
            "riskLevel": "low",
            "isType": "area",
            "isSubtype": "any",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "general",
            "number": 0
        },
        "2": {
            "riskType": "c",
            "riskScore": 0.5,
            "riskLevel": "acceptable",
            "isType": "line",
            "isSubtype": "counter",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "general",
            "number": 1
        },
        "3": {
            "riskType": "t",
            "riskScore": 0.5,
            "riskLevel": "any",
            "isType": "handwash",
            "isSubtype": "outside",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "general",
            "number": 2
        },
        "4": {
            "riskType": "c",
            "riskScore": 0.5,
            "riskLevel": "acceptable",
            "isType": "area",
            "isSubtype": "any",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "congestion",
            "number": 0
        },
        "5": {
            "riskType": "cdsst",
            "riskScore": 0.0,
            "riskLevel": "acceptable",
            "isType": "area",
            "isSubtype": "periodic",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "congestion",
            "number": 1
        },
        "6": {
            "riskType": "cdsst",
            "riskScore": 0.5,
            "riskLevel": "acceptable",
            "isType": "area, thing",
            "isSubtype": "handwash_stand",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "sanitisation",
            "number": 0
        },
        "7": {
            "riskType": "cdsst",
            "riskScore": 0.5,
            "riskLevel": "acceptable",
            "isType": "thing",
            "isSubtype": "handwash_stand",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "sanitisation",
            "number": 1
        },
        "8": {
            "riskType": "s",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "handwash_stand",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "sanitisation",
            "number": 2
        },
        "9": {
            "riskType": "c",
            "riskScore": 0.7,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "toilet",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "toilet",
            "number": 0
        },
        "10": {
            "riskType": "c",
            "riskScore": 0.5,
            "riskLevel": "high",
            "isType": "line",
            "isSubtype": "toilet",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "toilet",
            "number": 1
        },
        "11": {
            "riskType": "c",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "roadway",
            "other": "count",
            "toWhom": "forCustomers",
            "kind": "general",
            "number": 3
        },
        "12": {
            "riskType": "c",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "aisle",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "congestion",
            "number": 0
        },
        "13": {
            "riskType": "c",
            "riskScore": 0.7,
            "riskLevel": "high",
            "isType": "line",
            "isSubtype": "shop",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "congestion",
            "number": 1
        },
        "14": {
            "riskType": "c",
            "riskScore": 0.9,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "shop",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "congestion",
            "number": 2
        },
        "15": {
            "riskType": "d",
            "riskScore": 0.5,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "tables, eat ",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "disinfection",
            "number": 0
        },
        "16": {
            "riskType": "d",
            "riskScore": 0.6,
            "riskLevel": "acceptable",
            "isType": "area",
            "isSubtype": "aisles",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "disinfection",
            "number": 1
        },
        "17": {
            "riskType": "d",
            "riskScore": 0.4,
            "riskLevel": "low",
            "isType": "area",
            "isSubtype": "door",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "disinfection",
            "number": 2
        },
        "18": {
            "riskType": "d",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "shop",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "disinfection",
            "number": 3
        },
        "19": {
            "riskType": "d",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "parking",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "disinfection",
            "number": 4
        },
        "20": {
            "riskType": "d",
            "riskScore": 0.75,
            "riskLevel": "high",
            "isType": "area, thing",
            "isSubtype": "toilet., wash",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "sanitisation",
            "number": 0
        },
        "21": {
            "riskType": "d",
            "riskScore": 0.75,
            "riskLevel": "high",
            "isType": "thing",
            "isSubtype": "handwash_stand",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "sanitisation",
            "number": 1
        },
        "22": {
            "riskType": "d",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "toilet",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "toilet",
            "number": 0
        },
        "23": {
            "riskType": "s",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "thing",
            "isSubtype": "soap, handwash",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "toilet",
            "number": 1
        },
        "24": {
            "riskType": "c",
            "riskScore": 0.85,
            "riskLevel": "high",
            "isType": "area, line",
            "isSubtype": "toilet",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "toilet",
            "number": 2
        },
        "25": {
            "riskType": "s",
            "riskScore": 0.95,
            "riskLevel": "high",
            "isType": "thing",
            "isSubtype": "garbage_bin",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "garbage",
            "number": 0
        },
        "26": {
            "riskType": "s",
            "riskScore": 0.7,
            "riskLevel": "high",
            "isType": "thing",
            "isSubtype": "garbage_bin",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "garbage",
            "number": 1
        },
        "27": {
            "riskType": "d",
            "riskScore": 0.7,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "garbage",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "garbage",
            "number": 2
        },
        "28": {
            "riskType": "st",
            "riskScore": 0.9,
            "riskLevel": "high",
            "isType": "staff",
            "isSubtype": "area, location, shop",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "individual",
            "number": 0
        },
        "29": {
            "riskType": "st",
            "riskScore": 1.0,
            "riskLevel": "high",
            "isType": "staff",
            "isSubtype": "area, time",
            "other": "count",
            "toWhom": "toStaff",
            "kind": "individual",
            "number": 1
        },
        "30": {
            "riskType": "t",
            "riskScore": 0.9,
            "riskLevel": "high",
            "isType": "site",
            "isSubtype": "time, max, period",
            "other": "count",
            "toWhom": "toManager",
            "kind": "general",
            "number": 0
        },
        "31": {
            "riskType": "st",
            "riskScore": 0.9,
            "riskLevel": "high",
            "isType": "staff",
            "isSubtype": "staff, individual",
            "other": "count",
            "toWhom": "toManager",
            "kind": "general",
            "number": 1
        },
        "32": {
            "riskType": "t",
            "riskScore": 0.9,
            "riskLevel": "high",
            "isType": "site, total",
            "isSubtype": "total",
            "other": "today",
            "toWhom": "toManager",
            "kind": "general",
            "number": 2
        },
        "33": {
            "riskType": "t",
            "riskScore": -0.3,
            "riskLevel": "low",
            "isType": "site, total",
            "isSubtype": "total",
            "other": "mode, mean",
            "toWhom": "toManager",
            "kind": "general",
            "number": 3
        },
        "34": {
            "riskType": "ct",
            "riskScore": 0.9,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "shop, parking",
            "other": "max, area",
            "toWhom": "toManager",
            "kind": "congestion",
            "number": 0
        },
        "35": {
            "riskType": "ct",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "any",
            "other": "current",
            "toWhom": "toManager",
            "kind": "congestion",
            "number": 1
        },
        "36": {
            "riskType": "ct",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "any",
            "other": "median",
            "toWhom": "toManager",
            "kind": "congestion",
            "number": 2
        },
        "37": {
            "riskType": "ct",
            "riskScore": 2.0,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "location",
            "other": "peak, cummulative",
            "toWhom": "toManager",
            "kind": "congestion",
            "number": 3
        },
        "38": {
            "riskType": "dt",
            "riskScore": 2.0,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "time ",
            "other": "peak, cummulative",
            "toWhom": "toManager",
            "kind": "disinfection",
            "number": 0
        },
        "39": {
            "riskType": "dt",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "area",
            "isSubtype": "shop",
            "other": "pattern",
            "toWhom": "toManager",
            "kind": "disinfection",
            "number": 1
        },
        "40": {
            "riskType": "dt",
            "riskScore": 1.0,
            "riskLevel": "positive",
            "isType": "area",
            "isSubtype": "any",
            "other": "compare",
            "toWhom": "toManager",
            "kind": "disinfection",
            "number": 2
        },
        "41": {
            "riskType": "st",
            "riskScore": 0.8,
            "riskLevel": "high",
            "isType": "staff",
            "isSubtype": "individual",
            "other": "median",
            "toWhom": "toManager",
            "kind": "sanitisation",
            "number": 0
        },
        "42": {
            "riskType": "st",
            "riskScore": -0.4,
            "riskLevel": "high",
            "isType": "thing",
            "isSubtype": "handwash_stand",
            "other": "count",
            "toWhom": "toManager",
            "kind": "sanitisation",
            "number": 1
        }
    }

    return relationMap_json

    # #####
    # push notification Input
    # {
    #     "text":"" from template
    #     "title":"" short title
    #     "targetDevices": ["D8AA1D5F-A10E-4C09-98BA-BD481709E11D"]
    #     "apnsType":""

    #         }
    # level = "high"#, "acceptable, low"

    ###
    # Basic logic to create above json template
    # 1 - create dict and enter one by one
    # 2 - excel -> dataframe -> json

    # In principle,
    # - it checks many condtion - riskType, riskScore, riskLevel,isType, isSubtype, other
    # - gives output toWhom, kind, number
