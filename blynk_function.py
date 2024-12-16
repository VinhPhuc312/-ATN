import BlynkLib
import serial
import time
BLYNK_AUTH_TOKEN = 'fv1QDFbmcSUs9KNC2Jm9npL75On4p04k'
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
controlMode = 0 #0: auto // 1: manual
is_enable = 0 #0:off
my_variable = 0
forward = 0 
left = 0
right = 0
backward = 0
#from TennisDetection import thread_function_1, thread_function_2
try:
    ser = serial.Serial('/dev/ttyACM0',9600)
    #ser = serial.Serial('/dev/ttyUSB0',9600)
except:
    ser = serial.Serial('/dev/ttyACM1',9600)
    #ser = serial.Serial('/dev/ttyUSB1',9600)
#FORWARD
@blynk.on("V1")
def v1_write_handler(value):
	global is_enable, forward
	if is_enable:
		if(value[0] == '1'):
			blynk.virtual_write(2, 0)
			blynk.virtual_write(3, 0)
			blynk.virtual_write(4, 0)
			forward = 'F'
		else:
			forward = 'S'
		ser.write(forward.encode())
		print(f'FORWARD:{forward}')
#TURN LEFT
@blynk.on("V2")
def v2_write_handler(value):
	global is_enable, left
	if is_enable:
		if(value[0] == '1'):
			blynk.virtual_write(1, 0)
			blynk.virtual_write(3, 0)
			blynk.virtual_write(4, 0)
			left ='L'
		else:
			left = 'S'
		ser.write(left.encode())
		print(f'LEFT:{left}')
#BACKWARD  
@blynk.on("V3")
def v3_write_handler(value):
	global is_enable, backward
	if is_enable:
		if(value[0] == '1'):
			blynk.virtual_write(1, 0)
			blynk.virtual_write(2, 0)
			blynk.virtual_write(4, 0)
			backward = 'B'
		else:
			backward = 'S'
		ser.write(backward.encode())
		print(f'BACKWARD:{backward}')
#TURN RIGHT
@blynk.on("V4")
def v4_write_handler(value):
	global is_enable, right
	if is_enable:
		if(value[0] == '1'):
			blynk.virtual_write(1, 0)
			blynk.virtual_write(3, 0)
			blynk.virtual_write(2, 0)
			right = 'R'
		else:
			right = 'S'
		ser.write(right.encode())
		print(f'RIGHT:{right}')
#MODE

@blynk.on("V5")
def v5_write_handler(value):
	global controlMode, is_enable
	controlMode = value[0]
	print(f'controlMode: {controlMode}')
	if controlMode != '0' and controlMode != 0:
		blynk.virtual_write(1, 0)
		blynk.virtual_write(2, 0)
		blynk.virtual_write(3, 0)
		blynk.virtual_write(4, 0)
		ser.write('M'.encode())
		is_enable = 1 # Bat mode manual
		print('Mode: Manual')
	else:
		blynk.virtual_write(1, 0)
		blynk.virtual_write(2, 0)
		blynk.virtual_write(3, 0)
		blynk.virtual_write(4, 0)
		is_enable = 0# Bat mode auto
		ser.write('A'.encode())
		print(controlMode)
#CHECK_CONNECTION
@blynk.on("connected")
def blynk_connected():
    print("Raspberry Pi Connected to New Blynk")
def blynk_activate():
    while True:
        blynk.run() 
        time.sleep(0.5) 
