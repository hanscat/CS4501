import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait

driver = webdriver.Chrome('C:/Users/Student/Documents/4thYearCode/chromedriver_win32/chromedriver')  # Local path on Ryan's computer, change to wherever chromedriver is located
#Opens a .txt file log of success and failures
selresults = open("selresults.txt", 'w')


#Login Test
driver.get('localhost:8000/login');
time.sleep(3)
username = driver.find_element_by_id('id_username')
username.send_keys('buyer2')
password = driver.find_element_by_id('id_password')
password.send_keys('12345678')
submitbutton = driver.find_element_by_class_name('submit-row')
submitbutton.submit()
time.sleep(3)
currenturl = driver.current_url
if(currenturl == "http://localhost:8000/userdetail"):
	selresults.write("Login Success\n")
else:
	selresults.write("Login Failed\n")


#Search test
driver.get('localhost:8000/search');
time.sleep(3)
searchbox = driver.find_element_by_id('id_query')
searchbox.send_keys('Hans')
searchtype = Select(driver.find_element_by_id('id_query_specifier'))
searchtype.select_by_value('user')
search_box = driver.find_element_by_class_name('submit-row')
search_box.submit()
time.sleep(3)
userfound = driver.find_elements_by_xpath("//*[contains(text(), 'User Found')]")
if (userfound):
	selresults.write("User Search Success\n")
else:
	selresults.write("User search failed\n")


driver.get('localhost:8000/search');
time.sleep(3)
searchbox = driver.find_element_by_id('id_query')
searchbox.send_keys('BMW')
searchtype = Select(driver.find_element_by_id('id_query_specifier'))
searchtype.select_by_value('car')
search_box = driver.find_element_by_class_name('submit-row')
search_box.submit()
time.sleep(3)
carfound = driver.find_elements_by_xpath("//*[contains(text(), 'Car Found')]")
if (carfound):
	selresults.write("Car Search Success\n")
else:
	selresults.write("Car search failed\n")

driver.get('localhost:8000/search');
time.sleep(3)
searchbox = driver.find_element_by_id('id_query')
searchbox.send_keys('2016')
searchtype = Select(driver.find_element_by_id('id_query_specifier'))
searchtype.select_by_value('general')
search_box = driver.find_element_by_class_name('submit-row')
search_box.submit()
time.sleep(3)
generalfound1 = driver.find_elements_by_xpath("//*[contains(text(), 'Car Found')]")
generalfound2 = driver.find_elements_by_xpath("//*[contains(text(), 'User Found')]")
if (generalfound1 or generalfound2):
	selresults.write("General Search Success\n")
else:
	selresults.write("General search failed\n")

#Profile Test
driver.get('http://localhost:8000/userdetail');
time.sleep(3)
currenturl = driver.current_url
if(currenturl == "http://localhost:8000/userdetail"):
	selresults.write("Profile Link Success\n")
else: # Would lead to http://localhost:8000/login?next=/userdetail/
	selresults.write("Profile Link Failed\n")

#Logout Test
driver.get('localhost:8000/logout');
time.sleep(3)
logoutsuccess = driver.find_elements_by_xpath("//*[contains(text(), 'Logout Success')]")
if(logoutsuccess):
	selresults.write("Logout Success\n")
else:
	selresults.write("Logout Failed\n")


#Resigter Test
#Will need to change information after each use so as not to attempt to register same person twice
driver.get('localhost:8000/register');
time.sleep(3)
username = driver.find_element_by_id('id_username')
username.send_keys('buyer12345')
password = driver.find_element_by_id('id_password')
password.send_keys('12345678')
repeatpassword = driver.find_element_by_id('id_password_repeat')
repeatpassword.send_keys('12345678')
firstname = driver.find_element_by_id('id_first_name')
firstname.send_keys('buyerfirstname')
lastname = driver.find_element_by_id('id_last_name')
lastname.send_keys('buyersecondname')

submitbutton = driver.find_element_by_class_name('submit-row')
submitbutton.submit()
time.sleep(3)
registersuccess = driver.find_elements_by_xpath("//*[contains(text(), 'You just signed up!')]")
if(registersuccess):
	selresults.write("Register Success\n")
else:
	selresults.write("Register Failed\n")


driver.quit()
