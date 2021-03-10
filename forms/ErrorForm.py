from LEMON import *

class ErrorForm(Form):
	def init(self):
		self.title = "Error"
		self.fields = [
			Text("An Error Occurred", 
				x = 1, 
				y = 1
			),
			Text(str(self.error),
				x = 2,
				y = 2
			)
		]