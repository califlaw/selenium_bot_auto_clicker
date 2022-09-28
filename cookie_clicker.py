from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

chrome_driver_path = "/Users/dandelion/Development/chromedriver"
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
# Time every 5 seconds
timeout = time.time() + 5
five_min = time.time() + 60 * 5

# Get a cookie
cookie = driver.find_element(By.ID, "cookie")

# Get a store upgrades
upgrades = driver.find_elements(By.CSS_SELECTOR, '#store div')
upgrades_ids = [item.get_attribute("id") for item in upgrades]

while True:
    cookie.click()

    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        prices = []

        for x in all_prices:
            element = x.text
            if element != "":
                cost = int(element.replace(",", "").strip().split("-")[1])
                prices.append(cost)

        cookie_upgrades = {}
        for n in range(len(prices)):
            cookie_upgrades[prices[n]] = upgrades_ids[n]

        # Get a score
        score = driver.find_element(By.ID, "money").text
        if "," in score:
            score = score.replace(",", "")
        cookie_count = int(score)

        # Find an upgrade that we can afford
        affordable_upgrades = {}
        for cost, idd in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = idd

        # Purchase the most expensive upgrade
        highest_price = max(affordable_upgrades)
        purchase_id = affordable_upgrades[highest_price]

        driver.find_element(By.ID, purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

        # After 5 minutes stop the bot and check the cookies per second count.
        if time.time() > five_min:
            cookie_per_sec = driver.find_element(By.ID, "cps").text
            print(cookie_per_sec)
            break
