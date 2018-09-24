import LEMON

LEMON.USERS.assert_default_admin_user()

if __name__ == '__main__':
	form_server = LEMON.TornadoServer([
		(r".*", LEMON.FormsServerHandler, {"forms_path": "forms"}),
	], 
	cookie_secret="__this_is_A_secret__I_tInk__",
	port = 8090)
	print("Server @ " + str(form_server.port) + ". Ctrl_Break(Clear) to exit!")
	form_server.start()
