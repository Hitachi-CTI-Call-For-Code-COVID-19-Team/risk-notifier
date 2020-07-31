# Risk Notifier

Risk notifier generates notification and pushes them to database and devices.
It has two parts:

- [generate risk notifications](/create-notification/README.md) 
- [push notifiations to devices](/push-notification/readme.md)

Risk-notifier reads the data from **log_risk_calculation** database and generates parameteric values for creating notifications based on the latest entries in the risk-calculation database. Then it writes generated notifications to risk notification database (log_risk_notification).

Based on new entries in risk notification database, notfications are prepared for device push( Mesh led sensor and smartphone notifications).

For implementation, please check indvidual directories.

-----

##### [License](./LICENSE.txt)
