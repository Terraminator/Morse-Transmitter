import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(22,gpio.IN)

ontimer = 0
offtimer = 0
sequence = []
last20 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
# Wait until a sound is recieved
while gpio.input(22) ==0:
	continue

print("Received sound, starting to listen")
# Listen to inputs

while offtimer < 20000:
		# Make sensor ignore tiny signals
	last20.append(gpio.input(22))
	last20.pop(0)
	if gpio.input(22) == 1 or last20.count(1) >0:	
		if offtimer !=0 :
			sequence.append(offtimer)
		offtimer = 0
		ontimer += 1
		
	else:
		if ontimer != 0:
			sequence.append(ontimer)
		ontimer = 0
		offtimer +=1
	time.sleep(0.0005)
	
print("Receiving no input")


print("Received input:")
print(sequence)
# Remove most of the false inputs
sequence = [e for e in sequence if e >19]

print("Cleaned input:")
print(sequence)

# Get approximate length of dit
speed = int((sequence[0]/3 + sequence[1]+ sequence[2] + sequence[3] + sequence[4]/3 + sequence[5]+sequence[6]+sequence[7]+sequence[8]/3+sequence[9]/3)/10)

# Remove more short inputs
sequence = [e for e in sequence if e > speed / 10]

# Adjust the inputs to speed
for i in range(2,len(sequence)):
	if sequence[i] < speed * 1.7 :
		sequence[i] = speed
	elif sequence[i] >= speed * 1.7 and sequence[i] < speed * 5:
		sequence[i] = speed * 3
	elif sequence[i] >= sequence[0] * 5:
		sequence[i] = speed * 7
		
# Input lengths are converted into a usable string
enc = ""

for x in range(10,len(sequence)):
	if x % 2 == 0:
		if sequence[x] == speed:
			enc += "."
		elif sequence[x] == speed * 3 or sequence[x] == speed * 7:
			enc += "-"
	
	elif x % 2 == 1:
		if sequence[x] == speed * 3:
			enc += "/"
		elif sequence[x] > speed *3:
			enc += "|"
print("Translation: \n" + enc)


# Translation begins here
decoded = ""
letter = ""
translations = {"---...":":","-.-.-.":";","-....-":"-",".-.-":"Ä","...--..":"ß","..--":"Ü","---.":"Ö","..--..":"?","-.-.--":"!","|":" ",".-":"A", "-...":"B", "-.-.":"C","-..":"D",".":"E", "..-.":"F","--.":"G","....":"H","..":"I",".---":"J", "-.-":"K", ".-..":"L","--":"M","-.":"N","---":"O",".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T","..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z",".----":"1","..---":"2","...--":"3","....-":"4",".....":"5","-....":"6","--...":"7","---..":"8","----.":"9","-----":"0",".-.-.-":".","--..--":","}

for char in enc:
	if char != "|" and char != "/":
		letter += char
	else:
		try:
			decoded += translations[letter]
		except:
			print("WARNING! Letter " + letter + " is not identifiable!")
		letter = ""
		if char == "|":
			decoded += " "

decoded += translations[letter]
print(decoded)
