from LEMON import *

class LoginForm(Form):
	def init(self):
		self.title = "Main"
		self.fields = [
			TextBar("LOGIN", self.width, x = 0, y = 0),
			Text(TextMultiLine("""
               ...
             ;::::;
           ;::::; :;
         ;:::::'   :;
        ;:::::;     ;.
       ,:::::'       ;           OOO
       ::::::;       ;          OOOOO
       ;:::::;       ;         OOOOOOOO
      ,;::::::;     ;'         / OOOOOOO
    ;:::::::::`. ,,,;.        /  / DOOOOOO
  .';:::::::::::::::::;,     /  /     DOOOO
 ,::::::;::::::;;;;::::;,   /  /        DOOO
;`::::::`'::::::;;;::::: ,#/  /          DOOO
:`:::::::`;::::::;;::: ;::#  /            DOOO
::`:::::::`;:::::::: ;::::# /              DOO
`:`:::::::`;:::::: ;::::::#/               DOO
 :::`:::::::`;; ;:::::::::##                OO
 ::::`:::::::`;::::::::;:::#                OO
 `:::::`::::::::::::;'`:;::#                O
  `:::::`::::::::;' /  / `:#
   ::::::`:::::;'  /  /   `#
			""", color=Colors.RED), x = 0, y = 32),
			Text("Enter LOGON parameters below:", x = 5, y = 4),
			TextField(    TextColor("UserID   ===> ", Colors.TEAL), name = "username", x = 7, y = 4, field_length = 15),
			#TextField(    TextColor("UserID   ===> ", Colors.TEAL), x = 8, y = 4, field_length = 15),
			PasswordField(TextColor("Password ===> ", Colors.TEAL), name = "password", x = 9, y = 4, field_length = 15),
			Text("", name = "error", x = 11, y = 6),
			Text(TextColor("Unauthorized access is prohibited", Colors.PURPLE), x = 30, y = 4),
		]
		self.session.remove()

	def on_submit(self):
		self.persist_field_values()
		
		if self["username"].value == "":
			return
		if self["password"].value == "":
			return

		is_valid_login = users.check_password(
			self["username"].value,
			self["password"].value,
		)

		if is_valid_login:
			# self.session.create() <== this happens automatically if needed
			self.session["is_logged_in"] = True
			self.session["username"] = self["username"].value
			return "/"
		else:
			self["password"].value = ""
			self["error"].text = TextColor("wrong credentials", Colors.RED)