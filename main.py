from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
from time import sleep
import os
from bs4 import BeautifulSoup
import pandas as pd
import datetime

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
  sleep(random.uniform(7,10))

def get_flights_data(url, date):
  flights_data = []
  flights_list_element = driver.find_element(By.XPATH, "//ul[@data-test-id='listings']")
  flights_list_html = flights_list_element.get_attribute("outerHTML")
  # print("flights_list_html:", flights_list_html)
  soup = BeautifulSoup(flights_list_html, 'html.parser')
  # print("flights_list_html:", soup.prettify())
  flights = soup.find_all('li')
  for flight in flights:
    flight_data = {}

    # URL
    flight_data["url"] = url

    # Flight Date
    day_of_week = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%A')
    flight_data["flight_date"] = f"{day_of_week[:3]} - {date}"

    # Flight Price
    price_element = flight.find('span', attrs={"class": "uitk-lockup-price"})
    price = price_element.text.strip()
    flight_data["price"] = price

    # Flight Timeframe
    timeframe_element = flight.find('span', attrs={"data-test-id": "departure-time"})
    timeframe = timeframe_element.text.strip()
    departure_time = timeframe.split(' - ')[0]
    arrival_time = timeframe.split(' - ')[1]
    flight_data["depart_time"] = departure_time
    flight_data["arrive_time"] = arrival_time

    # Flight Duration
    duration_element = flight.find('div', attrs={"data-test-id": "journey-duration"})
    duration = duration_element.text.strip()
    flight_data["duration"] = duration

    # Flight Airline
    airline_element = flight.find('div', attrs={"data-test-id": "flight-operated"})
    airline = airline_element.text.strip()
    flight_data["airline"] = airline

    # Flight Departure and Arrival Airport
    airports_element = flight.find('div', attrs={"data-test-id": "arrival-departure"})
    airports = airports_element.text.strip()
    depart_from = airports.split(' - ')[0]
    arrive_at = airports.split(' - ')[1]
    flight_data["depart_from"] = depart_from
    flight_data["arrive_at"] = arrive_at

    flights_data.append(flight_data)

  return flights_data


def store_flights_data(flights_data, dep_airport, arr_airport):
  current_time = datetime.datetime.now()
  formatted_date = current_time.strftime("%b_%d_%Y")
  columns = ["flight_date", "price", "depart_from", "arrive_at", "depart_time", "arrive_time", "duration", "airline", "url"]
  df = pd.DataFrame(flights_data)
  df = df[columns]
  df.to_csv(f"{dep_airport}_to_{arr_airport}_{formatted_date}.csv", index=False)
  print(f"Flight data stored in: {dep_airport}_to_{arrival_airport}_{formatted_date}.csv")
  



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

  with open("stored_url.txt", "r") as f:
    expedia_url = f.read()
    
  options = Options()
  # options.add_experimental_option("detach", True)

  driver = webdriver.Chrome(options=options)
  driver.set_window_size(900, 1200)
  driver.get(expedia_url)
  sleep(random.uniform(12,14))

  sort_lowtohigh_price()
  flights_data = get_flights_data(expedia_url, date)
  store_flights_data(flights_data, departure_airport, arrival_airport)
