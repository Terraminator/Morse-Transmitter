from transmitter import Transmitter, SHORT, LONG, SEPERATOR, EOB
import sys
import time

mitter = Transmitter(17, 18, "led")


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage: sender.py message")
		exit(-1)
	try:
		morse = str(mitter.encrypt(sys.argv[1].replace("\n", "")))
	except Exception as e:
		print(e)
		print("Sorry special characters are not allowed!")
		mitter.cleanup()
		exit(0)

	start = time.time()
	mitter.send(morse)
	end = time.time()
	print("message sent in {} seconds({}min)!".format(round(end-start), round((end-start)/60, 1)))
	mitter.cleanup()
