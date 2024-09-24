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

def get_flights_data(url):
  flights_data = []
  flight_date_element = driver.find_element(By.XPATH, "//span[@class='uitk-date-range-button-date-text']")
  flight_date = flight_date_element.text.strip()
  # print("flight date:", flight_date)
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
    flight_data["flight_date"] = flight_date

    # Flight Price
    price_element = flight.find('span', attrs={"class": "uitk-lockup-price"})
    price = price_element.text.strip()
    print(price)
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


def store_flights_data(flights_data):
  current_time = datetime.datetime.now()
  formatted_date = current_time.strftime("%b_%d_%Y")
  columns = ["flight_date", "price", "depart_from", "arrive_at", "depart_time", "arrive_time", "duration", "airline", "url"]
  df = pd.DataFrame(flights_data)
  df = df[columns]
  df.to_csv(f"flight_data_{current_time}.csv")
  print(f"Flight data stored in: flight_data_{current_time}.csv")
  


if __name__ == '__main__':
  with open("stored_url.txt", "r") as f:
    expedia_url = f.read()
  # print("expedia_url:", expedia_url)
    
  options = Options()
  # options.add_experimental_option("detach", True)

  driver = webdriver.Chrome(options=options)
  driver.set_window_size(900, 1200)
  driver.get(expedia_url)
  sleep(random.uniform(7,12))

  sort_lowtohigh_price()
  flights_data = get_flights_data(expedia_url)
  store_flights_data(flights_data)