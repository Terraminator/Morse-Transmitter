import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(27,gpio.OUT)


def shortsound(speed):
    print("short")
    gpio.output(27,gpio.HIGH)
    time.sleep(speed)
    gpio.output(27,gpio.LOW)

def longsound(speed):
    print("long")
    gpio.output(27,gpio.HIGH)
    time.sleep(speed*3)
    gpio.output(27,gpio.LOW)

def send(enc,speed):
    for char in enc:
        if char == ".":
            shortsound(speed)
            time.sleep(speed)
        if char == "-":
            longsound(speed)
            time.sleep(speed)
        if char == "|":
            print("pause long")
            time.sleep(7*speed)
        if char == "/":
            print("pause short")
            time.sleep(3*speed)

    print("Sending complete")
    gpio.cleanup()
    time.sleep(4)
    
def convert(txt):
    print(txt)
    decoded = {"!":"-.-.--/"," ": "|","A":".-/", "B":"-.../", "C":"-.-./","D":"-../","E":"./", "F":"..-./","G":"--./","H":"..../","I":"../","J":".---/", "K":"-.-/", "L":".-../","M":"--/","N":"-./","O":"---/","P":".--./","Q":"--.-/","R":".-./","S":".../","T":"-/","U":"..-/","V":"...-/","W":".--/","X":"-..-/","Y":"-.--/","Z":"--../","1":".----/","2":"..---/","3":"...--/","4":"....-/","5":"...../","6":"-..../","7":"--.../","8":"---../","9":"----./","0":"-----/",".":".-.-.-/",",":"--..--/"}
    enc = ""
    for char in txt:
        enc += decoded[char]
    enc = "|-.-.-/" + enc
    print(enc)
    speed = input("Enter length of a Dit (short signal): ")
    try:
        speed = float(speed)
        if speed <= 0:
            print("Invalid input, using 0.3 instead.")
            speed = 0.3
    except:
        print("Invalid input, using 0.3 instead")
        speed = 0.3
    send(enc,speed)
    
msg = input("Enter message to encode here: ")
msg = msg.upper()
convert(msg)
