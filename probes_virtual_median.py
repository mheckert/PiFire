#!/usr/bin/env python3

'''
*****************************************
PiFire Probes Virtual Probe Median Module 
*****************************************

Description: 
  This module is a virtual probe device that will find the median any number of other probe inputs.  Probe labels must be defined in config data.
	
	Ex Device Definition: 
	
	device = {
			'device' : 'your_device_name',	# Unique name for the device
			'module' : 'virtual_median',	# Must be populated for this module to load properly
			'ports' : ['VIRT0'], 			# A port must be defined, with the labels of the probes to utilize in config data
			'config' : {
			  "probes_list" : ["Grill1", "Grill2"]	# List of probe labels to utilize
			} 
		}
'''

'''
*****************************************
 Imported Libraries
*****************************************
'''

from probes_base import ProbeInterface
from statistics import median

'''
*****************************************
 Class Definitions 
*****************************************
'''

class ReadProbes(ProbeInterface):

	def __init__(self, probe_info, device_info, units):
		super().__init__(probe_info, device_info, units)
	
	def read_all_ports(self, output_data):
		''' Find the probes to average '''
		for port in self.port_map:
			temp_list = []
			for probe in self.device_info['config']['probes_list']:
				if probe in output_data['primary']:
					temp_list.append(output_data['primary'][probe])
				elif probe in output_data['food']:
					temp_list.append(output_data['food'][probe])
				elif probe in output_data['aux']:
					temp_list.append(output_data['aux'][probe])			
			
			''' Get average temperature and store it in the output data structure'''
			if port == self.primary_port:
				self.output_data['primary'][self.port_map[port]] = median(temp_list)
			elif port in self.food_ports:
				self.output_data['food'][self.port_map[port]] = median(temp_list)
			elif port in self.aux_ports:
				self.output_data['aux'][self.port_map[port]] = median(temp_list)
			
			''' Set Tr value to 0 since we are averaging temperature outputs '''
			self.output_data['tr'][self.port_map[port]] = 0

		return self.output_data

