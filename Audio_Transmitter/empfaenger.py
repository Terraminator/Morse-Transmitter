import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(22,gpio.IN)

ontimer = 0
offtimer = 0
sequence = []

# Wait until a sound is recieved
while True:
	if gpio.input(22) == 0:
		break

# Listen to inputs

while True:
	if gpio.input(22) == 0:
		if offtimer !=0 and len(sequence) !=0:
			sequence.append(offtimer)
		offtimer = 0
		ontimer += 1
		print(sequence)
		
	else:
		if ontimer != 0:
			sequence.append(ontimer)
		ontimer = 0
		offtimer +=1
		print(sequence)
		# Stop listening
		if offtimer > sequence[0] * 25:
			print("Recieving no input")
			break
	time.sleep(0.0001)

print(len(sequence))


# Get approximate length of dit
speed = (sequence[0] + sequence[1] / 3) / 2

# Adjust the inputs to speed

for i in range(2,len(sequence)):
	if sequence[i] < speed * 1.4:
		sequence[i] = speed
	elif sequence[i] >= speed * 1.4 and sequence[i] < speed * 5:
		sequence[i] = speed * 3
	elif sequence[i] >= sequence[0] * 5:
		sequence[i] = speed * 7
		
		
print(sequence)

# Input lengths are converted into a usable string
enc = ""

for x in range(2, len(sequence)):
	if x % 2 == 0:
		if sequence[x] == speed:
			enc += "."
			print(enc)
		elif sequence[x] == speed * 3 or sequence[x] == speed * 7:
			enc += "-"
	
	elif x % 2 == 1:
		if sequence[x] == speed * 3:
			enc += "/"
		elif sequence[x] == speed * 7:
			enc += "|"

# Translation begins here
decoded = ""
letter = ""
translations = {"-.-.--":"!","|":" ",".-":"A", "-...":"B", "-.-.":"C","-..":"D",".":"E", "..-.":"F","--.":"G","....":"H","..":"I",".---":"J", "-.-":"K", ".-..":"L","--":"M","-.":"N","---":"O",".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T","..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z",".----":"1","..---":"2","...--":"3","....-":"4",".....":"5","-....":"6","--...":"7","---..":"8","----.":"9","-----":"0",".-.-.-":".","--..--":","}

for char in enc:
	if char != "|" and char != "/":
		letter += char
	else:
		decoded += translations[letter]
		letter = ""
		if char == "|":
			decoded += " "

decoded += translations[letter]
print(decoded)
