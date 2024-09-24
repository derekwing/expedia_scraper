from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
from time import sleep
import os

def click_one_way_tab():
  oneway_tab = driver.find_element(By.XPATH, "//a[@aria-controls='FlightSearchForm_ONE_WAY']")
  oneway_tab.click()
  sleep(random.uniform(1,2))

def select_airports(departure_airport="IAH", arrival_airport="SFO"):
  # Set Departure to (User's departure airport value)
  departure_open_input_button = driver.find_element(By.XPATH, "//button[@aria-label='Leaving from']")
  departure_open_input_button.click()
  sleep(random.uniform(3,7))
  departure_input = driver.find_element(By.XPATH, "//input[@id='origin_select']")
  departure_input.send_keys(departure_airport) # Replace with user's departure airport value
  sleep(random.uniform(1,2))
  departure_input.send_keys(Keys.ENTER)
  sleep(random.uniform(1,2))

  # Set Arrival to (User's arrival airport value)
  arrival_open_input_button = driver.find_element(By.XPATH, "//button[@aria-label='Going to']")
  arrival_open_input_button.click()
  sleep(random.uniform(3,7))
  arrival_input = driver.find_element(By.XPATH, "//input[@id='destination_select']")
  arrival_input.send_keys(arrival_airport) # Replace with user's arrival airport value
  sleep(random.uniform(1,2))
  arrival_input.send_keys(Keys.ENTER)
  sleep(random.uniform(1,2))

def select_date(date):
  date_open_input_button = driver.find_element(By.XPATH, "//button[@id='date_form_field-btn']")
  date_open_input_button.click()
  sleep(random.uniform(3,5))

  # Select date
  date_element = driver.find_element(By.XPATH, f"//button[@aria-label='{date}']")
  print("selected_day_element:",  date_element.get_attribute("outerHTML"))
  actions.move_to_element(date_element).perform()
  date_element.click()
  sleep(random.uniform(1,2))

  # Apply date
  apply_date_button = driver.find_element(By.XPATH, "//button[@data-stid='apply-date-picker']")
  apply_date_button.click()
  sleep(random.uniform(1,2))

  # Click Search
  search_button = driver.find_element(By.XPATH, "//button[@id='search_button']")
  search_button.click()
  sleep(random.uniform(2,4))

def store_url_in_txt():
  current_url = driver.current_url
  with open("stored_url.txt", "w") as f:
    f.write(current_url)

def execute_main2py():
  os.system("python main2.py")

def sort_lowtohigh_price():
  # Sort prices by (lowest to highest)
  filter_modal_button = driver.find_element(By.XPATH, "//button[@data-test-id='sort-filter-dialog-trigger']")
  filter_modal_button.click()
  sleep(random.uniform(2,4))

  # Open filter dropdown
  filter_dropdown = driver.find_element(By.XPATH, "//select[@id='sort-filter-dropdown-SORT']")
  filter_dropdown.click()
  sleep(random.uniform(1,2))

  low_to_high_option = driver.find_element(By.XPATH, "//option[@value='PRICE_INCREASING']")
  low_to_high_option.click()
  sleep(random.uniform(1,2))

  # Apply filter
  apply_filter_button = driver.find_element(By.XPATH, "//button[@data-test-id='sort-filter-done-button']")
  apply_filter_button.click()
  sleep(random.uniform(10,15))



if __name__ == '__main__':
  departure_airport = input("Enter departure airport: ")
  arrival_airport = input("Enter arrival airport: ")
  date = input("Enter date with format 'Jun 3, 2025'. \nOnly enter the first 3 letters of the month: ")

  months_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
  day = 3

  expedia_url = 'https://www.expedia.com/Flights'
  options = Options()
  # options.add_experimental_option("detach", True)

  driver = webdriver.Chrome(options=options)
  driver.set_window_size(900, 1300)
  driver.get(expedia_url)
  actions = ActionChains(driver)
  click_one_way_tab()
  select_airports(departure_airport, arrival_airport)
  select_date(date)
  store_url_in_txt()
  driver.quit()
  execute_main2py()
