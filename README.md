# LemonPY

LemonPY is an easy to use web framework. It is meant to be a simple, low fuss, batteries included framework. It is a fun escape from the complications of modern web application development. 

The framework API is simple enough to be learned in 5 mins and easy enough to code on an iPad. All code is written in python and the client markup is generated from the server side. Ngrok is built in for remote development and sharing your apps with your friends without having to stand up server infrastructure. 

The UI takes cues from text only systems such as a unix terminal and 3270. Pages are built around the concept of "Forms" (web pages) and "Components" (text only GUI elements). The client side UI automatically adjusts its font size based on the amount of room in the browser window. Components are positioned absolutley given X and Y positions.

## Install

1. Create a project folder (GIT, SVN, Plain Folder, etc...)
2. curl https://lemonpy.dev | sh
3. Modify/Create forms! Profit!!!

## Running

Usage: LEMON.py

Arguments:

- show this help message and exit
  * -h, --help

- upserts an admin user for authentication and print out the password to stdout. if the argument is specified without a value a password will be generated.
  * -a "optional password" or --assertdefaultadmin "optional password"

- port that is serving on (8090 is the default if not specified)
  * -p PORT, --port PORT

- cookie secret that is passed to tornado (used for signing, not for encrypting). default is "__this_is_A_secret__I_tInk__"
  * -c COOKIESECRET, --cookiesecret COOKIESECRET

- path for location of forms (default is current path)
  * -f FORMS, --forms FORMS

- path for location of sqlite DB file (default is current path)
  * -d DATA, --data DATA  

- is ngrok enabled for easy public serving
  * -n, --ngrok

- ngrok account key (or API token)
  * -nt NGROKTOKEN, --ngroktoken NGROKTOKEN

### Examples

Run on port 8090, do not use NGROK, Data is stored in path, no admin user is upserted, insecure secret for cookie.

```sh
./LEMON.py
```

Run on port 80, use NGROK, Data is stored in path, admin user is upserted with auto password, insecure secret for cookie.

```sh
./LEMON.py -p 80 -n -a
```

Run on port 8080, use NGROK with API key, Data is stored in path, admin user is upserted with given password, secure secret for cookie specified.

```sh
./LEMON.py -p 8080 -n -nt XXXXXXXX -a asdjklnci9 -c slkdnf_as_sdasdsds_3
```

## API Reference

### Form

Files containing a Form are contained in the forms directory. These are python files that get executed at runtime. File names should follow the convention "NameForm.py" with the name of the form with no spaces, followed by "Form.py".

Forms are navigated to via subpath, ex. http://localhost:8080/Login where Login is the Form name. Index is the default is Form is empty.

A Form is created by subclassing Lemon.Form.
There are 2 methods to override, "init" and "on_submit". "init" should be where the view is defined and setup. "on_submit" is where the logic is.

#### "init"

Set self.title and self.fields. self.fields is an array of components.

#### "on_submit"

Handle submissions on the form. In "on_submit", self is a dictionary of components. self.persist_field_values() will persist all component values in the submission. self.get_submit_type() will get the submission type. Return a string to change the view, where "/" is the IndexForm and None is the same form.

#### From Class Definition

The values can change in "init" or on "on_submit". The web page will automatically scale to the width and height of the form.

```
Form
	# Title of the Form (webpage)
	self.title = ""
	# Array contaning components
	self.fields = []
	# How wide in em the form is
	self.width = 80
	# How tall in em the form is
	self.height = 32
	# Should scaling be turned on
	self.is_scaled = True
```

### Session

Sessions are a part of the Form and are persisted as cookies. A unique ID is generated and stored in a cookie, and the data is sotred in the SQLITE DB. If using make sure your "cookie_secert" is secure in the arguments at startup in production. The Session object is a dictionary:

```
self.session["is_logged_in"] = True
self.session["username"] = self["username"].value
```

or

```
del self.session["is_logged_in"]
```

### Text Modifiers

#### Color Values
```
Colors.
	RED = "#FF0000"
	TEAL = "#BCFEFD"
	GREEN = "#40F85A"
	PURPLE = "#7992F9"
	NORMAL = "#FEFEFE"
	YELLOW = "#FFFF00"
	BLUE = "#0000FD"
```

#### TextColor

```
TextColor(text, color = "initial")
```

#### TextMultiLine

```
TextMultiLine(text, color = "initial")
```

#### TextBold

```
TextBold(text)
```

### Components

#### TextBar

```
TextBar(
	text, 
	width, 
	name = None, 
	x = 0, y = 0):
```

#### Text (label)

```
Text(
	text, 
	name = None, 
	x = 0, y = 0)
```

#### TextField

```
TextField(
	label, 
	color=None, 
	value="", 
	field_length=10, 
	placeholder="", 
	is_password=False, 
	name = None, 
	x = 0, y = 0):
```

#### PaswordField

```
PasswordField(
	label, 
	value="", 
	field_length=10, 
	placeholder="", 
	name = None, 
	x = 0, y = 0)
```