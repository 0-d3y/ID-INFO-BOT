import telebot
import requests
import json
import re

TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start'])
def send_welcome(message):
    start_message = """
• مرحبآ بك في بوت معلومات حسابات التليجرام لاظهار معلومات حساب قم بارسال الايدي مباشره وساحظر لك معلوماته

• Dev : t.me/i_0d3y
    """
    bot.reply_to(message,start_message)


@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_message(message):
    chat_id = message.text
    
    response = requests.get(f"http://api.telegram.org/bot{TOKEN}/getChat?chat_id={chat_id}")
    datainfo = json.loads(response.text)
    
    if 'result' in datainfo:
        names = datainfo['result'].get('first_name', 'N/A')
        ids = datainfo['result'].get('id', 'N/A')
        bios = datainfo['result'].get('bio', 'N/A')
        users = datainfo['result'].get('username', 'N/A')
        
        
        photo_file_id = datainfo['result'].get('photo', {}).get('big_file_id', None)
        msg = f"""
*• Name :*  `{names}`
*• Username :* `@{users}`
*• Bio :* ```\n{bios}```
*• ID : *{ids} 
*• Dev : * t.me/i_0d3y
        """
        if photo_file_id:
            file_info = bot.get_file(photo_file_id)
            file_url = f"http://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
            photo = requests.get(file_url)
            bot.send_photo(message.chat.id, photo.content, caption=msg,parse_mode='Markdown')
        else:
            bot.reply_to(message, msg,parse_mode='Markdown')
    else:
        bot.reply_to(message, "لم يتم العثور على حساب بهذا الرقم التعريفي.")


@bot.message_handler(func=lambda message: not message.text.isdigit())
def handle_invalid_message(message):
    bot.reply_to(message, "حبي ارسل الايدي ارقام مو احرف")

if __name__ == "__main__":
    print("Bot is started | Coded By : t.me/i_0d3y")
    bot.infinity_polling()
