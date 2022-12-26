from transmitter import Transmitter
import sys
import time

abc = {"A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", "M":"--", "N":"-.", "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T": "-", "U":"..-", "V":"...-", "W":".--", "X":"-..-", "Y":"-.--", "Z":"--..", "1":".----", "2":"..---", "3":"...--", "4":"....-", "5":".....", "6":"-....", "7":"--...", "8":"---..", "9":"----.", "0":"-----", "/":"-..-."}
morse = {".-":"A", "-...":"B", "-.-.":"C", "-..":"D", ".":"E", "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J", "-.-":"K", ".-..":"L", "--":"M", "-.":"N", "---":"O", ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T", "..-":"U", "...-":"V", ".--":"W", "-..-":"X", "-.--":"Y", "--..":"Z", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0", "-..-.":"/"}
def encrypt(msg):
	enc = ""
	for c in msg:
		try:
			int(c)
			enc += abc[str(c)] + " "
		except:
			if c == " ":
				enc += "/ "
			else:
				enc += abc[c.upper()] + " "
	return(enc)

	
if __name__ == "__main__":
	mitter = Transmitter(17, 18, "led")
	if len(sys.argv) < 2:
		print("usage: sender.py message")
		exit(-1)
	morse = encrypt(sys.argv[1])
	start = time.time()
	mitter.send(morse)
	end = time.time()
	print("message sent in {} seconds({}min)!".format(round(end-start), round((end-start)/60, 1)))
