import time
import logging
from telegram.ext import Updater, CommandHandler
from config import BOT_TOKEN
from utils import send_telegram_message, load_sent_ads, save_sent_ads, handle_start_command, load_users
from bina_az import get_bina_listings
from kub_az import get_kub_listings
from ev10_az import get_ev10_listings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

current_ads = []


def send_ads_to_user(chat_id):
    for ad in current_ads:
        message = (
            f"Kaynak: {ad['source']}\n"
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
            new_ads = []
            new_ads.extend(get_bina_listings())
            new_ads.extend(get_kub_listings())
            new_ads.extend(get_ev10_listings())

            current_ads = new_ads  # Mevcut ilanları güncelle

            for ad in new_ads:
                if ad["link"] not in sent_ads:
                    message = (
                        f"Kaynak: {ad['source']}\n"
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