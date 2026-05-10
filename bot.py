import telebot
from telebot import types

# Identifiants du Labo Nasser
TOKEN = "8774704728:AAEOSLgJviN9he_EDs-iEsWrNeee08sBZz0"
CHAT_ID = "6727767271"

# URL de ton index.html hébergé sur GitHub Pages
# Exemple: https://nasser-trading.github.io/shield-twa/
WEB_APP_URL = "TA_URL_GITHUB_PAGES_ICI"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_labo(message):
    """Initialisation du bot et affichage du bouton TWA"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Configuration du bouton Web App
    web_app = types.WebAppInfo(WEB_APP_URL)
    btn = types.KeyboardButton(text="🚀 OUVRIR BLACKSNIPER TWA", web_app=web_app)
    
    markup.add(btn)
    
    welcome_text = (
        "🛡️ **SANGMELIMA SHIELD - ACTIVE**\n\n"
        "**Trader :** Nasser\n"
        "**Capital :** 25$\n"
        "**Stratégie :** SMC/ICT Precision\n\n"
        "Prêt pour un sweep PDH/PDL ? Clique sur le bouton ci-dessous."
    )
    
    bot.send_message(CHAT_ID, welcome_text, parse_mode="Markdown", reply_markup=markup)

def alert_sniper(pair, level, type_sweep):
    """Fonction pour t'envoyer une alerte de sweep en direct"""
    msg = (
        f"⚠️ **ALERTE SWEEP DETECTÉ**\n\n"
        f"Instrument: {pair}\n"
        f"Niveau: {level} ({type_sweep})\n"
        f"Action: Attendre la réintégration et le rejet mèche."
    )
    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")

if __name__ == "__main__":
    print(f"Bot BLACKSNIPER SMC lancé pour Nasser (ID: {CHAT_ID})...")
    bot.infinity_polling()
  
