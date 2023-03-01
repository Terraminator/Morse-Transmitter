#from gpiozero import LED, LightSensor
import RPi.GPIO as gpio
import time
import numpy as np

abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] #abc enum for checksum
morse = {".-":"A", "-...":"B", "-.-.":"C", "-..":"D", ".":"E", "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J", "-.-":"K", ".-..":"L", "--":"M", "-.":"N", "---":"O", ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T", "..-":"U", "...-":"V", ".--":"W", "-..-":"X", "-.--":"Y", "--..":"Z", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0", "--..--":",", "-.-.--":"!", "-.--.":"(", "-.--.-":")", "..--..":"?", ".-.-.":"+", "":"", ".-.-.-":".", "-.-.-.":";"}
rev_m  = {"A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", "M":"--", "N":"-.", "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T": "-", "U":"..-", "V":"...-", "W":".--", "X":"-..-", "Y":"-.--", "Z":"--..", "1":".----", "2":"..---", "3":"...--", "4":"....-", "5":".....", "6":"-....", "7":"--...", "8":"---..", "9":"----.", "0":"-----", "#":"-..-..", ",":"--..--", "!":"-.-.--", "(":"-.--.", ")":"-.--.-", "?":"..--..", "+":".-.-.", "":"", ".":".-.-.-",";":"-.-.-."}

LONG = 0.02 # long delay -> -
SHORT=0.01 # short delay -> .
scale = 1
EOB = "-..-. " # /
SEPERATOR = "-..--.-- " # #
delay_sleep = 0.001

# bring wordlist to right format
with open("3000_de.txt", "r") as wordlist:
	words = list(map(lambda x: x.upper().strip("\n").replace("Ö", "OE").replace("Ä", "AE").replace("ß", "SZ").replace("Ü", "UE"), wordlist.readlines()))


#https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])

class Transmitter:

	def __init__(self, pin1=17, pin2=18, mode="led"):
		self.rlong = 0
		self.rshort = 0
		self.timeout = 0
		self.cc = 0
		gpio.setmode(gpio.BCM)
		if mode == "led":
			gpio.setup(pin1, gpio.OUT)
			#self.led = LED(pin1) #setting up led pin
			#self.led.value = 0
			gpio.output(pin1, gpio.LOW)
		elif mode == "ldr":
			gpio.setup(pin2, gpio.IN)
			#self.ldr = LightSensor(pin2) # setting up lightsensor pin
		self.pin1 = int(pin1) # LED
		self.pin2 = int(pin2) # LightSensor
		
	def __blink(self, delay, OFF_DELAY=SHORT): # declaring private method
		delay = float(delay) 
		#self.led.value = 0 # turn led off 
		#gpio.output(self.pin1, gpio.LOW)
		gpio.output(self.pin1, gpio.HIGH)
		time.sleep(delay)
		gpio.output(self.pin1, gpio.LOW)
		time.sleep(OFF_DELAY)
		self.cc+=2

	def __get_candidates(self, u, words):
			candidates= {}
			for x in words:
				if levenshtein(u, x) <= 3 :
					candidates.update({x.strip("\n"):levenshtein(u, x)})
			return(candidates)

	def __get_unknown(self, msg, words):
		unknown = []
		for w in msg.upper().split():
			if w not in words:
				try:
					int(w.strip("?!().,-/"))
				except:
					unknown.append(w.strip("?!().,-/"))
		return(unknown)

	def __check(self, guess, check):
		if int(self.checksum(guess)) == int(check):
			return(True)
		else:
			return(False)
	

	def defrag(self, msg:str, check:int):
		unknown = self.__get_unknown(msg, words)
		cs = []
		possibilities = []
		print("unknown words:" + str(unknown))
		for u in unknown:
			candidates = self.__get_candidates(u, words)
			#print(candidates)
			cs.append([a for a, b in sorted(candidates.items(), key=lambda x:x[1])])
		print("defragmenting...")

		for x in range(0, len(cs)):
			for ca in cs[x]:
				guess = msg.replace(unknown[x], ca.strip()).strip()
				if self.__check(guess, check) and not any(u in guess for u in unknown) and levenshtein(guess, msg)<=3:
					possibilities.append({guess:levenshtein(guess, msg)})
				
				for z in range(0, len([ö for ö in cs if ö != cs[x]])):
					cb = [ö for ö in cs if ö != cs[x]][z]
					for cc in cb:
						guess = msg.replace(unknown[x], ca.strip()).replace(unknown[z], cc.strip()).strip()
						if self.__check(guess, check) and not any(u in guess for u in unknown) and levenshtein(guess, msg)<=3:
							possibilities.append({guess:levenshtein(guess, msg)})
		if len(possibilities)==0:
			return(-1)
		else:
			print(possibilities)
			return(str([c for c in possibilities[0]]).strip(""""[']"""))

	def decrypt(self, msg):
		dec = ""
		tmp = ""
		for c in msg:
			if c == "/":
				dec += " "
			elif c == "#":
				dec += "#"
			elif c == " ":
				dec += morse[tmp]
				tmp = ""
			else:
				tmp += c
		if tmp != "": dec += morse[tmp]
		return(dec)
		
	def encrypt(self, msg):
		msg = msg.upper().strip("\n").replace("Ö", "OE").replace("Ä", "AE").replace("ß", "SZ").replace("Ü", "UE")
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
				OFF_DELAY = LONG#0.9
			else:
				OFF_DELAY = SHORT#0.3
			if sig == ".":
				self.__blink(SHORT, OFF_DELAY)
			elif sig == "-":
				self.__blink(LONG, OFF_DELAY)
			elif sig == "/":
				for sig in EOB: # send end of block
					self.__send(sig)
			else:
				time.sleep(OFF_DELAY)

	def send(self, morse, m=""):
		if m == "":
			morse += SEPERATOR
		morse = str(morse)
		print('\n"' + morse + '"')
		print("live: ", end="", flush=True)
		for i in range(0, len(morse)):
			sig = morse[i]
			print(sig, end="", flush=True)
			if i != len(morse) -1:
				if morse[i+1] == " ":
					self.__send(sig, "space")
				else:
					self.__send(sig) 
		if m == "":
			checksum = str(self.checksum(self.decrypt(morse.replace(SEPERATOR, ""))))
			print("\n\nchecksum: " + checksum)
			print("encrypted: " + str(self.encrypt(checksum)) + "\n")
			print("sending checksum!")
			self.send(self.encrypt(str(checksum)), m="check")
			print("\nsent {} signals!".format(self.cc))
		return(0)
		
	def __round_brightness(self, value):
		if value <= 0.3:
			return(0) # bright
		else:
			return(1) #dark

	def __sigs_to_morse(self, sigs):
		morse = ""
		count_long = np.arange((LONG/delay_sleep*scale)-8, 500, 1)
		count_short = np.arange(1, (SHORT/delay_sleep*scale)+8, 1)
		count_space = np.arange((LONG/delay_sleep*scale)-8, 500.0)
		for sig in sigs:
			if sig.count("-") in count_space:
				morse += " "
			if sig.count("+") in count_long:
				morse += "-"
			elif sig.count("+") in count_short:
				morse += "."
		return(morse.replace(SEPERATOR, "#").replace(EOB, "/")) # removing seperators from message

	def __recv(self):
			status = 0
			stop = False
			#self.__sync()
			junk = ""
			raw = ""
			ls = 0
			while gpio.input(self.pin2) > 0.3: pass
			print("Beginning to listen...")
			while not stop:
				status = str(self.__round_brightness(gpio.input(self.pin2)))
				junk += status 
				if ls != status: 
					raw+=round(len(junk)*scale)*str(ls)
					junk = status
				ls = status
				if len(junk)>LONG/delay_sleep*8:
					stop = True
				
				time.sleep(delay_sleep)
			del junk
			print("\nevaluating data...")
			raw = raw.replace("0", "+").replace( "1", "-").replace("+-", ";").replace("-+",";")
			sigs=raw.split(";")
			print("got", len(sigs), "sigs!")

			print("sigs:", sigs)
			print("morse:", self.__sigs_to_morse(sigs))
			morse_full = str(self.decrypt(self.__sigs_to_morse(sigs)))
			print("________________________________________________")
			print("morse_full: ", morse_full)
			print("________________________________________________")
			if len(morse_full.split("#"))<2:
				print("message corrupted!")
				return(-1)
			mf = morse_full.split("#")
			print(mf)
			msg = mf[0]
			checksum = mf[1]
			print("________________________________")
			print("checksum: " + str(checksum))
			print("msg: " + str(msg))
			return(msg, checksum)
		
	def recv(self):
		try:
			msg, check = self.__recv()
		except Exception as e:
			print(e)
			msg= "ERROR"
			check=0
		try:
			if int(self.checksum(msg)) == int(check):
				return(msg) # if checksum matches return message
			elif check != 0:
				print("\nfragmented msg: " + str(msg))
				msg = self.defrag(msg, check)
				if msg == -1:
					print("Couldnt defrag message!")
				else:
					print("defragemented msg: " + str(msg))
					return(msg)
				return(-1) # if checksum doesnt match return an error
			else:
				return(-1)
		except Exception as e:
			print(e)
			print("checksum corrupted!")
			print("fragmented msg: " + str(msg))
			return(-1)
	
	def checksum(self, msg):
		sum = 0
		for c in msg:
			sum += ord(str(c))
		return(sum)

	def cleanup(self):
		gpio.cleanup()
		pass
