# dummy test class for debugging


class PWMLED:

	def __init__(self, pin):
		self.pin = pin
		print("**DEBUG** PWMLED - pin: " + str(pin))
		self.value = 0
		print("**DEBUG** PWMLED - value=0")

class LightSensor:
	def __init__(self, pin):
		self.pin = pin
		print("**DEBUG** LightSensor - pin: " + str(pin))
		self.value = 0.6
		print("**DEBUG** LightSensor - value=0.6")