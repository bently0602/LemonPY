from LEMON import *

class IndexForm(Form):
	def init(self):
		if self.session["is_logged_in"] is None:
			return "Login"

		self.title = "Menu"
		self.fields = [
			Text("Main Menu", x = 0, y = 35),
			TextField(TextColor("Option ===> ", Colors.GREEN), name = "menu_option", x = 1, y = 0, field_length=(80)),
			Text("0 " + str(TextColor("Exit to Login Screen", Colors.GREEN)), x = 3, y = 0),
			Text(
				str(TextColor("Logged In: ", Colors.GREEN)) +
				str(TextColor(self.session["is_logged_in"], Colors.TEAL)), 
				x = 3, y = 60),
			Text(
				str(TextColor("Username : ", Colors.GREEN)) +
				str(TextColor(self.session["username"], Colors.TEAL)), 
				x = 4, y = 60),
			Text(
				str(TextColor("Cache    : ", Colors.GREEN)) +
				str(TextColor("", Colors.TEAL)), 
				x = 5, y = 60),

			Text(TextColor("PF 9=EXIT", Colors.PURPLE), x = 30, y = 0),			
		]

	def on_submit(self):
		self.persist_field_values()
		if self.get_submit_type() == SubmitTypes.F9:
			return "Login"
		if self["menu_option"].value == "0":
			return "Login"			
