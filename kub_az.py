import requests
from bs4 import BeautifulSoup
import logging
from config import KUB_AZ_URL

logger = logging.getLogger(__name__)

def get_kub_listings():
    logger.info("Kub.az veri çekme işlemi başladı.")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }

    try:
        response = requests.get(KUB_AZ_URL, headers=headers, timeout=15)
        logger.info(f"Kub.az isteği yapıldı. Durum kodu: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Kub.az URL'ye erişim sağlanamadı. Durum kodu: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")

        # Güncellenmiş sınıf adı
        listings = soup.find_all("div", class_="new-listing-class")  # Burayı güncelleyin
        logger.info(f"Kub.az: {len(listings)} ilan bulundu.")

        ads = []
        for listing in listings:
            try:
                title = listing.find("a", class_="link-address").text.strip()
                price = listing.find("a", class_="link-price").text.strip()
                location = listing.find("div", class_="loc-text").text.strip()
                link = "https://kub.az" + listing.find("a", class_="link-address")["href"]

                ads.append({
                    "source": "Kub.az",
                    "title": title,
                    "price": price,
                    "location": location,
                    "link": link
                })
                logger.debug(f"Kub.az ilan işlendi: {title}")
            except Exception as e:
                logger.error(f"Kub.az ilan işlenirken hata oluştu: {e}")
                logger.debug(f"Hata oluşan ilan HTML'i: {listing}")

        logger.info(f"Kub.az: {len(ads)} geçerli ilan bulundu.")
        return ads

    except requests.RequestException as e:
        logger.error(f"Kub.az istek hatası: {e}")
    except Exception as e:
        logger.exception(f"Kub.az beklenmedik bir hata oluştu: {e}")

    return []
