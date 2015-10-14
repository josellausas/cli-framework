#!bin/python
#! -​*- coding:utf-8 -*​-


'''
	Project name here
	=================

	About
	-----
	This is a template for quickly creating  a new Cement Framework Apps. 
	For documentation please visit the official [CementFremework site](http://builtoncement.com/)

	Based on: [http://builtoncement.com/2.6/](http://builtoncement.com/2.6/)

	Get started
	-----------
	1. This requires Cement 2.6 to be installed. Install it with: `pip install cement`
	2. We recomend using virtualenv.

	### Run the app
	`./myapp.py --help`

'''
import sys
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core.interface import Interface, Attribute
from cement.core import hook
from cement.core import handler
from cement.utils.misc import init_defaults
from cement.core.exc import FrameworkError, CaughtSignal
from signal import SIGINT, SIGABRT


# ---------------------
# Define the App
appname = 'myapp'
# Definir nuestros defaults
defaults = init_defaults(appname)
defaults[appname]['debug'] = False
defaults[appname]['some_custom_param'] = 'Some custom value'
# Definir la descripción de la app
appDescription = "\t===============\n\t= App CLI\n\t===============\n\t-> This is a template"


# Define Hooks
def my_cleanup_hook(app):
	pass


# The base controller for the app
class MyBaseController(CementBaseController):
	class Meta:
		label = 'base'
		# The app's description is taken from the base controller
		description = appDescription
		arguments = [
			(['-f', '--foo'], dict(action='store', help='The notorious foo option')),
			(['-C'], dict(action='store_true', help='The big C option')),
		]

	@expose(hide=True)
	def default(self):
		self.app.log.info("Inside BaseController.default()")
		if(self.app.pargs.foo):
			print("Received the foo option: %s" % self.app.pargs.foo)

	@expose(help="This command does nothing useful")
	def command1(self):
		self.app.log.info("Inside command 1")

	@expose(aliases=['cmd2'], help="More nothing")
	def command2(self):
		self.app.log.info("Inside command 2")



# A secondary controller for the app
class MySecondController(CementBaseController):
	class Meta:
		label = 'second'
		stacked_on = 'base'

	@expose(help='this is some command from the second controller', aliases=['some-cmd'])
	def second_cmd1(self):
		self.app.log.info("Inside second controller command1")


# Definir la app
class MyApp(CementApp):
	class Meta:
		label = appname
		config_defaults = defaults
		# extensions = ['daemon', 'memcached', 'json', 'yaml']
		extensions = ['json']
		#Custom controllers here
		base_controller = 'base'
		handlers = [MyBaseController, MySecondController]


'''
	main function ------->
'''
def main():
	# Run the app:
	with MyApp() as app:
		# Register custom app hooks
		hook.register('pre_close', my_cleanup_hook)

		# Add args to parser. These must not conflict with the controller's
		app.args.add_argument('-ll', '--llau', action='store', metavar='STR', help='The notorious Llau option')

		# Log stuff
		app.log.debug("Starting the app")

		try:
			app.run()
		except CaughtSignal as e:
			if(e.signum == signal.SIGTERM):
				print("Caught SIGTERM")
			elif(e.signum == signal.SIGINT):
				print("Caught SIGINT")

		except FrameworkError as fe:
			print("FrameworkError: %e" %fe)

		finally:
			if(app.debug):
				import traceback
				traceback.print_exc()

		if app.pargs.llau:
			app.log.info("Llau flag received: %s" % app.pargs.foo )

# Run only if this file is the executed one.
if __name__ == '__main__':
	main()
