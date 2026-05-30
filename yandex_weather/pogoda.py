import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

start_url = (
    "https://yandex.ru/pogoda/ru/krasnodar"
    "?lat=45.035469&lon=38.975311"
)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts,
)

driver.get(start_url)
time.sleep(3)

mesyac_url = None
for link in driver.find_elements(By.TAG_NAME, "a"):
    href = link.get_attribute("href")
    if href and "/month" in href and "krasnodar" in href:
        mesyac_url = href
        break

if mesyac_url:
    driver.get(mesyac_url)
else:
    driver.get("https://yandex.ru/pogoda/ru/krasnodar/month?lat=45.035469&lon=38.975311")

time.sleep(8)

dni = driver.find_elements(By.CSS_SELECTOR, "li[class*='calendar__item']")

for blok in dni:
    stroki = []
    for chast in blok.text.split("\n"):
        chast = chast.strip()
        if chast:
            stroki.append(chast)
    if len(stroki) < 4:
        continue
    if "°" in stroki[1]:
        data = stroki[3].split(",")[0]
        den = stroki[1]
        noch = stroki[2]
    else:
        data = stroki[0] + " " + stroki[1]
        den = stroki[2]
        noch = stroki[3]
    print(data, "| день:", den, "| ночь:", noch)

driver.quit()
