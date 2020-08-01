# Generate Risk Notifcation

Risk notification package consits of one sequence named <code>riskNotificationFlow</code>. 


![risk-notifier](/images/risk-notifier.png)


For deploying please follow these steps:

- target/create namespace
- create required cloudant-bindings
- deploying the Risk Notifier actions/sequences
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

## Deploying the Risk Notifier from the CLI

Use the CLI to deploy the Risk Notifier template.

- Deploy the template. You must include a package name to contain your action. Replace <name> with a custom name for your package.

    ```sh
    PACKAGE_NAME=<name> ibmcloud fn deploy -m manifest.yaml
    ```

    Sample

    ```sh
    PACKAGE_NAME= risk-notifier ibmcloud fn deploy -m manifest.yaml
    ```

After the template deploys, you can make further edits to the code to customize it as needed, or go back and check out the catalog of available templates.

## Creating actions from the CLI

- Create an action by running the ibmcloud fn action create command.

    ```sh
    ibmcloud fn action create <action_name> <file> --kind <runtime>
    ```

    Samples

    ```sh
    cd create-notification/runtimes/actions/riskNotificationFlow

    ibmcloud fn action create prepareRelatedData_ReadAsset prepareRelatedData_ReadAsset.py --kind python:3.7

    ibmcloud fn action create createRiskNotification createRiskNotification.py --kind python:3.7

    ibmcloud fn action create formatDataToWrite formatDataToWrite.py --kind python:3.7
    ```

- Verify that the actions are in your actions list.

    ```sh
    ibmcloud fn action list
    ```

## Creating a sequence from the CLI

- Create a sequence from the CLI with the ibmcloud fn action create command.

    ```sh
    ibmcloud fn action create <sequence_name> --sequence <action_1>,<action_2>
    ```

    Sample: sequence name is riskNotificationFlow

    ```sh
    ibmcloud fn action create riskNotificationFlow --sequence /_/myCloudant/read,prepareRelatedData_ReadAsset,createRiskNotification,formatDataToWrite,/_/myCloudant/write
    ```

## Creating triggers from the CLI

- Triggers must be created directly within a namespace and can't be created inside packages. This trigger detects change in Cloudant DB.

    - Pre-requisite: IBM Cloudant instance. To create an instance, see [Getting started with IBM Cloudant](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-getting-started-with-cloudant).

    Create a [/whisk.system/cloudant]((https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-pkg_cloudant)) package binding that is configured for your IBM Cloudant account. In this example, the package name is myCloudant, followed by trigger named <code> trigger_log_risk_calculation_change </code>

    Sample

    ```sh
    ibmcloud fn package bind /whisk.system/cloudant myCloudant

    ibmcloud fn trigger create trig_log_risk_calc_change --feed /_/myCloudant/changes \
    --param dbname log-risk-calculation \
    --param filter "mailbox/by_status" \
    --param query_params '{"status":"new"}'
    ```

    **Example output**

    ```sh
    ok: created trigger trig_log_risk_calc_change
    ```

- Verify that the trigger is created.

    ```sh
    ibmcloud fn trigger list
    ```

    **Example output**

    ```sh
    triggers
    /NAMESPACE/trig_log_risk_calc_change                           private
    ```

Next, you can test the trigger or create a rule to associate the trigger with an action.

- Set rule to conect trigger to sequence
Create a rule that invokes the riskNotificationFlow sequence every time the trig_log_risk_calc_change trigger gets fired.

    ```sh
    ibmcloud fn rule create ruleRN trig_log_risk_calc_change riskNotificationFlow
    ```

    **Example output**

    ok: created rule ruleRN

- Check that the action is being invoked by polling for activation logs.

    ```sh
    ibmcloud fn activation poll
    ```

You can see that the activations occur every minute for the trigger, the rule, and the action.

---------
#### [Licence](./LICENSE.txt)
