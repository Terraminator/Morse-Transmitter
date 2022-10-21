import time
import winsound


# Will add raspberry support later
def shortsound(speed):
    print("short")
    str(speed)
    winsound.Beep(1000, 20*speed)

def longsound(speed):
    print("long")
    str(speed)
    winsound.Beep(1000, 60*speed)

def send(enc,speed):
    for char in enc:
        if char == ".":
            shortsound(speed)
            time.sleep(0.02 * speed)
            
        if char == "-":
            longsound(speed)
            time.sleep(0.06 * speed)

        if char == "│":
            print("pause long")
            time.sleep(0.14 * speed)

        if char == "/":
            print("pause short")
            time.sleep(0.06 * speed)
        time.sleep(0.02 * speed)
    print("Sending complete")   
    time.sleep(4)

def convert(txt):
    decoded = {" ":"│","A":".-/", "B":"-.../", "C":"-.-./", "D":"-../", "E":"./", "F":"..-./", "G":"--./", "H":"..../", "I":"../", "J":".---/", "K":"-.-/", "L":".-../", "M":"--/", "N":"-./", "O":"---/", "P":".--./", "Q":"--.-/", "R":".-./", "S":".../", "T": "-/", "U":"..-/", "V":"...-/", "W":".--/", "X":"-..-/", "Y":"-.--/", "Z":"--../", "1":".----/", "2":"..---/", "3":"...--/", "4":"....-/", "5":"...../", "6":"-..../", "7":"--.../", "8":"---../", "9":"----./", "0":"-----/","a":".-/", "b":"-.../", "c":"-.-./", "d":"-../", "e":"./", "f":"..-./", "g":"--./", "h":"..../", "i":"../", "j":".---/", "k":"-.-/", "l":".-../", "m":"--/", "n":"-./", "o":"---/", "p":".--./", "q":"--.-/", "r":".-./", "s":".../", "t": "-/", "u":"..-/", "v":"...-/", "w":".--/", "x":"-..-/", "y":"-.--/", "z":"--../", ".":".-.-.- ", ",":"--..--/"}
    enc = ""
    for char in txt:
        enc += decoded[char]
        print(enc)
    speed = input("Enter signal length (Must be higher than 5) ")
    try:
        speed = int(speed)
        if speed < 5:
            print("Invalid input, using 5 instead")
            speed = 5
    except:
        print("Invalid input, using 5 instead")
        speed = 5
    send(enc,speed)



msg = input("Enter Message to encode here:")
convert(msg)
        
