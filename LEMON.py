#!/usr/bin/env python3
import uuid
import string
import secrets
import sys
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
import tornado.process
from tornado import template
import sqlite3
import math
from passlib.hash import pbkdf2_sha256
import signal
import os
from pyngrok import ngrok
from pathlib import Path

FORM_TEMPLATE_STR = ""
FORM_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "LEMON.html")
with open(FORM_TEMPLATE_PATH, 'r') as file:
	FORM_TEMPLATE_STR = file.read()
FORM_TEMPLATE = template.Template(FORM_TEMPLATE_STR)

class Colors():
	RED = "#FF0000"
	TEAL = "#BCFEFD"
	GREEN = "#40F85A"
	PURPLE = "#7992F9"
	NORMAL = "#FEFEFE"
	YELLOW = "#FFFF00"
	BLUE = "#0000FD"

class SubmitTypes():
	F9 = "f9"
	F8 = "f8"
	F3 = "f3"
	NORMAL = None

class TextMultiLine():
	def __init__(self, text, color = "initial"):
		self.text = text.replace(" ", "&nbsp;").replace("\n", "<br />").strip()
		self.color = color

	def __str__(self):
		return "<p style=\"color: " + str(self.color) + ";\">" + str(self.text) + "</p>"

class TextColor():
	def __init__(self, text, color = "initial"):
		self.text = text.replace(" ", "&nbsp;")
		self.color = color

	def __str__(self):
		return "<span style=\"color: " + str(self.color) + ";\">" + str(self.text) + "</span>"

class TextBold():
	def __init__(self, text):
		self.text = text.replace(" ", "&nbsp;")

	def __str__(self):
		return "<b>" + str(self.text) + "</b>"

class Component():
	def __init__(self, name = None, x = 0, y = 0):
		self.x = x
		self.y = y
		self.name = name
		if name is None:
			self.name = "gen_" + str(uuid.uuid4())

	def compose(self, inner):
		return "<div class=\"unit\" style=\"" + "top:" + str(self.x) + "rem;left:" + str(self.y) + "ch;\">" + \
		inner + \
		"</div>"		
		# "<div class=\"spacer\">" + \

	def html(self):
		return self.compose("&nbsp;")

class TextBar(Component):
	def __init__(self, text, width, name = None, x = 0, y = 0):
		Component.__init__(self, name = name, x = x, y = y)
		self.text = text
		self.width = width

	def html(self):
		left_off = math.floor(len(self.text) / 2) + 1
		right_off = math.ceil(len(self.text) / 2) + 1

		padding_size = int(round((self.width / 2)))
		padding_rem = int(round(self.width % 2))

		contents = "|" + ("-" * (padding_size - left_off))
		contents = contents + self.text
		contents = contents + ("-" * ((padding_size + padding_rem) - right_off)) + "|"
		return self.compose(contents)

class Text(Component):
	def __init__(self, text, name = None, x = 0, y = 0):
		Component.__init__(self, name = name, x = x, y = y)
		self._text = str(text)

	def get_text(self):
		return str(self._text)

	def set_text(self, val):
		self._text = str(val)

	text = property(get_text, set_text)

	def html(self):
		return self.compose("<span>" + self._text + "</span>")

class TextField(Component):
	def __init__(self, label, color=None, value="", field_length=10, placeholder="", is_password=False, name = None, x = 0, y = 0):
		Component.__init__(self, name = name, x = x, y = y)
		if label is None:
			self.label = "&nbsp;"
		else:
			self.label = str(label)
		self.field_length = field_length
		self.placeholder = placeholder
		self._value = str(value)
		if color is None:
			self.color = Colors().NORMAL
		else:
			self.color = color
		if is_password == False:
			self.type = "text"
		else:
			self.type = "password"

	def clear(self):
		self._value = ""
	
	def get_value(self):
		if self._value is None:
			return ""
		else:
			return self._value.strip()

	def set_value(self, val):
		self._value = str(val).strip()

	value = property(get_value, set_value)

	def html(self):
		# <span class=\"input-underline\" style=\"width:" + str(self.field_length) + "ch;background:" + str(self.color) + ";\"></span>"
		return self.compose(
		"<label for=\"" + self.name + "\">" + self.label + "</label>" \
		"<input style=\"color:" + str(self.color) + ";\" placeholder=\"" + self.placeholder + "\" size=\"" + str(self.field_length) + "\" name=\"" + self.name + "\" " \
		"type=\"" + self.type + "\" value=\"" + self._value + "\" maxlength=\"" + str(self.field_length) + "\" autocomplete=\"off\"></input>"
		)

class PasswordField(TextField):
	def __init__(self, label, value="", field_length=10, placeholder="", name = None, x = 0, y = 0):
		TextField.__init__(self, label, value = value, field_length = field_length, placeholder = placeholder, is_password = True, name = name, x = x, y = y)

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
	def set_extra_headers(self, path):
		# Disable cache
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class Form():
	def __init__(self):
		self.title = ""
		self.fields = []
		self.width = 80
		self.height = 32
		self.is_scaled = True
		self.request = None
		self.session = None

	def persist_field_values(self):
		for key, value in self.request.arguments.items():
			for x in self.fields:
				if x.name.startswith("__"):
					pass
				if x.name == key:
					try:
						x.value = (value[0].decode("utf-8"))
					except:
						pass

	def clear_field_values(self):		
		for key, value in self.request.arguments.items():
			for x in self.fields:
				if x.name == key:
					try:
						x.clear()
					except:
						pass

	def __getitem__(self, key):
		for x in self.fields:
			if x.name == key:
				try:
					return x
				except:
					pass
		return None

	def get_field_value(self, name):
		for key, value in self.request.arguments.items():
			for x in self.fields:
				if x.name == key and key == name:
					return value[0].decode("utf-8")

	def get_submit_type(self):
		for key, value in self.request.arguments.items():
			if key == "__submit_type":
				return value[0].decode("utf-8")
		return None

	# subclasses need to override this
	def on_submit(self):
		pass

class FormsServerHandler(tornado.web.RequestHandler):
	def initialize(self):
		form_name = self.request.path.split("/")[-1]
		if form_name == "":
			form_name = "Index"
		
		error = None
		try:
			form_path = os.path.join(FORMSFOLDER, form_name + "Form.py")
			exec(open(form_path).read(), globals())
		except:
			form_name = "Error"
			form_path = os.path.join(FORMSFOLDER, form_name + "Form.py")
			error = sys.exc_info()[0]
			exec(open(form_path).read(), globals())
		
		self.form = globals()[form_name + "Form"]()
		self.form.fields = []
		self.form.title = "NO TITLE"
		self.form.request = self.request
		self.form.is_scaled = True
		self.form.width = 80
		self.form.height = 32
		self.form.session = Session(self)
		self.form.error = error
		
	def prepare(self):
		# https://stackoverflow.com/questions/29794641/tornado-redirect-to-a-different-domain
		self._init_ret = self.form.init()
		if self._init_ret is not None:
			self.redirect(str(self._init_ret))		

	def get(self):
		invert_op = getattr(self.form, "setup", None)
		if callable(invert_op):
			ret = self.form.setup()
		invert_op = getattr(self.form, "on_get", None)
		if callable(invert_op):
			ret = self.form.on_get()
		self.write(FORM_TEMPLATE.generate(
			title=self.form.title, 
			is_scaled=self.form.is_scaled, 
			fields=self.form.fields,
			width=self.form.width,
			height=self.form.height))

	def post(self):
		invert_op = getattr(self.form, "setup", None)
		if callable(invert_op):
			ret = self.form.setup()		
		invert_op = getattr(self.form, "on_post", None)
		if callable(invert_op):
			ret = self.form.on_post()	
		invert_op = getattr(self.form, "on_submit", None)
		ret = None
		if callable(invert_op):
			ret = self.form.on_submit()
		if ret is None:
			self.postback()
		else:
			self.navigate_to_form(str(ret))

	def postback(self):
		self.write(FORM_TEMPLATE.generate(
			title=self.form.title, 
			is_scaled=self.form.is_scaled, 
			fields=self.form.fields,
			width=self.form.width,
			height=self.form.height))

	def navigate_to_form(self, name):
		self.redirect(name)

class SessionCacheKeyValue():
	def __init__(self, session_id):
		self.session_id = session_id
		self.SESSIONCONNECTION = os.path.join(DATAFOLDER, "session.db")

	def __getitem__(self, key):
		conn = sqlite3.connect(self.SESSIONCONNECTION)
		c = conn.cursor()
		c.execute('SELECT value FROM kv WHERE sessionid = ? and key = ?', (self.session_id, key,))
		item = c.fetchone()
		conn.close()
		if item is None:
			return None
		return item[0]

	def __setitem__(self, key, value):
		conn = sqlite3.connect(self.SESSIONCONNECTION)
		c = conn.cursor()
		c.execute('REPLACE INTO kv (sessionid, key, value) VALUES (?,?,?)', (self.session_id, key, value))
		conn.commit()
		conn.close()

class SessionCache():
	def __init__(self):
		self.SESSIONCONNECTION = os.path.join(DATAFOLDER, "session.db")
		conn = sqlite3.connect(self.SESSIONCONNECTION)
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS kv (sessionid text, key text, value text, UNIQUE(sessionid, key))")
		conn.commit()
		conn.close()

	def __getitem__(self, session_id):
		return SessionCacheKeyValue(session_id)

	def __delitem__(self, session_id):
		if key not in self:
			raise KeyError(key)
		conn = sqlite3.connect(self.SESSIONCONNECTION)
		c = self.conn.cursor()
		c.execute('DELETE FROM kv WHERE sessionid = ?', (session_id,))
		conn.commit()
		conn.close()

class Session():
	def __init__(self, handler):
		self.handler = handler
		self.session_id = None
		self.session_cache = SessionCache()
		self.session_cookie_name = "FromServerSession"

	def _get_session_id(self):
		if self.session_id is None:
			cookie = self.handler.get_secure_cookie(self.session_cookie_name)
			if cookie is None:
				self.session_id = None
			else:
				self.session_id = cookie.decode("utf-8")

	def create(self):
		self.session_id = str(secrets.token_urlsafe(64))
		self.handler.set_secure_cookie(self.session_cookie_name, self.session_id)
		# no need to create if never used?
		self.session_cache[self.session_id]["_created"] = True 

	def remove(self):
		self._get_session_id()
		if self.session_id is None:
			pass
		else:
			try:
				del self.session_cache[self.session_id]
			except:
				pass
			self.handler.clear_cookie(self.session_cookie_name)

	def is_valid(self):
		id = ""
		self._get_session_id()
		if self.session_id is None:
			return False
		else:
			try:
				id = self.session_cache[self.session_id]
			except:
				return False
		return True

	def __getitem__(self, key):
		self._get_session_id()
		if self.session_id is None:
			return None
		else:
			if self.session_cache[self.session_id] is None:
				return None
			return self.session_cache[self.session_id][key]

	def __setitem__(self, key, value):
		self._get_session_id()
		if self.session_id is None:
			self.create() # will assign self.session_id a value
		self.session_cache[self.session_id][key] = value

# just as a shorthand to wrap tornado
class TornadoServer():
	def __init__(self, handlers, cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__", port=8090, autoreload=False):
		self.handlers = handlers
		self.autoreload = autoreload
		self.handlers.append((r"/static/(.*)", NoCacheStaticFileHandler, {"path": "static"}))
		self.cookie_secret = cookie_secret
		self.port = port
		self.is_closing = False
		self.app = tornado.web.Application(
			self.handlers, autoreload=self.autoreload,
			cookie_secret=self.cookie_secret)

	def start(self):
		self.app.listen(self.port)

	def block(self):
		tornado.ioloop.IOLoop.instance().start()

	def signal_handler(self, signum, frame):
		self.is_closing = True

	def try_exit(self):
		if self.is_closing:
			tornado.ioloop.IOLoop.instance().stop()

class DB():
	def __init__(self, dbname):
		self.filename = os.path.join(DATAFOLDER, dbname + ".db")
		conn = sqlite3.connect(self.filename)
		conn.commit()
		conn.close()

	def execute(self, cmd, params = None):
		conn = sqlite3.connect(self.filename)
		c = conn.cursor()
		if params is None:
			c.execute(cmd)
		else:
			c.execute(cmd, params)
		conn.commit()
		conn.close()

	def select_one(self, cmd, params = None):
		conn = sqlite3.connect(self.filename)
		c = conn.cursor()
		if params is None:
			c.execute(cmd)
		else:
			c.execute(cmd, params)
		items = c.fetchone()
		conn.commit()
		conn.close()
		return items

	def select(self, cmd, params = None):
		conn = sqlite3.connect(self.filename)
		c = conn.cursor()
		if params is None:
			c.execute(cmd)
		else:
			c.execute(cmd, params)
		items = c.fetchall()
		conn.commit()
		conn.close()
		return items

class Users():
	def __init__(self, max_attempts = 4):
		self.users_db = DB("users")
		self.max_attempts = max_attempts
		self.users_db.execute("""
			CREATE TABLE IF NOT EXISTS users (
				name text,
				hash text,
				attempts integer
			)
		""")

	def assert_default_admin_user(self, password="password"):
		user = self.users_db.select("select name from users where name = ?", ("admin",))
		hashed = pbkdf2_sha256.hash(password, rounds=200000, salt_size=16)
		if len(user) == 0:
			self.users_db.execute("insert into users (name, hash, attempts) values (?, ?, 0)", ("admin", hashed,))
		else:
			self.users_db.execute("update users set hash = ?, attempts = 0 where name = ?", (hashed, "admin"))

	def change_user_password(self, username, password):
		hashed = pbkdf2_sha256.hash(password, rounds=200000, salt_size=16)
		self.users_db.execute("update users set hash = ? where name = ?", (hashed, username,))		

	def check_password(self, username, password):
		matching_users = self.users_db.select_one(
			"select name, hash, attempts from users where name = ?", 
			(username,))
		if matching_users is None:
			return False
		else:
			if matching_users[2] > self.max_attempts:
				return False

			res = pbkdf2_sha256.verify(password, matching_users[1])
			if res == False:
				self.users_db.execute("update users set attempts = attempts + 1 where name = ?", (username,))
			else:
				self.users_db.execute("update users set attempts = 0 where name = ?", (username,))
			return res

############################################################################################################

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--assertdefaultadmin", help="assert default admin user", default="")
parser.add_argument("-p", "--port", type=int, help="port that LEMON listens on", default=8090)
parser.add_argument("-c", "--cookiesecret", help="cookie secret", default="__this_is_A_secret__I_tInk__")
parser.add_argument("-f", "--forms", help="location of forms", required=False, type=os.path.abspath)
#parser.add_argument("-s", "--sql", help="location of sql scripts", default="sql")
parser.add_argument("-d", "--data", help="location of data files", required=False, type=os.path.abspath)
parser.add_argument("-n", "--ngrok", help="is ngrok enabled (or what key)", action="store_true")
parser.add_argument("-nt", "--ngroktoken", help="ngrok API token", default="")
args = parser.parse_args()

print("LemonPY starting")

DATAFOLDER = os.getcwd()
FORMSFOLDER = os.path.join(os.getcwd(), "forms")

if args.data is not None:
	DATAFOLDER = args.data
	Path(DATAFOLDER).mkdir(parents=True, exist_ok=True)
	print("Using " + DATAFOLDER + " as data path")

if args.forms is not None:
	FORMSFOLDER = args.forms
	Path(FORMSFOLDER).mkdir(parents=True, exist_ok=True)
	print("Using " + FORMSFOLDER + " as forms path")

if __name__ == '__main__':
	USERS = Users()

	if args.assertdefaultadmin != "":
		USERS.assert_default_admin_user(args.assertdefaultadmin)
		print("Using supplied admin password")

	if args.assertdefaultadmin == "":
		alphabet = string.ascii_letters + string.digits
		password = ''.join(secrets.choice(alphabet) for i in range(10))
		USERS.assert_default_admin_user(password)
		print("Using generated admin password '" + password + "'")

	ngrok_tunnel = None
	if args.ngrok:
		if args.ngroktoken != "":
			ngrok.set_auth_token(args.ngroktoken)
		ngrok_tunnel = ngrok.connect(args.port, "http")	
	
	form_server = TornadoServer(
		[
			(r".*", FormsServerHandler),
		], 
		cookie_secret = args.cookiesecret,
		port = args.port
	)
	signal.signal(signal.SIGINT, form_server.signal_handler)
	form_server.start()
	
	if args.ngrok:
		print("NGROK URI: " + str(ngrok_tunnel.uri))
		print("NGROK Public URL (or https): " + str(ngrok_tunnel.public_url))

	print("Server Local: http://localhost:" + str(form_server.port))
	print("Ctrl_Break(Clear)/Ctrl_C to exit!")

	tornado.ioloop.PeriodicCallback(form_server.try_exit, 1000).start()
	form_server.block()

	if ngrok_tunnel != None:
		ngrok.disconnect(ngrok_tunnel.public_url)
	