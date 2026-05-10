import telebot
import ccxt
import time
import threading
from telebot import types

# --- CONFIGURATIONS ---
TOKEN = "8774704728:AAEOSLgJviN9he_EDs-iEsWrNeee08sBZz0"
CHAT_ID = "6727767271"
WEB_APP_URL = "https://traderprosniper-ship-it.github.io/Kit-IFDA-interbank-flow-/"

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.bingx() # Agnostique (Crypto + Indices + Forex)

# Actifs Universels
WATCHLIST = ["BTC/USDT", "NAS100", "US30", "XAU/USDT", "GER40"]

def get_tv_url(symbol):
    s = symbol.replace("/", "").upper()
    if "NAS100" in s: return "https://fr.tradingview.com/chart/?symbol=CAPITALCOM:US100"
    if "US30" in s: return "https://fr.tradingview.com/chart/?symbol=CAPITALCOM:US30"
    if "XAU" in s: return "https://fr.tradingview.com/chart/?symbol=OANDA:XAUUSD"
    return f"https://fr.tradingview.com/chart/?symbol=BINANCE:{s}"

# --- SCANNER CRT H4 ---
def engine_loop():
    print("🛡️ Moteur Universel SANGMELIMA SHIELD Opérationnel...")
    while True:
        for asset in WATCHLIST:
            try:
                ohlcv = exchange.fetch_ohlcv(asset, timeframe='4h', limit=2)
                b1, b2 = ohlcv[0], ohlcv[1]
                
                # Logic CRT (Sweep B1 + Close Inside B1)
                swept = (b2[2] > b1[2]) or (b2[3] < b1[3])
                reintegrated = b1[3] < b2[4] < b1[2]
                
                if swept and reintegrated:
                    url = get_tv_url(asset)
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("👁️ VOIR LE GRAPH", url=url))
                    
                    bot.send_message(CHAT_ID, f"🎯 **SIGNAL CRT: {asset}**\nB2 Sweep + Réintégration.\nGo M5 pour sniper !", 
                                     reply_markup=markup, parse_mode="Markdown")
                    time.sleep(10)
            except: continue
        time.sleep(600) # Scan toutes les 10 min

# --- COMMANDES BOT ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚀 OPEN SHIELD DASHBOARD", web_app=types.WebAppInfo(WEB_APP_URL)))
    bot.send_message(CHAT_ID, "🛡️ **LABO SANGMELIMA SHIELD ACTIF**\nIA et Scanner Universel prêts.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def ai_chat(message):
    msg = message.text.lower()
    if "crt" in msg:
        bot.reply_to(message, "🧠 IA: Le CRT demande un sweep de la B1 et une clôture de la B2 dans le range de la B1. Attends l'entrée M5.")
    else:
        bot.reply_to(message, "🧠 IA: Je surveille le flux IPDA. Capital 25$, risque 1.25$. Prudence.")

if __name__ == "__main__":
    threading.Thread(target=engine_loop, daemon=True).start()
    bot.infinity_polling()
                
