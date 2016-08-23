#!/usr/bin/python3

import rw_emoncms as emoncms

emon = emoncms.EnergyMonitor()

print(emon.readHeatingTempSetpoint())