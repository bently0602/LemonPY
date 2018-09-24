from LEMON import *

class ErrorForm(Form):
	def init(self):
		self.title = "Error"
		self.fields = [
			Text("An Error Occurred", x = 0, y = 35),	
		]