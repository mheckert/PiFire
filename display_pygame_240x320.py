#!/usr/bin/env python3

# *****************************************
# PiFire Display Interface Library
# *****************************************
#
# Description: This library supports using pygame 
# on your development PC for debug and development 
# purposes. Likely only works in an desktop 
# environment.  Tested on Ubuntu 20.04.  
#
# Edit the WIDTH / HEIGHT constants below to 
# simulate your screen size. 
# 
# Dependancies:
#   sudo pip3 install pygame Pillow 
#   sudo apt install ttf-mscorefonts-installer
#
# *****************************************

# *****************************************
# Imported Libraries
# *****************************************
import pygame  
from PIL import Image, ImageDraw, ImageFont
import time

class Display:

	def __init__(self, units='F'):
		# Set Display Width and Height.  Modify for your needs.   
		self.WIDTH = 320
		self.HEIGHT = 240
		self.units = units
		# Activate PyGame
		pygame.init()

		# Create Display Surface
		self.display_surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) 

		# set the pygame window name 
		pygame.display.set_caption('PiFire Device Display')

		self.DisplaySplash()
		time.sleep(0.5) # Keep the splash up for three seconds on boot-up - you can certainly disable this if you want 


	def DisplayStatus(self, in_data, status_data):
		self.units = status_data['units']  # Update units in case there was a change since instantiation
		# Create canvas
		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), color=(0, 0, 0))

		background = Image.open('background.jpg')

		# Resize the boot-splash
		background = background.resize((self.WIDTH, self.HEIGHT))

		# Set the position 
		position = (0,0)

		# Paste the splash screen onto the canvas
		img.paste(background, position)

		# Create drawing object
		draw = ImageDraw.Draw(img)

		# Grill Temp Circle
		draw.ellipse((80, 10, 240, 170), fill=(50, 50, 50)) # Grey Background Circle
		if in_data['GrillTemp'] < 0:
			endpoint = 0
		elif self.units == 'F':
			endpoint = ((360*in_data['GrillTemp']) // 600) + 90
		else:
			endpoint = ((360*in_data['GrillTemp']) // 300) + 90
		draw.pieslice((80, 10, 240, 170), start=90, end=endpoint, fill=(200, 0, 0)) # Red Arc for Temperature
		if (in_data['GrillSetPoint'] > 0):
			if self.units == 'F':
				setpoint = ((360*in_data['GrillSetPoint']) // 600) + 90
			else:
				setpoint = ((360*in_data['GrillSetPoint']) // 300) + 90
			draw.pieslice((80, 10, 240, 170), start=setpoint-2, end=setpoint+2, fill=(255, 255, 0)) # Yellow Arc for SetPoint
		draw.ellipse((90, 20, 230, 160), fill=(0, 0, 0)) # Black Circle for Center

		# Grill Temp Label
		font = ImageFont.truetype("trebuc.ttf", 16)
		text = "Grill"
		(font_width, font_height) = font.getsize(text)
		draw.text((self.WIDTH//2 - font_width//2,20), text, font=font, fill=(255,255,255))

		# Grill Set Point (Small Centered Top)
		if (in_data['GrillSetPoint'] > 0):
			font = ImageFont.truetype("trebuc.ttf", 16)
			text = ">" + str(in_data['GrillSetPoint'])[:5] + "<"
			(font_width, font_height) = font.getsize(text)
			draw.text((self.WIDTH//2 - font_width//2, 45 - font_height//2), text, font=font, fill=(0,200,255))

		# Grill Temperature (Large Centered) 
		if(self.units == 'F'):
			font = ImageFont.truetype("trebuc.ttf", 80)
			text = str(in_data['GrillTemp'])[:5]
			(font_width, font_height) = font.getsize(text)
			draw.text((self.WIDTH//2 - font_width//2,40), text, font=font, fill=(255,255,255))
		else: 
			font = ImageFont.truetype("trebuc.ttf", 55)
			text = str(in_data['GrillTemp'])[:5]
			(font_width, font_height) = font.getsize(text)
			draw.text((self.WIDTH//2 - font_width//2,56), text, font=font, fill=(255,255,255))

		# Draw Grill Temp Scale Label
		text = "°" + self.units
		font = ImageFont.truetype("trebuc.ttf", 24)
		(font_width, font_height) = font.getsize(text)
		draw.text((self.WIDTH//2 - font_width//2, self.HEIGHT//2 - font_height//2 + 10), text, font=font, fill=(255, 255, 255))

		# PROBE1 Temp Circle
		draw.ellipse((10, self.HEIGHT//2 + 10, 110, self.HEIGHT//2 + 110), fill=(50, 50, 50))
		if in_data['Probe1Temp'] < 0:
			endpoint = 0
		elif self.units == 'F':
			endpoint = ((360*in_data['Probe1Temp']) // 300) + 90
		else:
			endpoint = ((360*in_data['Probe1Temp']) // 150) + 90
		draw.pieslice((10, self.HEIGHT//2 + 10, 110, self.HEIGHT//2 + 110), start=90, end=endpoint, fill=(3, 161, 252))
		if (in_data['Probe1SetPoint'] > 0):
			if self.units == 'F':
				setpoint = ((360*in_data['Probe1SetPoint']) // 300) + 90
			else: 
				setpoint = ((360*in_data['Probe1SetPoint']) // 150) + 90
			draw.pieslice((10, self.HEIGHT//2 + 10, 110, self.HEIGHT//2 + 110), start=setpoint-2, end=setpoint+2, fill=(255, 255, 0)) # Yellow Arc for SetPoint
		draw.ellipse((20, self.HEIGHT//2 + 20, 100, self.HEIGHT//2 + 100), fill=(0, 0, 0))

		# PROBE1 Temp Label
		font = ImageFont.truetype("trebuc.ttf", 16)
		text = "Probe-1"
		(font_width, font_height) = font.getsize(text)
		draw.text((60 - font_width//2, self.HEIGHT//2 + 40 - font_height//2), text, font=font, fill=(255,255,255))

		# PROBE1 Temperature (Large Centered) 
		if(self.units == 'F'):
			font = ImageFont.truetype("trebuc.ttf", 36)
		else:
			font = ImageFont.truetype("trebuc.ttf", 30)
		text = str(in_data['Probe1Temp'])[:5]
		(font_width, font_height) = font.getsize(text)
		draw.text((60 - font_width//2, self.HEIGHT//2 + 60 - font_height//2), text, font=font, fill=(255,255,255))

		# PROBE1 Set Point (Small Centered Bottom)
		if (in_data['Probe1SetPoint'] > 0):
			font = ImageFont.truetype("trebuc.ttf", 16)
			text = ">" + str(in_data['Probe1SetPoint'])[:5] + "<"
			(font_width, font_height) = font.getsize(text)
			draw.text((60 - font_width//2, self.HEIGHT//2 + 85 - font_height//2), text, font=font, fill=(0,200,255))

		# PROBE2 Temp Circle
		draw.ellipse((self.WIDTH - 110, self.HEIGHT//2 + 10, self.WIDTH - 10, self.HEIGHT//2 + 110), fill=(50, 50, 50))
		if in_data['Probe2Temp'] < 0:
			endpoint = 0
		elif self.units == 'F':
			endpoint = ((360*in_data['Probe2Temp']) // 300) + 90
		else:
			endpoint = ((360*in_data['Probe2Temp']) // 150) + 90
		draw.pieslice((self.WIDTH - 110, self.HEIGHT//2 + 10, self.WIDTH - 10, self.HEIGHT//2 + 110), start=90, end=endpoint, fill=(3, 161, 252))
		if (in_data['Probe2SetPoint'] > 0):
			if self.units == 'F':
				setpoint = ((360*in_data['Probe2SetPoint']) // 300) + 90
			else: 
				setpoint = ((360*in_data['Probe2SetPoint']) // 150) + 90
			draw.pieslice((self.WIDTH - 110, self.HEIGHT//2 + 10, self.WIDTH - 10, self.HEIGHT//2 + 110), start=setpoint-2, end=setpoint+2, fill=(255, 255, 0)) # Yellow Arc for SetPoint
		draw.ellipse((self.WIDTH - 100, self.HEIGHT//2 + 20, self.WIDTH - 20, self.HEIGHT//2 + 100), fill=(0, 0, 0))

		# PROBE2 Temp Label
		font = ImageFont.truetype("trebuc.ttf", 16)
		text = "Probe-2"
		(font_width, font_height) = font.getsize(text)
		draw.text((self.WIDTH - 60 - font_width//2, self.HEIGHT//2 + 40 - font_height//2), text, font=font, fill=(255,255,255))

		# PROBE2 Temperature (Large Centered) 
		if(self.units == 'F'):
			font = ImageFont.truetype("trebuc.ttf", 36)
		else:
			font = ImageFont.truetype("trebuc.ttf", 30)
		text = str(in_data['Probe2Temp'])[:5]
		(font_width, font_height) = font.getsize(text)
		draw.text((self.WIDTH - 60 - font_width//2, self.HEIGHT//2 + 60 - font_height//2), text, font=font, fill=(255,255,255))

		# PROBE2 Set Point (Small Centered Bottom)
		if (in_data['Probe2SetPoint'] > 0):
			font = ImageFont.truetype("trebuc.ttf", 16)
			text = ">" + str(in_data['Probe2SetPoint'])[:5] + "<"
			(font_width, font_height) = font.getsize(text)
			draw.text((self.WIDTH - 60 - font_width//2, self.HEIGHT//2 + 85 - font_height//2), text, font=font, fill=(0,200,255))

		# Active Outputs 
		font = ImageFont.truetype("FA-Free-Solid.otf", 36)
		if(status_data['outpins']['fan']==0):
			#F = Fan (Upper Left), 40x40, origin 10,10
			text = '\uf863'
			(font_width, font_height) = font.getsize(text)
			draw = self.rounded_rectangle(draw, (self.WIDTH//8 - 22, self.HEIGHT//6 - 22, self.WIDTH//8 + 22, self.HEIGHT//6 + 22), 5, (0, 100, 255))
			draw = self.rounded_rectangle(draw, (self.WIDTH//8 - 20, self.HEIGHT//6 - 20, self.WIDTH//8 + 20, self.HEIGHT//6 + 20), 5, (0, 0, 0))
			draw.text((self.WIDTH//8 - font_width//2 + 1, self.HEIGHT//6 - font_height//2), text, font=font, fill=(0,100,255))
		if(status_data['outpins']['igniter']==0):
			# I = Igniter(Center Right)
			text = '\uf46a'
			(font_width, font_height) = font.getsize(text)
			draw = self.rounded_rectangle(draw, (7*(self.WIDTH//8) - 22, self.HEIGHT//2.5 - 22, 7*(self.WIDTH//8) + 22, self.HEIGHT//2.5 + 22), 5, (255, 200, 0))
			draw = self.rounded_rectangle(draw, (7*(self.WIDTH//8) - 20, self.HEIGHT//2.5 - 20, 7*(self.WIDTH//8) + 20, self.HEIGHT//2.5 + 20), 5, (0, 0, 0))
			draw.text((7*(self.WIDTH//8) - font_width//2, self.HEIGHT//2.5 - font_height//2), text, font=font, fill=(255,200,0))
		if(status_data['outpins']['auger']==0):
			# A = Auger (Center Left)
			text = '\uf101'
			(font_width, font_height) = font.getsize(text)
			draw = self.rounded_rectangle(draw, (self.WIDTH//8 - 22, self.HEIGHT//2.5 - 22, self.WIDTH//8 + 22, self.HEIGHT//2.5 + 22), 5, (0, 255, 0))
			draw = self.rounded_rectangle(draw, (self.WIDTH//8 - 20, self.HEIGHT//2.5 - 20, self.WIDTH//8 + 20, self.HEIGHT//2.5 + 20), 5, (0, 0, 0))
			draw.text((self.WIDTH//8 - font_width//2 + 1, self.HEIGHT//2.5 - font_height//2 - 2), text, font=font, fill=(0,255,0))

		# Notification Indicator (Right)
		show_notify_indicator = False
		for item in status_data['notify_req']:
			if status_data['notify_req'][item] == True:
				show_notify_indicator = True
		if(show_notify_indicator == True):
			font = ImageFont.truetype("FA-Free-Solid.otf", 36)
			text = '\uf0f3'
			(font_width, font_height) = font.getsize(text)
			draw = self.rounded_rectangle(draw, (7*(self.WIDTH//8) - 22, self.HEIGHT//6 - 22, 7*(self.WIDTH//8) + 22, self.HEIGHT//6 + 22), 5, (255,255,0))
			draw = self.rounded_rectangle(draw, (7*(self.WIDTH//8) - 20, self.HEIGHT//6 - 20, 7*(self.WIDTH//8) + 20, self.HEIGHT//6 + 20), 5, (0, 0, 0))
			draw.text((7*(self.WIDTH//8) - font_width//2 + 1, self.HEIGHT//6 - font_height//2), text, font=font, fill=(255,255,0))

		# Smoke Plus Inidicator
		if(status_data['s_plus'] == True) and ((status_data['mode']=='Smoke') or (status_data['mode']=='Hold')):
			draw = self.rounded_rectangle(draw, (7*(self.WIDTH//8) - 22, self.HEIGHT//2.5 - 22, 7*(self.WIDTH//8) + 22, self.HEIGHT//2.5 + 22), 5, (150, 0, 255))
			draw = self.rounded_rectangle(draw, (7*(self.WIDTH//8) - 20, self.HEIGHT//2.5 - 20, 7*(self.WIDTH//8) + 20, self.HEIGHT//2.5 + 20), 5, (0, 0, 0))
			font = ImageFont.truetype("FA-Free-Solid.otf", 32)
			text = '\uf0c2' # FontAwesome Icon for Cloud (Smoke)
			(font_width, font_height) = font.getsize(text)
			draw.text((7*(self.WIDTH//8) - font_width//2, self.HEIGHT//2.5 - font_height//2), text, font=font, fill=(100,0,255))
			font = ImageFont.truetype("FA-Free-Solid.otf", 24)
			text = '\uf067' # FontAwesome Icon for PLUS 
			(font_width, font_height) = font.getsize(text)
			draw.text((7*(self.WIDTH//8) - font_width//2, self.HEIGHT//2.5 - font_height//2 + 3), text, font=font, fill=(0,0,0))

		# Grill Hopper Level (Lower Center)
		font = ImageFont.truetype("trebuc.ttf", 16)
		text = "Hopper:" + str(status_data['hopper_level']) + "%"
		(font_width, font_height) = font.getsize(text)
		if(status_data['hopper_level'] > 70): 
			hopper_color = (0,255,0)
		elif(status_data['hopper_level'] > 30): 
			hopper_color = (255,150,0)
		else:
			hopper_color = (255,0,0)
		draw = self.rounded_rectangle(draw, (self.WIDTH//2 - font_width//2 - 7, 156 - font_height//2, self.WIDTH//2 + font_width//2 + 7, 166 + font_height//2), 5, hopper_color)
		draw = self.rounded_rectangle(draw, (self.WIDTH//2 - font_width//2 - 5, 158 - font_height//2, self.WIDTH//2 + font_width//2 + 5, 164 + font_height//2), 5, (0,0,0))
		draw.text((self.WIDTH//2 - font_width//2, 160 - font_height//2), text, font=font, fill=hopper_color)

		# Current Mode (Bottom Center)
		font = ImageFont.truetype("trebuc.ttf", 36)
		text = status_data['mode'] #+ ' Mode'
		(font_width, font_height) = font.getsize(text)
		draw = self.rounded_rectangle(draw, (self.WIDTH//2 - font_width//2 - 7, self.HEIGHT - font_height - 2, self.WIDTH//2 + font_width//2 + 7, self.HEIGHT-2), 5, (3, 161, 252))
		draw = self.rounded_rectangle(draw, (self.WIDTH//2 - font_width//2 - 5, self.HEIGHT - font_height, self.WIDTH//2 + font_width//2 + 5, self.HEIGHT-4), 5, (255,255,255))
		draw.text((self.WIDTH//2 - font_width//2, self.HEIGHT - font_height - 6), text, font=font, fill=(0,0,0))

		# Convert to PyGame and Display
		strFormat = img.mode
		size = img.size
		raw_str = img.tobytes("raw", strFormat)

		self.display_image = pygame.image.fromstring(raw_str, size, strFormat)

		self.display_surface.fill((255,255,255))
		self.display_surface.blit(self.display_image, (0, 0))

		pygame.display.update() 


	def DisplaySplash(self):
		# Create canvas
		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), color=(0, 0, 0))

		splash = Image.open('color-boot-splash.png')

		(splash_width, splash_height) = splash.size
		splash_width *= 2
		splash_height *= 2

		# Resize the boot-splash
		splash = splash.resize((splash_width, splash_height))

		# Set the position 
		position = ((self.WIDTH - splash_width)//2, (self.HEIGHT - splash_height)//2)

		# Paste the splash screen onto the canvas
		img.paste(splash, position)

		# Convert to PyGame and Display
		strFormat = img.mode
		size = img.size
		raw_str = img.tobytes("raw", strFormat)
		self.display_image = pygame.image.fromstring(raw_str, size, strFormat)

		self.display_surface.fill((255,255,255))
		self.display_surface.blit(self.display_image, (0, 0))

		pygame.display.update() 


	def ClearDisplay(self):
		# Fill with black
		self.display_surface.fill((0,0,0))
		pygame.display.update() 


	def DisplayText(self, text):
		# Create canvas
		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), color=(0, 0, 0))

		# Create drawing object
		draw = ImageDraw.Draw(img)

		font = ImageFont.truetype("impact.ttf", 42)
		(font_width, font_height) = font.getsize(text)
		draw.text((self.WIDTH//2 - font_width//2, self.HEIGHT//2 - font_height//2), text, font=font, fill=255)

		# Convert to PyGame and Display
		strFormat = img.mode
		size = img.size
		raw_str = img.tobytes("raw", strFormat)

		self.display_image = pygame.image.fromstring(raw_str, size, strFormat)

		self.display_surface.fill((255,255,255))
		self.display_surface.blit(self.display_image, (0, 0))

		pygame.display.update() 
	
	def rounded_rectangle(self, draw, xy, rad, fill=None):
		x0, y0, x1, y1 = xy
		draw.rectangle([ (x0, y0 + rad), (x1, y1 - rad) ], fill=fill)
		draw.rectangle([ (x0 + rad, y0), (x1 - rad, y1) ], fill=fill)
		draw.pieslice([ (x0, y0), (x0 + rad * 2, y0 + rad * 2) ], 180, 270, fill=fill)
		draw.pieslice([ (x1 - rad * 2, y1 - rad * 2), (x1, y1) ], 0, 90, fill=fill)
		draw.pieslice([ (x0, y1 - rad * 2), (x0 + rad * 2, y1) ], 90, 180, fill=fill)
		draw.pieslice([ (x1 - rad * 2, y0), (x1, y0 + rad * 2) ], 270, 360, fill=fill)
		return(draw)

	def EventDetect(self):
		return()