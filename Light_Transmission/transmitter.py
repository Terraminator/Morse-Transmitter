from gpiozero import PWMLED
from time import time, sleep
from gpiozero import LightSensor
import threading
from queue import Queue

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] #abc enum for checksum
morse = {".-":"A", "-...":"B", "-.-.":"C", "-..":"D", ".":"E", "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J", "-.-":"K", ".-..":"L", "--":"M", "-.":"N", "---":"O", ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T", "..-":"U", "...-":"V", ".--":"W", "-..-":"X", "-.--":"Y", "--..":"Z", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0", "-..-.":"/"}

LONG = 1 # long delay -> -
SHORT = 0.5 # short delay -> .
EOB = "-..-." # /
SEPERATOR = "-..-.." # #

def timedelta(q):
	start = time.time()
	while q.get() != "stop": pass
	q.put(time.time()-start)

class Transmitter:

	def __init__(self, pin1=17, pin2=18):
		self.led = PWMLED(pin1) #setting up led pin
		self.ldr = LightSensor(pin2) # setting up lightsensor pin
		self.pin1 = int(pin1) # LED
		self.pin2 = int(pin2) # LightSensor
		self.led.value = 0
		
	def __blink(self, delay): # declaring private method
		delay = float(delay) # important - 0.5 --> 0
		self.led.value = 0 # turn led off 
		self.led.value = 1 # turn led on
		sleep(delay)
		self.led.value = 0
		
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
		
	
	def __send(self, sig): # declaring private send method
			sig = str(sig)
			if sig == ".":
				self.__blink(SHORT)
			elif sig == "-":
				self.__blink(LONG)
			elif sig == "/":
				for sig in EOB: # could hang program - sorry
					self.__send(sig)
				
	def send(self, morse):
		morse = str(morse)
		for i in range(0,2): # sending msg two times
			for sig in morse:
				self.__send(sig) 
			for sig in SEPERATOR:
				self.__send(sig)
			checksum = str(self.checksum(self.decrypt(morse)))
			for sig in checksum:
				self.__send(sig)
			sleep(1)
		return(0)
		
	def __recv(self):
			while not SEPERATOR in msg: # receiving until message  block (packet) ends
				q = Queue()
				clock = threading.Thread(target=timedelta, args=(q,))
				while self.ldr.value < 0.5: pass		#0=dark, 1=light
				clock.start()
				while self.ldr.value > 0.5: pass
				q.put("stop")
				q.join()
				if q.get() in range(0.3, 0.7): #time in seconds
					msg += "."
				elif q.get() in range(0.8, 1.3):
					msg += "-"
				else:
					pass
			msg = msg.replace(EOB, "/").replace(SEPERATOR, "") # removing seperators from message
			return(msg)
		
	def recv(self):
			# receiving msg
			for i in range(0, 2): # receiving 2 times to avoid packet loss - but it is still possible
				msg = __recv()
				checksum = __recv()
				if self.checksum(self.decrypt(msg)) == check: return(msg) # if checksum matches return message
			return(-1) # if checksum doesnt match return an error
	
	def checksum(self, msg):
		msg = str(msg.upper()) # making message uppercase (not every char is in abc - yet)
		sum = 0
		for c in msg:
			for i in range(0, len(abc)):
				if c == abc[i]:
					sum += i
					i = len(abc)
		return(sum)