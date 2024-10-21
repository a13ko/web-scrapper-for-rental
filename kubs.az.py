from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# ChromeDriver yolu
chrome_service = Service('C:/webdriver/chromedriver.exe')
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Kub.az sayfasını aç
KUB_AZ_URL = "https://kub.az/search?adsDateCat=All&entityType=0&buildingType=-1&purpose=1&ownerType=-1&city=1&subwayStation=8&subwayStation=34&subwayStation=2&subwayStation=33&subwayStation=7&subwayStation=59&subwayStation=1&subwayStation=35&words=&documentType=-1&loanType=-1&oneRoom=false&twoRoom=false&threeRoom=false&fourRoom=false&fiveMoreRoom=false&remakeType=-1&minFloor=1&maxFloor=31&minBuildingFloors=1&maxBuildingFloors=31&minPrice=250&maxPrice=450&minArea=&maxArea=&minParcelArea=&maxParcelArea=&search="
driver.get(KUB_AZ_URL)

# Sayfanın yüklenmesini bekle
time.sleep(5)  # Gerekirse süreyi uzatın

# İlanları çekin (örneğin başlıklar)
ilanlar = driver.find_elements(By.CLASS_NAME, 'ad-title-class')  # İlgili elementin sınıf adı ile değiştirin

for ilan in ilanlar:
    print(ilan.text)

# Tarayıcıyı kapat
driver.quit()
