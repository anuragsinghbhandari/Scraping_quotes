from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd

start = time.time()
Data = []

# Setup driver
driver = webdriver.Safari()
driver.get('https://quotes.toscrape.com/login')

# Fill login form
driver.find_element(By.NAME, 'username').send_keys('Anurag')
driver.find_element(By.NAME, 'password').send_keys('abcd123')
driver.find_element(By.CSS_SELECTOR, 'input.btn').click()

# Scrape data from all pages
i = 1
while True:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'quote'))
    )

    quote_blocks = driver.find_elements(By.CLASS_NAME, 'quote')
    
    for quote_block in quote_blocks:
        try:
            quote = quote_block.find_element(By.CSS_SELECTOR, 'span.text').text
            author = quote_block.find_element(By.CSS_SELECTOR, 'small.author').text
            tags = [tag.text for tag in quote_block.find_elements(By.CSS_SELECTOR, 'a.tag')]

            Data.append({
                "Quote": quote,
                "Author": author,
                "Tags": tags
            })
        except StaleElementReferenceException:
            print("Stale element encountered, skipping this quote.")
            continue

    print(f"Page {i} scraped")
    i += 1

    # Handle next page navigation
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
        next_button.click()

        # Wait for the new page to load before continuing
        WebDriverWait(driver, 10).until(
            EC.staleness_of(quote_blocks[0])  # Wait until the old elements are no longer present
        )
    except NoSuchElementException:
        print("No more pages.")
        break

# Save to DataFrame
df = pd.DataFrame(Data)
df.to_csv('quotes_using_sele.csv')
end = time.time()

print(f'Time taken: {end - start:.2f} seconds')
print(f'Data scraped: {df.shape[0]} quotes')
driver.quit()
