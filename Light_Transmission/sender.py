from transmitter import Transmitter, SHORT, LONG, SEPERATOR, EOB
import sys
import time

abc = {"A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", "M":"--", "N":"-.", "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T": "-", "U":"..-", "V":"...-", "W":".--", "X":"-..-", "Y":"-.--", "Z":"--..", "1":".----", "2":"..---", "3":"...--", "4":"....-", "5":".....", "6":"-....", "7":"--...", "8":"---..", "9":"----.", "0":"-----", "/":"-..-."}
morse = {".-":"A", "-...":"B", "-.-.":"C", "-..":"D", ".":"E", "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J", "-.-":"K", ".-..":"L", "--":"M", "-.":"N", "---":"O", ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T", "..-":"U", "...-":"V", ".--":"W", "-..-":"X", "-.--":"Y", "--..":"Z", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0", "-..-.":"/"}
mitter = Transmitter(17, 18, "led")

#def encrypt(msg: str):
#	msg = msg.replace("ö", "oe").replace("ä", "ae").replace("ß", "sz").replace("ü", "ue")
#	enc = ""
#	for c in msg:
#		try:
#			int(c)
#			enc += abc[str(c)] + " "
#		except:
#			if c == " ":
#				enc += "/ "
#			else:
#				enc += abc[c.upper()] + " "
#	return(enc)

def estimate_time(morse: str, m=""):
	et=0
	if m == "":
		morse += SEPERATOR + mitter.encrypt(str(mitter.checksum(mitter.decrypt(morse))))
	for i in range(0, len(morse)):
		sig = morse[i]
		if i != len(morse) -1:
			if morse[i+1] == " ":
				if sig == "-":
					et += LONG*2
				elif sig == ".":
					et += (SHORT + LONG)
				elif sig == "/":
					et += estimate_time(EOB, m=1)
			else:
				if sig == "-":
					et += LONG+SHORT
				elif sig == ".":
					et += SHORT*2
				elif sig == "/":
					et += estimate_time(EOB, m=1)
	return(et)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage: sender.py message")
		exit(-1)
	try:
		morse = str(mitter.encrypt(sys.argv[1]))
	except:
		print("Sorry special characters are not allowed!")
		exit(0)
	estimated = round(estimate_time(morse), 1)
	print("estimated time: {}s".format(estimated+(len(morse.split(" "))/2)*1.5))
	start = time.time()
	mitter.send(morse)
	end = time.time()
	print("message sent in {} seconds({}min)!".format(round(end-start), round((end-start)/60, 1)))
