import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait

driver = webdriver.Chrome('C:/Users/Student/Documents/4thYearCode/chromedriver_win32/chromedriver')  # Optional argument, if not specified will search path.
driver.get('localhost:8000/login');
time.sleep(3)
username = driver.find_element_by_id('id_username')
username.send_keys('Ryan')
password = driver.find_element_by_id('id_password')
password.send_keys('ryanpassword')
submitbutton = driver.find_element_by_class_name('submit-row')
submitbutton.submit()
time.sleep(3) 
driver.get('localhost:8000/search');
time.sleep(3)
searchbox = driver.find_element_by_id('id_query')
searchbox.send_keys('BMW')
searchtype = Select(driver.find_element_by_id('id_query_specifier'))
searchtype.select_by_value('car')
search_box = driver.find_element_by_class_name('submit-row')
search_box.submit()
time.sleep(3)



driver.quit()
