# Risk Notifier

Risk notifier generates notification and pushes them to database and devices.
It has two parts:

- [generate risk notifications](/create-notification/README.md) 
- [push notifiations to devices](/push-notification/readme.md)

Risk-notifier reads the data from <code> log_risk_calculation </code? database and generates parameteric values for creating notifications based on the latest entries in the risk-calculation database. Then it writes generated notifications to risk notification database <code>log_risk_notification</code>.

Based on new entries in risk notification database, notfications are prepared for device push( [Mesh-device led/sensor](https://github.com/Hitachi-CTI-Call-For-Code-COVID-19-Team/indicator.git) and [smartphone notifications](https://github.com/Hitachi-CTI-Call-For-Code-COVID-19-Team/push-notifications.git).

This implementation comprises of smaller sequences, actions and some default [openwhisk-cloudant actions](https://github.com/ibm-functions/package-cloudant/tree/master/packages/database-actions).


For implementation, copy the repository and follow steps in indvidual directories.

- Clone the risk-notifier repository.

    ```sh
    git clone https://github.com/Hitachi-CTI-Call-For-Code-COVID-19-Team/risk-notifier.git
    ```

    **REQUIRED SETTING:**

    - Set Cloudant credentials in actions: 
    
        Input you cloudant credentials [here](/create-notification/runtimes/actions/riskNotificationFlow/prepareRelatedData_ReadAsset.py) and [here](push-notification/runtimes/actions/preparePushes.py).

    You can gets your Cloudant credentials by [delivery scripts](delivery/scripts/.credentials) or as obtained in (Cloudant-binding) steps [here](risk-calculator/README.md).

## Related:
- [Risk Calculator](https://github.com/Hitachi-CTI-Call-For-Code-COVID-19-Team/risk-calculator.git)
- [Push Notification](https://github.com/Hitachi-CTI-Call-For-Code-COVID-19-Team/push-notifications.git)
-----

##### [License](./LICENSE.txt)
