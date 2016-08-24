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


SampleTime = 3

PostDataTime = 30

#state-indicators for solar-control:
SolarPumpRunning = False
SwitchOnTime = 0

#state-indicators for heating-control:
HeatingPumpRunning = False
HeatControlSampleTime = 300
HeatingState = 0     # heating off
DecreaseTempTime = 200
IncreaseTempTime = 0
ControlSampleTime = HeatControlSampleTime
ControlError = 0


#========================================
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
    PostDataTime -= SampleTime
    if (PostDataTime<=0):
        PostDataTime = 30
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
        print("solar-pump running (cooling/heating)")
    else:
        if SolarPumpRunning:
            SwitchOnTime += SampleTime
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

    HeatTempSetpoint = emon.readHeatingTempSetpoint()

    if (HeatingState == 0):  #heating off: setpoint = 0, temperature-mixer to lowest position
        HeatingPumpRunning = False
        if (DecreaseTempTime == 0):
            HeatingState = 1
    elif (HeatingState == 1):  #heating idle: heating-system off, waiting for setpoint > 0
        HeatingPumpRunning = False
        if (HeatTempSetpoint > 0):
            HeatingState = 2
            ControlSampleTime = HeatControlSampleTime
    elif (HeatingState == 2): #heating-control: setpoint > 0, pump running, closed-loop temperature control
        HeatingPumpRunning = True
        ControlSampleTime -= SampleTime
        if (ControlSampleTime <= 0):
            ControlSampleTime = HeatControlSampleTime
            ControlError = HeatTempSetpoint - T10
            if (ControlError > 4):
                IncreaseTempTime = ControlError
            elif (ControlError < 4):
                DecreaseTempTime = ControlError
        if (HeatTempSetpoint == 0):
            HeatingState = 0
            DecreaseTempTime = 200
    else:
        HeatingPumpRunning = False
        DecreaseTempTime = 200
        HeatingState = 0


    if (HeatingPumpRunning):
        runHeatingPump()
    else:
        stopHeatingPump()

    if (DecreaseTempTime > 0):
        DecreaseTempTime -= SampleTime
        decreaseHeatingTemp()
        IncreaseTempTime = 0
    elif (IncreaseTempTime > 0):
        IncreaseTempTime -= SampleTime
        increaseHeatingTemp()
        DecreaseTempTime = 0
    else:
        freezeHeatingTemp()
        DecreaseTempTime = 0
        IncreaseTempTime = 0

    print ("HeatingState = %f", HeatingState)
    print ("DecreaseTempTime = %f", DecreaseTempTime)
    print ("IncreaseTempTime = %f", IncreaseTempTime)
    print ("HeatControlError = %f", ControlError)
    # ========================================
    time.sleep(SampleTime)