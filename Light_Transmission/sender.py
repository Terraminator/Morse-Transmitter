from transmitter import Transmitter
import sys

abc = {"A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", "M":"--", "N":"-.", "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T": "-", "U":"..-", "V":"...-", "W":".--", "X":"-..-", "Y":"-.--", "Z":"--..", "1":".----", "2":"..---", "3":"...--", "4":"....-", "5":".....", "6":"-....", "7":"--...", "8":"---..", "9":"----.", "0":"-----"}
morse = {".-":"A", "-...":"B", "-.-.":"C", "-..":"D", ".":"E", "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J", "-.-":"K", ".-..":"L", "--":"M", "-.":"N", "---":"O", ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T", "..-":"U", "...-":"V", ".--":"W", "-..-":"X", "-.--":"Y", "--..":"Z", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0"}

def encrypt(msg):
	enc = ""
	for c in msg:
		try:
			int(c)
			enc += abc[str(c)] + " "
		except:
			if c == " ":
				enc += "/"
			else:
				enc += abc[c.upper()] + " "
	return(enc)

def decrypt(msg):
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
	dec += morse[tmp]
	return(dec)
	
if __name__ == "__main__":
	mitter = Transmitter(17)
	if sys.argc < 2:
		print("usage: sender.py message")
		exit(-1)
	morse = encrypt(sys.argv[1])
	mitter.send(morse)
	print("message sent")