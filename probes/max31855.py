#!/usr/bin/env python3

'''
*****************************************
PiFire Probes MAX31855 Module
*****************************************

Description:
  This uses a precompiled c program accessing spidev0.0 to read 31855 data

'''

'''
*****************************************
 Imported Libraries
*****************************************
'''
import subprocess
import datetime
from probes.base import ProbeInterface

'''
*****************************************
 Class Definitions
*****************************************
'''

class ReadProbes(ProbeInterface):

    def __init__(self, probe_info, device_info, units):
        super().__init__(probe_info, device_info, units)

    def _init_device(self):
        pass

    #Get temp with retry
    def get_temp(self):
        retries = 10
        while retries > 0:
            ret = self._get_temp()
            if( ret ):
                return ret
            else:
                retries -= 1
        return None

    def _get_temp(self):
        child = subprocess.run("/home/pi/git/max31855/readtemp", capture_output=True)
        if( child.returncode ):
            now = str(datetime.datetime.now())
            now = now[0:19] # Truncate the microseconds
            print(str(now) + ' Error Reading Temperature.')
            return None

        temp_c = float( child.stdout )
        temp_f = temp_c * 9 / 5.0 + 32

        return (temp_c, temp_f)

    def read_all_ports(self, output_data):
        ''' Read temperature from device '''
        port = self.device_info['ports'][0]

        ret = get_temp()
        if ret is None:
            return
        (tempC, tempF) = ret

        ''' Get average temperature from the queue and store it in the output data structure'''
        if port == self.primary_port:
                self.output_data['primary'][self.port_map[port]] = tempF if self.units == 'F' else tempC
        elif port in self.food_ports:
                self.output_data['food'][self.port_map[port]] = tempF if self.units == 'F' else tempC
        elif port in self.aux_ports:
                self.output_data['aux'][self.port_map[port]] = tempF if self.units == 'F' else tempC

        return self.output_data
