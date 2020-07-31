#!/bin/bash -eu

## Variables
API_KEY="<PLEASE_MODIFY_HERE>"
APP_GUID="<PLEASE_MODIFY_HERE>"
CLIENT_SECRET="<PLEASE_MODIFY_HERE>"

## Reference
# Swagger
# https://jp-tok.imfpush.cloud.ibm.com/imfpush/
#
# API manual
# https://cloud.ibm.com/apidocs/push-notifications

## IAM Access Token
#echo <<END
curl -sk -X POST --header "Content-Type: application/x-www-form-urlencoded" \
     --header "Accept: application/json" --data-urlencode "grant_type=urn:ibm:params:oauth:grant-type:apikey" \
     --data-urlencode "response_type=cloud_iam" \
     --data-urlencode "apikey=$API_KEY" "https://iam.cloud.ibm.com/identity/token" > token.json
#END

ACCESS_TOKEN=`cat token.json | jq -r '.access_token'`

#echo $ACCESS_TOKEN

## Get Devices
function getDevices() {
    curl -s --request GET \
         --url "https://jp-tok.imfpush.cloud.ibm.com/imfpush/v1/apps/$APP_GUID/devices?expand=true" \
         --header 'accept: application/json' \
         --header "Authorization: $ACCESS_TOKEN" | jq '.'
}


## Delete Devices
function deleteDevices() {
    for i in `
    curl -s --request GET \
         --url "https://jp-tok.imfpush.cloud.ibm.com/imfpush/v1/apps/$APP_GUID/devices?expand=true" \
         --header 'accept: application/json' \
         --header "Authorization: $ACCESS_TOKEN" | jq '.devices[].deviceId' | xargs echo`
     do
         echo $i
         read KEY
         if [ "$KEY" = "y" ]; then
    
    curl -s --request DELETE \
         --url "https://jp-tok.imfpush.cloud.ibm.com/imfpush/v1/apps/$APP_GUID/devices/$i" \
         --header 'accept: application/json' \
         --header "clientSecret: $CLIENT_SECRET"
         #--header "Authorization: $ACCESS_TOKEN"
         fi
     done
}

getDevices

#deleteDevices
