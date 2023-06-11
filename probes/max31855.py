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
import spidev
import datetime
from probes.base import ProbeInterface

'''
*****************************************
 Class Definitions
*****************************************
'''
class Max31855Result:
    def __init__(self):
        self.thermocouple_temp = 0
        self.internal_temp = 0
        self.fault = 0
        self.scv_fault = 0
        self.scg_fault = 0
        self.oc_fault = 0

class ReadProbes(ProbeInterface):

    def __init__(self, probe_info, device_info, units):
        super().__init__(probe_info, device_info, units)

    def _init_device(self):
        self.port = (0,0) #spidev0.0
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

    def read_spidev(self):
        spi = spidev.SpiDev()
        spi.open(*self.port)
        spi.max_speed_hz = 500000

        spi_data = spi.xfer2([0x00] * 4)

        spi.close()

        result = Max31855Result()
        result.thermocouple_temp = ((spi_data[0] << 8) | spi_data[1]) >> 2
        result.internal_temp = ((spi_data[2] << 8) | spi_data[3]) >> 4
        result.fault = 1 if (spi_data[1] & 0x01) else 0
        result.scv_fault = 1 if (spi_data[3] & 0x04) else 0
        result.scg_fault = 1 if (spi_data[3] & 0x02) else 0
        result.oc_fault = 1 if (spi_data[3] & 0x01) else 0

        if result.fault or result.scv_fault or result.scg_fault or result.oc_fault:
            return None

        thermocouple_temp_c = result.thermocouple_temp * 0.25
        return thermocouple_temp_c

    def _get_temp(self):
        temp_c = self.read_spidev()
        if( temp_c is None ):
            now = str(datetime.datetime.now())
            now = now[0:19] # Truncate the microseconds
            print(str(now) + ' Error Reading Temperature.')
            return None

        temp_f = temp_c * 9 / 5.0 + 32

        return (temp_c, temp_f)

    def read_all_ports(self, output_data):
        ''' Read temperature from device '''
        port = self.device_info['ports'][0]

        ret = self.get_temp()
        if ret is None:
            print("error reading max31855")
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
