#!/usr/bin/python3

import heating_ctrl_hw as hardware
import rw_emoncms as emoncms
import time

hw = hardware.CtrlHardware()
emon = emoncms.EnergyMonitor()

# hardware allocation:
def runSolarPump ():
    hw.changeOutput(pin=0, state=1)

def stopSolarPump ():
    hw.changeOutput(pin=0, state=0)

def runHeatingPump ():
    hw.changeOutput(pin=1, state=1)

def stopHeatingPump ():
    hw.changeOutput(pin=1, state=0)

def increaseHeatingTemp ():
    hw.changeOutput(pin=2, state=0)
    hw.changeOutput(pin=3, state=1)

def decreaseHeatingTemp ():
    hw.changeOutput(pin=2, state=1)
    hw.changeOutput(pin=3, state=0)

def freezeHeatingTemp ():
    hw.changeOutput(pin=2, state=0)
    hw.changeOutput(pin=3, state=0)

def changeToFullSolarHeatExchange ():
    hw.changeOutput(pin=4, state=0)
    hw.changeOutput(pin=5, state=1)

def changeToLowSolarHeatExchange ():
    hw.changeOutput(pin=4, state=1)
    hw.changeOutput(pin=5, state=0)

def freezeSolarHeatExchange ():
    hw.changeOutput(pin=4, state=0)
    hw.changeOutput(pin=5, state=0)

#========================================




SolarPumpRunning = False
SwitchOnTime = 0

hw.initOutputs()

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
    emon.postData(TempLog, 1)
    # postDataRemoteServer(TempLog,27)

    # ========================================
    # solar-control:
    # ========================================
    # mean-temperature:
    StorageMeanTemp = (T1 * 30 + T2 * 5 + T3 * 5 + T4 * 10 + T5 * 20 + T6 * 30) / 100
    print("StorageMeanTemp = %2.1f" % StorageMeanTemp)

    if (StorageMeanTemp > 80):  # activ cooling
        SolarPumpRunning = True
        #hw.setRelais0()
        runSolarPump()
        SwitchOnTime = 0
        print("cooling")
    else:
        if SolarPumpRunning:
            SwitchOnTime += 30
            if (T9 > T8) and (SwitchOnTime > 300):
                SolarPumpRunning = False
                #hw.resetRelais0()
                stopSolarPump()
                SwitchOnTime = 0
        elif (T7 > (T6 + 4)):
            SolarPumpRunning = True
            #hw.setRelais0()
            runSolarPump()

    if (SolarPumpRunning):
        print("solar-pump running")
    else:
        print("solar-pump idle")
    # ========================================
    # heating-control:
    # ========================================

    emon.readHeatingTempSetpoint()

    time.sleep(30)