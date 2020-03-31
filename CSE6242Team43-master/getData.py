from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome('chromedriver.exe')
wait = WebDriverWait(driver, 60)

GetDataFrom = [["realGDP","https://fred.stlouisfed.org/series/A191RL1Q225SBEA"],["RealDispInc_growth_l1","https://fred.stlouisfed.org/series/A067RL1Q156SBEA"], ["Unemp_rate_l1","https://fred.stlouisfed.org/series/UNRATE"],["Avg30YrMortgage_rate_l1","https://fred.stlouisfed.org/series/MORTGAGE30US"],["DRSFRMACBS_l1","https://fred.stlouisfed.org/series/DRSFRMACBS"]]


dict = {}

for i in range(len(GetDataFrom)):
    URL = GetDataFrom[i][1]
    VariableName = GetDataFrom[i][0]
    driver.get(URL)
    value = driver.find_element_by_xpath("//span[contains(@class,'series-meta-observation')]").get_attribute('textContent')
    print("Reading ******** ",VariableName)
    pair = {VariableName : value}
    dict.update(pair)
    time.sleep(5)

driver.close()
driver.quit()

print("Dictonary values",dict)
print (json.dumps(dict, ensure_ascii=False))

with open('result.js', 'w') as fp:
    fp.write("var values = "+str(dict))



