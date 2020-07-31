
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


def main(params):

    if params["variables"]["riskType"] == "st":

        selector = {"id": {"$eq": params["id"]}}
        fields = []
        sort = [{"timestamp": "desc"}]

        query = {"selector": selector,
                 "fields": fields, "sort": sort, "limit": 2}

        return {"dbname": "log_risk_notifier", "query": query}

    else:
        return {"error": "Forced Stop: notification is not invidual type"}
