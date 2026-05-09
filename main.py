import requests
import secrets, random, base64, string,re,time,json
import telebot
from telebot import TeleBot,types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot.apihelper
telebot.apihelper.READ_TIMEOUT = 60
telebot.apihelper.CONNECT_TIMEOUT = 30
#style="primary"
#primary → أزرق
#success → أخضر
#danger → أحمر
ADMIN_ID = 7506329433

def send_response_log(name, response):
    try:
        filename = f"{name}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"URL:\n{response.url}\n\n")
            f.write(f"STATUS:\n{response.status_code}\n\n")
            f.write("HEADERS:\n")
            f.write(json.dumps(dict(response.headers), indent=2, ensure_ascii=False))
            f.write("\n\nBODY:\n")
            f.write(response.text)

        with open(filename, "rb") as doc:
            bot.send_document(
                chat_id=ADMIN_ID,
                document=doc,
                caption=f"📄 Log: {name}"
            )

    except Exception as e:
        print("send_response_log error:", e)
PREFIXES = [
    "/",
    ".",
    "!",
    "~",
    ":",
    "$",
    "<",
    "-",
    "+",
    "?",
    "¿",
    ")",
    "(",
    "#",
    "%",
    "&",
    "*",
    '"',
    "'",
    ";",
    ",",
    "_",
    ">",
    "`",
    "•",
    "|",
    "√",
    "π",
    "×",
    "¶",
    "∆",
    "£",
    "¢",
    "€",
    "¥",
    "^",
    "°",
    "=",
    "{",
    "}",
    "©",
    "®",
    "™",
    "[",
    "]",
]
TOKEN='8765127743:AAFGj0Tas3A7x0607ao9IsXeeSCW7ANkqiU'


bot = TeleBot(TOKEN, parse_mode="HTML")
def command(commands):
    def checker(message):
        if not message.text:
            return False

        text = message.text.strip()

        for prefix in PREFIXES:
            if text.startswith(prefix):
                cmd = text[len(prefix):].split()[0]
                return cmd in commands

        return False

    return checker


stopped_users = set()
stop_keyboard = InlineKeyboardMarkup()
stop_keyboard.add(
    InlineKeyboardButton(
        text="🛑 إيقاف الأرسال",
        callback_data="stop_process",
        style="danger"
    )
)

@bot.callback_query_handler(func=lambda call: call.data == "stop_process")
def stop_process(call):

    user_id = call.from_user.id

    stopped_users.add(user_id)

    bot.answer_callback_query(
        call.id,
        "تم إيقاف العملية."
    )

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )
    

support = types.InlineKeyboardMarkup()
support.add(
    types.InlineKeyboardButton(
        text="💬 مراسلة الدعم",
        url=f"https://instagram.com/6b.bw",
        style="primary"
    )
)
following = {}
followers = {}
despicable = {}

@bot.message_handler(func=command(['start', 'help', 'cmds', 'cmd']))
def start_handler(message):
	bot.reply_to(
        message,
        "ارسل يوزرك بهذا الشكل\n\n<code>@username</code>\nتأكد من كونه حساب عام!"
    )
@bot.message_handler(func=lambda message: message.text and message.text.startswith("@"))
def bool_handler(message):
	user_id = message.from_user.id
	stopped_users.discard(user_id)
	us = message.text.replace("@", "", 1)
	msg=bot.reply_to(message, f"تم استلام اليوزر: <code>{us}</code>")
	headers = {
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
	    'accept-language': 'ar,en;q=0.9',
	}
	url = f'https://www.instagram.com/{us}/'
	rse = requests.get(url, headers=headers)
	ja = re.search(r'"user_id":"(\d+)"', rse.text) or re.search(r'"id":"(\d+)"', rse.text)
	
	if ja:
		id = ja.group(1)
	else:
		send_response_log("instagram_response", rse)
		bot.edit_message_text(
	      chat_id=msg.chat.id,
	      message_id=msg.message_id,
	      text="لم يتم العثور على حسابك."
	    )
		return 
#44
	    
	an_agent='Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
	s=requests.Session()
	r=s.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/',headers={
	 	                'user-agent': an_agent
	 	            },timeout=30).cookies
	 	            
	csrf = r["csrftoken"]
	mid  = r["mid"]
	did  = r["ig_did"]
	lsd="A" + base64.urlsafe_b64encode(secrets.token_bytes(19)).decode().rstrip("=")
	
	jassuzt="2" + ''.join(random.choices(string.digits, k=4))
	
	si='80683688237%3ASzproaehH5mJny%3A28%3AAYhXVGVrLpQIpv8Hn_RpiwDYDPVxEKjIRQP6K0IbAg'
	L=['following','followers']
	following[user_id] = {}
	followers[user_id] = {}
	despicable[user_id] = {}
	dots=0
	
	for page in L:
		headers = {
		    'authority': 'www.instagram.com',
		    'accept': '*/*',
		    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7',
		    'cache-control': 'no-cache',
		    'pragma': 'no-cache',
		    'cookie': f'dpr=3; ds_user_id={si.split("%3A")[0]};csrftoken={csrf}; mid={mid}; ig_nrcb=1; ig_did={did};sessionid={si}',
		    'referer': f'https://www.instagram.com/6b.bw/{page}/',
		    'sec-ch-prefers-color-scheme': 'dark',
		    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
		    'sec-ch-ua-full-version-list': '"Chromium";v="137.0.7337.0", "Not/A)Brand";v="24.0.0.0"',
		    'sec-ch-ua-mobile': '?1',
		    'sec-ch-ua-platform': '"Android"',
		    'sec-fetch-site': 'same-origin',
		    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
		    'x-csrftoken': csrf,
		    'x-ig-app-id': '1217981644879628',
		}
		
		
		url=f'https://www.instagram.com/api/v1/friendships/{id}/{page}/'
		#: 
		max_id = None
		while True:
		    dots = (dots % 3) + 1
		    bot.edit_message_text(
				chat_id=msg.chat.id,
				message_id=msg.message_id,
				text=f"انتظر من فضلك{'.' * dots}"
			)
		
		    params = {
		        'count': '50',
		    }
		
		    if max_id:
		        params['max_id'] = max_id
		    if 'followers' in url:
		    	params['search_surface'] = 'follow_list_page'
		
		    response = s.get(
		        url,
		        params=params,
		        headers=headers,
		    )
		
		    data = response.json()
		    if data.get('require_login',False):
		    	bot.edit_message_text(
	      chat_id=msg.chat.id,
	      message_id=msg.message_id,
	      text="""❌ Session Invalid

تعذر إكمال العملية لأن جلسة إنستغرام لم تعد صالحة أو تم تقييدها مؤقتاً من إنستغرام.""",
	      reply_markup=support
	    )
		    	return 
		
		    if data.get("status") != "ok":
		        message=data.get("message","حدث خطأ اثناء جلب المتابعين.")
		        bot.edit_message_text(
	      chat_id=msg.chat.id,
	      message_id=msg.message_id,
	      text=message,
	      reply_markup=support
	    )
		        return 
		
		    for user in data["users"]:
			    username = user.get("username", "")
			    full_name = user.get("full_name", "")
			    pic_url = user.get("profile_pic_url", "")
			
			    if 'followers' in url:
			        followers[user_id][username] = {
			        "name": full_name,
			        "pic": pic_url
			        }
			    elif 'following' in url:
			    	following[user_id][username]= {
			        "name": full_name,
			        "pic": pic_url
			    	}
		
		
		    if not data.get("has_more"):
		        break
		
		    max_id = data.get("next_max_id")
		    time.sleep(0.5)
	s.close()
	if len(following[user_id]) == 0 and len(following[user_id]) == 0:
			bot.edit_message_text(
				chat_id=msg.chat.id,
				message_id=msg.message_id,
				text="لم يتم العثور على أي مستخدمين تأكد من الحساب اذا كان خاص!\nاذا كنت تعتقد ان هنالك خطأ تفضل بمراسلة الدعم",
				reply_markup=support
			)
			return 
	for username in following[user_id]:
		
		    if username not in followers[user_id]:
		        despicable[user_id][username] = following[user_id][username]
	bot.edit_message_text(
    chat_id=msg.chat.id,
    message_id=msg.message_id,
    text=f"""تم جلب المستخدمين غير المتابعين بنجاح ✅

العدد: <code>{len(despicable[user_id])}</code>

ملاحظة:
قد تجد بعض الأشخاص الذين يتابعونك، وهذا بسبب إعدادات الخصوصية لدى المستخدمين وليس خطأ من البوت!
""",
    reply_markup=stop_keyboard
)
		
		
	for username, info in despicable[user_id].items():
	    if user_id in stopped_users:
	    	break
	    name = info.get("name", "")
	    pic = info.get("pic", "")
	
	    profile_url = f"https://www.instagram.com/{username}/"
	
	    caption = f"""
	هذا المستخدم لا يتابعك ❌
	
	👤 Username: <code>@{username}</code>
	📝 Name: {name}
	"""
	
	    keyboard=InlineKeyboardMarkup()
	    keyboard.add(InlineKeyboardButton(
	    text="فتح حسابه في إنستغرام",
	    url=profile_url,
	    style="danger"
	    )
	    )
	
	    try:
	        if pic:
	            bot.send_photo(
	            	caption=caption,
	            	chat_id=user_id,
	            	parse_mode="HTML",
	            	photo=pic,
	            	reply_markup=keyboard
	            )
	        else:
	            bot.send_message(
	            	text=caption,
	            	chat_id=user_id,
	            	parse_mode="HTML",
	            	reply_markup=keyboard
	            )
	
	    except Exception as e:
	        print("ERROR:", e)
	
	    time.sleep(1)
bot.remove_webhook()
time.sleep(1)
bot.remove_webhook()

bot.infinity_polling(
    timeout=10,
    long_polling_timeout=5,
    skip_pending=True
)
