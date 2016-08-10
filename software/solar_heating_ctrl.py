#!/usr/bin/python3

import heating_ctrl_hw as hardware
import time

hw = hardware.CtrlHardware()

SolarPumpRunning = False
SwitchOnTime = 0

hw.resetRelais0()

while True:
    T1 = hw.readTemp(0)
    T2 = hw.readTemp(1)
    T3 = hw.readTemp(2)
    T4 = hw.readTemp(3)
    T5 = hw.readTemp(4)
    T6 = hw.readTemp(5)
    T7 = hw.readTemp(6)
    T8 = hw.readTemp(7)
    T9 = hw.readTemp(8)
    T10 = hw.readTemp(9)
    T11 = hw.readTemp(10)

    TempLog = "T1:%2.1f,T2:%2.1f,T3:%2.1f,T4:%2.1f,T5:%2.1f,T6:%2.1f,T7:%2.1f,T8:%2.1f,T9:%2.1f,T10:%2.1f,T11:%2.1f" % (
    T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11)
    print("T1 = %2.1f, T2 = %2.1f, T3 = %2.1f, T4 = %2.1f, T5 = %2.1f, T6 = %2.1f, T7 = %2.1f" % (
    T1, T2, T3, T4, T5, T6, T7))
    print("T8 = %2.1f, T9 = %2.1f, T10 = %2.1f, T11 = %2.1f" % (T8, T9, T10, T11))
    hw.postData(TempLog, 1)
    # postDataRemoteServer(TempLog,27)

    # mean-temperature:
    StorageMeanTemp = (T1 * 30 + T2 * 5 + T3 * 5 + T4 * 10 + T5 * 20 + T6 * 30) / 100

    if (StorageMeanTemp > 81):  # activ cooling
        SolarPumpRunning = True
        hw.setRelais0()
        SwitchOnTime = 0
    else:
        if SolarPumpRunning:
            SwitchOnTime += 30
            if (T9 > T8) and (SwitchOnTime > 300):
                SolarPumpRunning = False
                hw.resetRelais0()
                SwitchOnTime = 0
        elif (T7 > (T6 + 4)):
            SolarPumpRunning = True
            hw.setRelais0()

    time.sleep(30)