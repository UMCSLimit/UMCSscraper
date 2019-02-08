from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import Select

browser = webdriver.Firefox( executable_path = "./geckodriver" )
browser.set_window_size( 900, 900 )
browser.get( "http://www.sip.ztm.lublin.eu" )

s = browser.execute_script( "return s" )
check = browser.execute_script( "return checkcheck()" )
allcookies = { c[ "name" ]: c["value"] for c in browser.get_cookies()  }
print( s )
print( check )
print( allcookies["ASP.NET_SessionId"] )