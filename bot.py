import telebot
import ccxt
import threading
import time
from telebot import types

# --- CONFIGURATION LABO ---
TOKEN = "8774704728:AAEOSLgJviN9he_EDs-iEsWrNeee08sBZz0"
CHAT_ID = "6727767271"
WEB_APP_URL = "https://traderprosniper-ship-it.github.io/Kit-IFDA-interbank-flow-/"

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.bingx() # Moteur universel (Crypto + Indices + Forex)

# Liste de surveillance dynamique (tu peux l'éditer ici)
WATCHLIST = ["BTC/USDT", "ETH/USDT", "NAS100", "US30", "XAU/USDT", "GER40"]

# --- LOGIQUE IA ROBOT (Icône AI Chat) ---
def ai_shield_consultant(query):
    query = query.lower()
    if "crt" in query:
        return "🧠 IA SHIELD : Le cycle CRT H4 demande 3 bougies. B1 (Range), B2 (Sweep/Reinteg), B3 (Entry M5). Attends la clôture B2."
    if "indices" in query or "nas100" in query:
        return "🧠 IA SHIELD : Les indices US ouvrent à 14h30 (GMT+1). C'est là que la liquidité est maximale pour un sweep."
    return f"🧠 IA SHIELD : Analyse en cours pour Nasser. Capital: 25$. Risque max: 1.25$."

# --- SCANNER UNIVERSEL INDÉPENDANT ---
def universal_market_scanner():
    print("🛡️ Moteur Universel SANGMELIMA SHIELD lancé sur Termux...")
    while True:
        for symbol in WATCHLIST:
            try:
                # Récupération des bougies H4
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe='4h', limit=2)
                if len(ohlcv) < 2: continue
                
                b1 = {"h": ohlcv[0][2], "l": ohlcv[0][3], "c": ohlcv[0][4]}
                b2 = {"h": ohlcv[1][2], "l": ohlcv[1][3], "c": ohlcv[1][4]}
                
                # Algorithme CRT
                swept_high = b2['h'] > b1['h']
                swept_low = b2['l'] < b1['l']
                reintegrated = b1['l'] < b2['c'] < b1['h']
                
                if (swept_high or swept_low) and reintegrated:
                    type_trade = "BEARISH (Sweep High)" if swept_high else "BULLISH (Sweep Low)"
                    msg = (
                        f"🚨 **SIGNAL CRT DÉTECTÉ : {symbol}**\n\n"
                        f"Type: {type_trade}\n"
                        f"Action: Ouvre la Web App, calcule ton lot et cherche l'entrée M5."
                    )
                    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                    print(f"✅ Signal envoyé pour {symbol}")
                    time.sleep(10) # Petit délai entre les signaux
                    
            except Exception as e:
                print(f"Erreur sur {symbol}: {e}")
                continue
        
        # Scan complet toutes les 15 minutes pour correspondre aux clôtures
        time.sleep(900)

# --- GESTION DES MESSAGES ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = types.WebAppInfo(WEB_APP_URL)
    btn = types.KeyboardButton("🚀 OUVRIR TRADINGGAIN DASHBOARD", web_app=web_app)
    markup.add(btn)
    bot.send_message(CHAT_ID, "🛡️ **LABO SANGMELIMA SHIELD**\nMoteur Universel & IA Active.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def chat_with_ai(message):
    response = ai_shield_consultant(message.text)
    bot.reply_to(message, response)

# --- LANCEMENT ---
if __name__ == "__main__":
    # Lancement du scanner dans un thread indépendant
    scanner_thread = threading.Thread(target=universal_market_scanner, daemon=True)
    scanner_thread.start()
    
    bot.infinity_polling()
                
