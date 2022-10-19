from gpiozero import PWMLED
from time import time, sleep
from gpiozero import LightSensor
import threading
from queue import Queue

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
LONG = 1
SHORT = 0.5
EOB = ".-..-."
SEPERATOR = "-..-."

def timedelta(q):
	start = time.time()
	while q.get() != "stop": pass
	q.put(time.time()-start)

class Transmitter:

	def __init__(self, pin1=17, pin2=18):
		self.led = PWMLED(pin1)
		self.ldr = LightSensor(pin2)
		self.pin1 = pin1
		self.pin2 = pin2
		self.led.value = 0
		
	def blink(self, delay):
		self.led.value = 0
		self.led.value = 1
		sleep(delay)
		self.led.value = 0
		
	
	def eval_sig(self, sig):
			if sig == ".":
				self.blink(SHORT)
			elif sig == "-":
				self.blink(LONG)
				
	def send(self, morse):
		for sig in morse:
			self.eval_sig(sig) # / needs to be interpreted and end of one char needs to be clear
		for sig in SEPERATOR:
			self.eval_sig(sig)
		checksum = str(self.checksum(msg))
		for sig in checksum:
			self.eval_sig(sig)
		return(0)
		
	def recv(self):

		while not SEPERATOR in msg:
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
		return(0)
	
	def checksum(self, msg):
		msg = msg.upper()
		sum = 0
		for c in msg:
			for i in range(0, len(abc)):
				if c == abc[i]:
					sum += i
					i = len(abc)
		return(sum)