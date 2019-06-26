import tornado.ioloop
import tornado.web
import signal
import LEMON

LEMON.USERS.assert_default_admin_user()

if __name__ == '__main__':
	form_server = LEMON.TornadoServer(
		[
			(r".*", LEMON.FormsServerHandler, {"forms_path": "forms"}),
		], 
		cookie_secret="__this_is_A_secret__I_tInk__",
		port = 8090
	)
	signal.signal(signal.SIGINT, form_server.signal_handler)
	form_server.start()
	print("Server @ " + str(form_server.port) + ". Ctrl_Break(Clear)/Ctrl_C to exit!")
	tornado.ioloop.PeriodicCallback(form_server.try_exit, 1000).start()
	form_server.block()