from gpiozero import PWMLED
from time import sleep
import time
from gpiozero import LightSensor
import threading
from queue import Queue
import numpy as np

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] #abc enum for checksum
morse = {".-":"A", "-...":"B", "-.-.":"C", "-..":"D", ".":"E", "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J", "-.-":"K", ".-..":"L", "--":"M", "-.":"N", "---":"O", ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T", "..-":"U", "...-":"V", ".--":"W", "-..-":"X", "-.--":"Y", "--..":"Z", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0", "-..-.":"/", "":""}
rev_m  = {"A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", "M":"--", "N":"-.", "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T": "-", "U":"..-", "V":"...-", "W":".--", "X":"-..-", "Y":"-.--", "Z":"--..", "1":".----", "2":"..---", "3":"...--", "4":"....-", "5":".....", "6":"-....", "7":"--...", "8":"---..", "9":"----.", "0":"-----", "/":"-..-.", "":""}

LONG = 4 # long delay -> -
SHORT = 2 # short delay -> .
#OFF_DELAY = 1
EOB = "-..-." # /
SEPERATOR = "-..-.." # #

class Transmitter:

	def __init__(self, pin1=17, pin2=18, mode="led"):
		if mode == "led":
			self.led = PWMLED(pin1) #setting up led pin
			self.led.value = 0
		elif mode == "ldr":
			self.ldr = LightSensor(pin2) # setting up lightsensor pin
		self.pin1 = int(pin1) # LED
		self.pin2 = int(pin2) # LightSensor
		
	def __blink(self, delay, OFF_DELAY=1): # declaring private method
		delay = float(delay) # important - 0.5 --> 0
		self.led.value = 0 # turn led off 
		self.led.value = 1 # turn led on
		#print("sleeping on", str(delay))
		sleep(delay)
		self.led.value = 0
		#print("sleeping off", str(OFF_DELAY))
		sleep(OFF_DELAY)
		
	def decrypt(self, msg):
		msg = str(msg)
		dec = ""
		tmp = ""
		for c in msg:
			if c == "/":
				dec += " "
			elif c == " ":
				dec += morse[tmp]
				tmp = ""
			else:
				tmp += c
		if tmp != "": dec += morse[tmp]
		return(dec)
		
	def encrypt(self, msg):
		enc = ""
		for c in msg:
			try:
				int(c)
				enc += rev_m[str(c)] + " "
			except ValueError:
				if c == " ":
					enc += "/ "
				else:
					enc += rev_m[c.upper()] + " "
		return(enc)

	def __send(self, sig, mode=""): # declaring private send method
			sig = str(sig)
			if mode == "space":
				OFF_DELAY = 4
				#print(" ", end="", flush=True)
			else:
				OFF_DELAY = 1
			if sig == ".":
				#print("blinking short")
				#print(".", end="", flush=True)
				self.__blink(SHORT, OFF_DELAY)
			elif sig == "-":
				#print("blinking long")
				#print("-", end="",flush=True)
				self.__blink(LONG, OFF_DELAY)
			elif sig == "/":
				#print("blinking EOB")
				for sig in EOB: # could hang program - sorry
					self.__send(sig)
				
	def send(self, morse, m=""):
		ms = ""
		morse = str(morse)
		print('"' + morse + '"')
		print("live: ", end="", flush=True)
		#for i in range(0,1): # sending msg two times
		for i in range(0, len(morse)):
			sig = morse[i]
			print(sig, end="", flush=True)
			if i != len(morse) -1:
				if morse[i+1] == " ":
					self.__send(sig, "space")
				else:
					self.__send(sig) 
		if m == "":
			for sig in SEPERATOR:
				self.__send(sig)
			checksum = str(self.checksum(self.decrypt(morse)))
			print("\nchecksum: " + checksum)
			print("encrypted: " + str(self.encrypt(checksum)) + "\n")
			self.send(self.encrypt(str(checksum)), m="check")
			sleep(1)
		return(0)
		
	def __round_brightness(self, value):
		if value > 0.5:
			return("-") # dark
		elif value < 0.5:
			return("+") # bright
	def __sigs_to_morse(self, sigs):
		morse = ""
		count_long = np.arange((float(LONG)/0.5)-2, (float(LONG/0.5))+2, 1)
		count_short = np.arange((float(SHORT)/0.5)-2, (float(SHORT/0.5))+2, 1)
		count_space = np.arange((float(4)/0.5)-2, (float(4/0.5))+2, 1) # OFF_DELAY:4
		for sig in sigs:
			if sig.count("-") in count_space:
				morse += " "
			if sig.count("+") in count_long:
				morse += "-"
			elif sig.count("+") in count_short:
				morse += "."
		#morse = ".-" + SEPERATOR + "-----"
		return(morse.replace(SEPERATOR, "#").replace(EOB, "/")) # removing seperators from message
	def __recv(self):
			msg = ""
			data = ""
			status = ""
			delta = 0
			while self.ldr.value > 0.5: pass
			print("Beginning to listen...")
			start = time.time()
			while delta < LONG+2:
				if status != self.__round_brightness(self.ldr.value):
					#print(";", end="")
					start = time.time()
					data += ";"
					print(";", end="", flush=True)
				status = self.__round_brightness(self.ldr.value)
				data = data + status
				print(status, end="", flush=True)
				time.sleep(0.5)
				#print(delta)
				#input("PRESS ENTER")
				#print(status, end="")
				delta = time.time() - start
			print("evaluating data...")
			sigs = data.split(";")
			print("raw sigs: ", sigs)
			del sigs[0]
			del sigs[-1]
			morse_full = self.__sigs_to_morse(sigs)
			print(morse_full.split("#"))
			if len(morse_full.split("#"))<2:
				print("message corrupted!")
				return(-1)
			morse = morse_full.split("#")[0]
			checksum = self.decrypt(morse_full.split("#")[1])
			print(sigs)
			print("________________________________")
			print("checksum: " + checksum)
			print("morse: " + morse)
			msg = self.decrypt(morse)
			return(msg, checksum)
		
	def recv(self):
			# receiving msg
			#for i in range(0, 2): # receiving 2 times to avoid packet loss - but it is still possible
			msg, check = self.__recv()
			#print("message from checksum: ", self.decrypt(msg))
			try:
				if int(self.checksum(msg)) == int(check):
					return(msg) # if checksum matches return message
				else:
					print("fragmented msg: " + str(msg))
					return(-1) # if checksum doesnt match return an error
			except:
				print("checksum corrupted!")
				print("fragmented msg: " + str(msg))
				return(-1)
	
	def checksum(self, msg):
		#msg = str(msg.upper()) # making message uppercase (not every char is in abc - yet)
		sum = 0
		for c in msg:
			sum += ord(str(c))
			#for i in range(0, len(abc)):
			#	if c == abc[i]:
			#		sum += i
			#		i = len(abc)
		print("Calculated Checksum:", sum)
		return(sum)
