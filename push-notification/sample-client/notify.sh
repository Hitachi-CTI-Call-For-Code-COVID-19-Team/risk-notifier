#!/bin/bash -eu

icfn="ibmcloud fn"
text="text xxxxx"
title="title xxx"
#targetDevices='["B31B7A09-198D-48D0-8630-867C9DB3BC58"]'
targetDevices='["D8AA1D5F-A10E-4C09-98BA-BD481709E11D"]' # Device1(iPhone7)

$icfn action invoke push-notifications/send-message --blocking --result \
   # --param targetDeviceIds "$targetDevices" \
    --param messageText "$text" \
    --param apnstitle "$title" #\

