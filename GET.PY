from haverhelpers import chromeBrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import csv

try:
    
    print("RETRIEVING DATA...")
    
    if int(datetime.today().strftime("%d")) == 1:
        today = int(datetime.today().strftime("%m")) - 1         
    else:
        today = int(datetime.today().strftime("%m")) 
    
    driver = chromeBrowser(headless=True)
    
    url = "https://www.bb.org.bd/en/index.php/econdata/exchangerate"
    driver.get(url)
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "form_submit")))
    driver.find_element(By.NAME, "currencies").click()
    driver.find_element(By.XPATH, "//*[@id='inputGroupSelect01']/option[2]").click()
    driver.find_element(By.ID, "dob").click()
    driver.find_element(By.XPATH, f"//*[@id='datepickers-container']/div/div/div/div/div[{today}]").click()
    driver.find_element(By.CLASS_NAME, "form_submit").click()
    
    page = bs(driver.page_source, "lxml")
    table = page.find("table")
    
    non_header_row = 1
    output_rows = []
    
    for header_row in table.findAll("tr")[:non_header_row]:
        columns = header_row.findAll("th")
        output_row = []
        for column in columns:
            try:
                multi_col = int(column["colspan"])
                for x in range(multi_col):
                    output_row.append(column.text)
            except:
                output_row.append(column.text)
        output_rows.append(output_row)
    
    for table_row in table.findAll("tr")[non_header_row:]:
        columns = table_row.findAll("td")
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
        
    print("EXCHANGE RATE RELEASED: ", output_rows[2][0])
        
    with open("XR.CSV", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)
        csvfile.close()

finally:
    driver.close()