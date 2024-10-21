import requests
from bs4 import BeautifulSoup
import logging
from config import EV10_AZ_URL

logger = logging.getLogger(__name__)

def get_ev10_listings():
    logger.info("Ev10.az veri çekme işlemi başladı.")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(EV10_AZ_URL, headers=headers, timeout=15)
        logger.info(f"Ev10.az isteği yapıldı. Durum kodu: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Ev10.az URL'ye erişim sağlanamadı. Durum kodu: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")

        # Güncellenmiş sınıf adı
        listings = soup.find_all("div", class_="new-listing-class")  # Burayı güncelleyin
        logger.info(f"Ev10.az: {len(listings)} ilan bulundu.")

        ads = []
        for listing in listings:
            try:
                title = listing.find("h5", class_="properties-title").text.strip()
                price = listing.find("div", class_="properties-price").text.strip()
                location = listing.find("div", class_="properties-address").text.strip()
                link = listing.find("a", class_="property-link")["href"]

                ads.append({
                    "source": "Ev10.az",
                    "title": title,
                    "price": price,
                    "location": location,
                    "link": link
                })
                logger.debug(f"Ev10.az ilan işlendi: {title}")
            except Exception as e:
                logger.error(f"Ev10.az ilan işlenirken hata oluştu: {e}")
                logger.debug(f"Hata oluşan ilan HTML'i: {listing}")

        logger.info(f"Ev10.az: {len(ads)} geçerli ilan bulundu.")
        return ads

    except requests.RequestException as e:
        logger.error(f"Ev10.az istek hatası: {e}")
    except Exception as e:
        logger.exception(f"Ev10.az beklenmedik bir hata oluştu: {e}")

    return []
