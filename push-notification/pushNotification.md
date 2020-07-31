# Setup to install the IBM Push Notifications package into the Cloudfunctions namespace

```sh
git clone https://github.com/ibm-functions/package-push-notifications.git
```

```bash
$ ibmcloud fn property set --namespace risk-notifier

onk: whisk namespace set to risk-notifier
```

```sh
$ cd package-push-notifications/runtimes/nodejs/
$ ibmcloud fn  deploy -m manifest.yaml
Success: Deployment completed successfully.
```

```sh
$ ibmcloud fn package list packages

/96e4911c-15bf-4779-aaaf-cf257c10caf2/push-notifications               private
```

```sh
$ ibmcloud fn service bind imfpush push-notifications
Credentials 'f61d5d98-f1e6-4feb-90ff-81c0620b6171' from 'imfpush' service instance 'mobile-app-with-push-push-1590413402291' bound to 'push-notifications'.

$ ibmcloud fn package get push-notifications parameters
```

**Example Output**

```
ok: got package push-notifications, displaying field parameters

[
    {
        "key": "__bx_creds",
        "value": {
            "imfpush": {
                "apikey": "....",
                "appGuid": "...",
                "clientSecret": "....",
                "credentials": "....",
                "iam_apikey_description": "Auto-generated for key ....",
                "iam_apikey_name": "....",
                "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
                "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::...::serviceid:ServiceId-.....",
                "instance": ".......",
                "plan": "LITE",
                "url": "https://jp-tok.imfpush.cloud.ibm.com/imfpush/v1/apps/....."
            }
        }
    }
]
```
