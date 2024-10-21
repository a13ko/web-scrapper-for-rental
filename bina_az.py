import requests
from bs4 import BeautifulSoup
import logging
from config import BINA_AZ_URL

logger = logging.getLogger(__name__)

def get_bina_listings():
    logger.info("Bina.az veri çekme işlemi başladı.")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(BINA_AZ_URL, headers=headers, timeout=15)
        logger.info(f"Bina.az isteği yapıldı. Durum kodu: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Bina.az URL'ye erişim sağlanamadı. Durum kodu: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("div", class_="items-i")
        logger.info(f"Bina.az: {len(listings)} ilan bulundu.")

        ads = []
        for listing in listings:
            try:
                title_ul = listing.find("ul", class_="name")
                price_div = listing.find("div", class_="abs_block")
                location_div = listing.find("div", class_="location")
                link_tag = listing.find("a", class_="item_link")

                if all([title_ul, price_div, location_div, link_tag]):
                    title = " ".join([li.text.strip() for li in title_ul.find_all("li")])
                    price = price_div.find("span", class_="price-val").text.strip()
                    location = location_div.text.strip()
                    link = "https://bina.az" + link_tag.get("href", "")

                    ads.append({
                        "source": "Bina.az",
                        "title": title,
                        "price": price,
                        "location": location,
                        "link": link
                    })
                    logger.debug(f"Bina.az ilan işlendi: {title}")
                else:
                    logger.warning("Bina.az: Bir veya daha fazla ilan bilgisi eksik, atlanıyor.")
            except Exception as e:
                logger.error(f"Bina.az ilan işlenirken hata oluştu: {e}")

        logger.info(f"Bina.az: {len(ads)} geçerli ilan bulundu.")
        return ads

    except requests.RequestException as e:
        logger.error(f"Bina.az istek hatası: {e}")
    except Exception as e:
        logger.exception(f"Bina.az beklenmedik bir hata oluştu: {e}")

    return []