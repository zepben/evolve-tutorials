from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://evolve.essential.zepben.com")
assert "EWB App" in driver.title
