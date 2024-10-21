import requests
from bs4 import BeautifulSoup
import time
import logging
from telegram.ext import Updater, CommandHandler
from config import BOT_TOKEN, URL
from utils import send_telegram_message, load_sent_ads, save_sent_ads, handle_start_command, load_users

# Logging ayarları
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global değişken olarak mevcut ilanları saklayalım
current_ads = []

def get_listings():
    logger.info("Veri çekme işlemi başladı.")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=15)
        logger.info(f"İstek yapıldı. Durum kodu: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"URL'ye erişim sağlanamadı: {URL}. Durum kodu: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("div", class_="items-i")
        logger.info(f"{len(listings)} ilan bulundu.")

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
                        "title": title,
                        "price": price,
                        "location": location,
                        "link": link
                    })
                    logger.debug(f"İlan işlendi: {title}")
                else:
                    logger.warning("Bir veya daha fazla ilan bilgisi eksik, atlanıyor.")
            except Exception as e:
                logger.error(f"İlan işlenirken hata oluştu: {e}")

        logger.info(f"{len(ads)} geçerli ilan bulundu.")
        return ads

    except requests.RequestException as e:
        logger.error(f"İstek hatası: {e}")
    except Exception as e:
        logger.exception(f"Beklenmedik bir hata oluştu: {e}")

    return []

def send_ads_to_user(chat_id):
    for ad in current_ads:
        message = (
            f"Başlık: {ad['title']}\n"
            f"Fiyat: {ad['price']} AZN\n"
            f"Konum: {ad['location']}\n"
            f"Link: {ad['link']}"
        )
        send_telegram_message(message, [chat_id])
        logger.info(f"Mevcut ilan gönderildi: {ad['title']} - {ad['link']} to {chat_id}")

def start(update, context):
    chat_id = update.effective_chat.id
    logger.info(f"Start command received from chat_id: {chat_id}")
    handle_start_command(chat_id)
    context.bot.send_message(chat_id=chat_id, text="Merhaba! Bot'a hoş geldiniz. Mevcut ilanları gönderiyorum...")
    send_ads_to_user(chat_id)

def main():
    global current_ads
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    logger.info("Bot started polling")

    sent_ads = load_sent_ads()

    while True:
        try:
            new_ads = get_listings()
            current_ads = new_ads  # Mevcut ilanları güncelle

            for ad in new_ads:
                if ad["link"] not in sent_ads:
                    message = (
                        f"Başlık: {ad['title']}\n"
                        f"Fiyat: {ad['price']} AZN\n"
                        f"Konum: {ad['location']}\n"
                        f"Link: {ad['link']}"
                    )
                    send_telegram_message(message)
                    logger.info(f"Yeni ilan gönderildi: {ad['title']} - {ad['link']}")
                    sent_ads.add(ad["link"])

            save_sent_ads(sent_ads)
            logger.info("Gönderilen ilanlar kaydedildi. 60 saniye bekleniyor...")
            time.sleep(60)
        except Exception as e:
            logger.exception(f"Ana döngüde beklenmeyen hata: {e}")
            logger.info("60 saniye sonra yeniden denenecek...")
            time.sleep(60)

if __name__ == "__main__":
    main()