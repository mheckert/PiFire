#!/usr/bin/env python3
import subprocess
import datetime
class ReadADC:
    def __init__(self, *args, **kwargs):
        pass

    def ReadAllPorts(self):
        child = subprocess.run("/home/pi/git/max31855/readtemp", capture_output=True)
        if( child.returncode ):
            now = str(datetime.datetime.now())
            now = now[0:19] # Truncate the microseconds
            print(str(now) + ' Error Reading Temperature.')
            return None

        temp_c = float( child.stdout )
        temp_f = temp_c * 9 / 5.0 + 32

        return {"GrillTemp": temp_f,
                "GrillTr":   temp_f, #This garbage is here because control.py expects these
                "Probe1Tr":   1, #This garbage is here because control.py expects these
                "Probe2Tr":   2, #This garbage is here because control.py expects these
                "Probe1Temp":   3, #This garbage is here because control.py expects these
                "Probe2Temp":   4 #This garbage is here because control.py expects these
                }

    def SetProfiles(self, *args, **kwargs ):
        print( "adc_max31855.py does not support SetProfiles yet..." )
        
if "main" in __name__:
    ReadADC().ReadAllPorts()
