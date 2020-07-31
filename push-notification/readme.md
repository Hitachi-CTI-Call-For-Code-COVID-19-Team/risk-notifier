# Push Notifications

This repository consits of functions related to package push-notifications that prepares (only) individual staff related device-notifications and pushes to individual user devices.

- target/create namespace
- create required cloudant-bindings
- deploying the Push Notification actions/sequences
- deploying trigger

## Implementation steps
*Pre-requisite*:

- Install [IBM cloud CLI](https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-cli_install)
- [Setting up](https://cloud.ibm.com/docs/cli?topic=cli-getting-started) CLI environment.
- Deployment of [risk-calulation package](risk-calculator)

Steps to implement risk-calulator are mentioned as follows:

- target/create namespace
- create required cloudant-bindings
- deploying the actions/sequences
- deploying trigger 

This is a repeat of deployment of risk calculation package, [please check it for target namespace and cloudant binding](risk-calculator).

## Deploying the push-notification  from the CLI

- install push notification package from IBM Cloud (deploys send-message action used for sending messages)

    ```sh
    git clone https://github.com/ibm-functions/package-push-notifications.git

    cd package-push-notifications/runtimes/nodejs/

    ibmcloud fn  deploy -m manifest.yaml

    ibmcloud fn service bind imfpush push-notifications

    ibmcloud fn package get /96e4911c-15bf-4779-aaaf-cf257c10caf2/push-notifications parameters
    ```

- Clone the push notification template repo.

    ```sh
    git clone https://gitlab.rdcloud.intra.hitachi.co.jp/call-for-code-2020/covid-19/cloud-functons/risk-notifier.git

    cd push-notification/runtimes/actions
    ```

## Creating actions from the CLI

- Create an action by running the ibmcloud fn action create command.

    ```sh
    ibmcloud fn action create <action_name> <file> --kind <runtime>
    ```

    Samples

    ```sh
    ibmcloud fn action create push-notifications/createQuerySelector createQuerySelector.py --kind python:3.7

    ibmcloud fn action create push-notifications/preparePushes preparePushes.py --kind python:3.7
    ```

- Verify that the action is in your actions list.

    ```sh
    ibmcloud fn action list
    ```

## Creating a sequence from the CLI

- Create a sequence from the CLI with the ibmcloud fn action create command.

    ```sh
    ibmcloud fn action create <sequence_name> --sequence <action_1>,<action_2>
    ```

    Sample: It makes use of custom action and Open-whisk packages.

    ```sh
    ibmcloud fn action create pushNotificationFlow --sequence /_/myCloudant/read, push-notifications/createQuerySelector, /_/myCloudant/exec-query-find, push-notifications/preparePushes, push-notifications/send-message
    ```

## Creating triggers from the CLI

- Triggers must be created directly within a namespace and can't be created inside packages. This trigger detects change in Cloudant DB.

    - Pre-requisite: IBM Cloudant instance. To create an instance, see [Getting started with IBM Cloudant](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-getting-started-with-cloudant).

    Create a [/whisk.system/cloudant]((https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-pkg_cloudant)) package binding that is configured for your IBM Cloudant account. In this example, the package name is myCloudant, followed by trigger named <code>trigger_log_risk_calculation_change</code>

    Sample

    ```sh
    ibmcloud fn package bind /whisk.system/cloudant myCloudant

    ibmcloud fn trigger create trig_log_risk_notificaiton_change --feed /_/myCloudant/changes \
    --param dbname log_risk_notifier \
    --param filter "mailbox/by_status" \
    --param query_params '{"status":"new"}'    
    ```

**Example output**

    ```sh
    ok: created trigger trig_log_risk_notificaiton_change
    ```

- Verify that the trigger is created.

    ```sh
    ibmcloud fn trigger list
    ```

    **Example output**

    ```sh
    triggers
    /NAMESPACE/trig_log_risk_notificaiton_change                            private
    ```

Next, you can test the trigger or create a rule to associate the trigger with an action.

- Set rule to conect trigger to sequence
Create a rule that invokes the pushNotificationFlow sequence every time the trigger_log_risk_notificaiton_change trigger fires.

    ```sh
    ibmcloud fn rule create rulePush trig_log_risk_notificaiton_change push_notifications/pushNotificationFlow
    ```

    **Example output**

    ok: created rule rulePush

- Check that the action is being invoked by polling for activation logs.

    ```sh
    ibmcloud fn activation poll
    ```

You can see that the activations occur every minute for the trigger, the rule, and the action.

----

#### [License](./LICENCE.text)
