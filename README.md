[Bounts](bounts.it) have a roulette wheel type thing that you get spins on for logging work outs. But it's painfully slow to use, and doesn't take long to rack up silly amounts of spins.

This automates the spinning process via [Selenium](http://www.seleniumhq.org/).

Requirements:
 
 - [Python 2](https://www.python.org/)
 - [Selenium](http://www.seleniumhq.org/)
 - [Python Selenium bindings](https://pypi.python.org/pypi/selenium) (tested with version 2.48.0)
 - Google Chrome and the [Chrome web driver](https://code.google.com/p/selenium/wiki/ChromeDriver) (tested with version 2.20.353124)

There's no reason Chrome couldn't be replaced by another webdriver supported browser just by changing the browser initialisation line.

Set the environment variables BOUNTS_USR and BOUNTS_PWD to be be your user name and password respectively. 

It doesn't currently handle all the transitions intelligently, it just waits a normally long enough period of time.
