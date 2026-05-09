import requests
import secrets, random, base64, string,re,time,json
import telebot
from telebot import TeleBot,types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot.apihelper

TOKEN = '8765127743:AAFGj0Tas3A7x0607ao9IsXeeSCW7ANkqiU'  # استخدمت التوكين الثاني
telebot.apihelper.READ_TIMEOUT = 60
telebot.apihelper.CONNECT_TIMEOUT = 30

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
            bot.send_document(chat_id=ADMIN_ID, document=doc, caption=f"📄 Log: {name}")
    except Exception as e:
        print("send_response_log error:", e)

PREFIXES = ["/", ".", "!", "~", ":", "$", "<", "-", "+", "?", "¿", ")", "(", "#", "%", "&", "*", '"', "'", ";", ",", "_", ">", "`", "•", "|", "√", "π", "×", "¶", "∆", "£", "¢", "€", "¥", "^", "°", "=", "{", "}", "©", "®", "™", "[", "]"]

import requests, uuid, json
from user_agent import generate_user_agent as ua

def check_session_web(sessionid: str):
    an_agent = ua()
    cookies = {"sessionid": sessionid}
    headers = {
        "User-Agent": an_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        r = requests.get("https://www.instagram.com/accounts/edit/", headers=headers, cookies=cookies, allow_redirects=True)
    except:
        return False
    if r.status_code == 200:
        if "checkpoint" in r.url or "login" in r.url:
            return False
        match = re.search(r'"full_name":"([^"]+)"', r.text)
        if match:
            return True, json.loads(f'"{match.group(1)}"')
        return True, "Unknown Name"
    return False

def check_session(sess: str):
    cookies = {"sessionid": sess}
    headers = {
        "User-Agent": "Instagram 262.0.0.11.117 Android (30/3.0; 320dpi; 720x1280; samsung; SM-G973F; beyond1; exynos9820; en_US)",
        "Accept": "*/*",
        "X-IG-Capabilities": "3brTvw==",
        "X-IG-Connection-Type": "WIFI",
    }
    r = requests.get("https://i.instagram.com/api/v1/accounts/current_user/?edit=true", headers=headers, cookies=cookies, timeout=10)
    try:
        data = r.json()
    except:
        return False
    if r.status_code == 400 or r.status_code == 403:
        return check_session_web(sess)
    if data.get("message") == "unsupported_version":
        return check_session_web(sess)
    if data.get("status") == "ok" and "user" in data:
        return True, data["user"]["full_name"]
    return False

import re
from urllib.parse import unquote

SESSION_PATTERN = re.compile(r'\d+(?::|%3A)[A-Za-z0-9]+(?::|%3A)\d+(?::|%3A)[A-Za-z0-9_-]+')

def extract_sessionid(data):
    if isinstance(data, (dict, list)):
        text = json.dumps(data)
    else:
        text = str(data)
    text = unquote(text)
    match = SESSION_PATTERN.search(text)
    return match.group() if match else None

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

def get_user_info(username, sessionid=None):
    headers = {
        "User-Agent": "Instagram 370.0.0.42.96 Android",
        "Accept": "*/*"
    }
    cookies = {}
    if sessionid:
        cookies["sessionid"] = sessionid
    
    # جلب PK من HTML أولاً
    url = f'https://www.instagram.com/{username}/'
    try:
        r = requests.get(url, headers=headers, cookies=cookies, timeout=15)
        
        if r.status_code != 200:
            return {"ok": False, "status": r.status_code}
        
        # استخراج PK من HTML
        pk = find(r.text, '{"content_type":"PROFILE","target_id":"', '"}}}')
        if not pk:
            return {"ok": False, "message": "لم يتم العثور على PK المستخدم"}
        
        # استخدام API لجلب المعلومات الكاملة باستخدام PK
        api_url = f"https://i.instagram.com/api/v1/users/{pk}/info/"
        api_headers = {
            "User-Agent": "Instagram 370.0.0.42.96 Android",
            "Accept": "*/*",
            "X-IG-App-ID": "936619743392459",
        }
        
        api_response = requests.get(api_url, headers=api_headers, cookies=cookies, timeout=15)
        
        if api_response.status_code != 200:
            return {"ok": False, "message": f"فشل جلب المعلومات: {api_response.status_code}"}
        
        data = api_response.json()
        
        if "user" not in data:
            return {"ok": False, "message": "لم يتم العثور على المستخدم في الرد"}
        
        user = data["user"]
        
        # استخراج رابط الصورة بشكل صحيح
        profile_pic_url = user.get("hd_profile_pic_url_info", {}).get("url")
        if not profile_pic_url:
            profile_pic_url = data.get("profile_pic_url")
        
        return {
            "ok": True,
            "pk": user.get("pk"),
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "biography": user.get("biography"),
            "is_private": user.get("is_private"),
            "is_verified": user.get("is_verified"),
            "followers": user.get("follower_count", 0),
            "following": user.get("following_count", 0),
            "posts": user.get("media_count", 0),
            "profile_pic_url": profile_pic_url
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)}

def check_user_follows_developer(user_id, dev_username="6b.bw", sessionid=None):
    """التحقق إذا كان المستخدم يتابع حساب المطور"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        "Accept": "*/*",
    }
    cookies = {}
    if sessionid:
        cookies["sessionid"] = sessionid
    
    # جلب معرف المطور أولاً
    dev_info = get_user_info(dev_username, sessionid)
    if not dev_info.get("ok"):
        return False
    
    dev_pk = dev_info.get("pk")
    
    # التحقق من علاقة المتابعة
    url = f"https://i.instagram.com/api/v1/users/{user_id}/full_detail_info/"
    try:
        r = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if r.status_code != 200:
            return False
        data = r.json()
        user_detail = data.get("user_detail", {}).get("user", {})
        following = user_detail.get("following_count", 0)
        # هذا ليس دقيقاً 100%، بديل أفضل:
        # نستخدم endpoint آخر للتحقق من متابعة مستخدم معين
        check_url = f"https://i.instagram.com/api/v1/friendships/show/{dev_pk}/"
        r2 = requests.get(check_url, headers=headers, cookies=cookies, timeout=10)
        if r2.status_code == 200:
            friendship = r2.json()
            return friendship.get("followed_by", False)
        return False
    except:
        return False

stopped_users = set()
stop_keyboard = InlineKeyboardMarkup()
stop_keyboard.add(InlineKeyboardButton(text="🛑 إيقاف الإرسال", callback_data="stop_process",style="danger"))

@bot.callback_query_handler(func=lambda call: call.data == "stop_process")
def stop_process(call):
    user_id = call.from_user.id
    stopped_users.add(user_id)
    bot.answer_callback_query(call.id, "تم إيقاف العملية.")
#    bot.send_message(text="✅ تم إيقاف العملية", chat_id=user_id)

support = types.InlineKeyboardMarkup()
support.add(types.InlineKeyboardButton(text="💬 مراسلة الدعم", url="https://instagram.com/6b.bw",style="primary"))

follo = types.InlineKeyboardMarkup()
follo.add(types.InlineKeyboardButton(text="➕ متابعة مطور البوت", url="https://instagram.com/6b.bw",style="primary"))

@bot.message_handler(func=command(['start', 'help', 'cmds', 'cmd']))
def start_handler(message):
    bot.reply_to(message, "📌 أرسل يوزرك بهذا الشكل:\n\n<code>@username</code>\nتأكد من كون الحساب عام!", reply_markup=follo)

si = '80683688237%3AluP74n6IjS0gUA%3A15%3AAYjGncVepCutJKlhmPu4rNco1eKGyHzRvkzvr0lu8g'

def find(ichi, ni='', san=''):
    if ni in ichi:
        yon = ichi.index(ni) + len(ni)
        go = ichi[yon:len(ichi)]
        roku = go.index(san) if san in go else len(go)
        return go[0:roku]
    return ''

def get_user_pk_from_html(html, username):
    """استخراج PK المستخدم من HTML"""
    patterns = [
        r'"target_id":"(\d+)"',
        r'"user_id":"(\d+)"',
        r'"pk":"(\d+)"',
        r'"id":"(\d+)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    
    # محاولة البحث عن profile page
    match = re.search(r'{"content_type":"PROFILE","target_id":"(\d+)"', html)
    if match:
        return match.group(1)
    return None

# متغير لتخزين بيانات المستخدم مؤقتاً قبل التأكيد
pending_users = {}

@bot.message_handler(func=lambda message: message.text and message.text.startswith("@"))
def handle_username(message):
    user_id = message.from_user.id
    stopped_users.discard(user_id)
    username = message.text.replace("@", "", 1).strip()
    
    msg = bot.reply_to(message, f"⏳ جاري التحقق من حساب <code>{username}</code>...")
    
    if not check_session(si):
        bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
            text="❌ جلسة الإنستغرام غير صالحة أو تم تقييدها مؤقتاً.",
            reply_markup=support
        )
        return
    
    # جلب معلومات المستخدم
    user_info = get_user_info(username, si)
    if not user_info.get("ok"):
        bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
            text=f"❌ لم يتم العثور على حساب <code>{username}</code>\nتأكد من صحة اليوزر وأن الحساب عام.",
            reply_markup=support
        )
        return
    
    # تخزين معلومات المستخدم مؤقتاً
    pending_users[user_id] = {
        "username": username,
        "pk": user_info.get("pk"),
        "full_name": user_info.get("full_name"),
        "followers": user_info.get("followers", 0),
        "following": user_info.get("following", 0),
        "posts": user_info.get("posts", 0),
        "is_private": user_info.get("is_private", False),
        "profile_pic": user_info.get("profile_pic_url", ""),
        "confirm_message_id": msg.message_id,
        "chat_id": msg.chat.id,
        "message":message
    }
    
    # إنشاء كيبورد التأكيد
    confirm_keyboard = InlineKeyboardMarkup(row_width=2)
    confirm_keyboard.add(
        InlineKeyboardButton("✅ نعم، هذا حسابي", callback_data=f"confirm_yes:{username}",style="success"),
        InlineKeyboardButton("❌ لا، هذا ليس حسابي", callback_data=f"confirm_no:{username}",style="danger")
    )
    
    # عرض معلومات الحساب مع صورة
    caption = f"""📌 <b>هل هذا حسابك؟</b>

👤 <b>اليوزر:</b> <code>@{username}</code>
📝 <b>الاسم:</b> {user_info.get('full_name', 'لا يوجد')}
👥 <b>المتابعون:</b> {user_info.get('followers', 0):,}
📖 <b>يتابع:</b> {user_info.get('following', 0):,}
📷 <b>المنشورات:</b> {user_info.get('posts', 0):,}
🔒 <b>حساب خاص:</b> {'نعم' if user_info.get('is_private') else 'لا'}

✨ <i>إذا كان هذا حسابك، اضغط "نعم" للمتابعة</i>"""


    try:
        if user_info.get('profile_pic_url'):
            bot.edit_message_media(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                media=types.InputMediaPhoto(media=user_info['profile_pic_url'], caption=caption, parse_mode="HTML"),
                reply_markup=confirm_keyboard
            )
        else:
            bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text=caption,
                reply_markup=confirm_keyboard,
                parse_mode="HTML"
            )
    except Exception as e:
        bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
            text=caption,
            reply_markup=confirm_keyboard,
            parse_mode="HTML"
        )
def is_follow(query,id):
	headers = {
    'User-Agent': 'Mozilla/5.0',
    'X-IG-App-ID': '936619743392459',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/',
    'Cookie': f'sessionid={si};',
}
	params = {
	    'count': '1',
	    'query': query,
	    'search_surface': 'follow_list_page',
	}
	
	response = requests.get(
	    'https://i.instagram.com/api/v1/friendships/60103550730/followers/',
	    params=params,
	    headers=headers,
   )
	print(response.json())
	try:
		pk=(response.json().get("users")[0])
		pk=pk['pk_id']
		print(pk,id)
		if pk != id:
			return False
	except:
		return False
	return True
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def handle_confirm(call):
    user_id = call.from_user.id
    action, username = call.data.split(":", 1)
    
    if action == "confirm_no":
        bot.answer_callback_query(call.id, "❌ تم الإلغاء، أرسل اليوزر الصحيح من فضلك.")
        
        # حذف الرسالة القديمة
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        
        # إرسال رسالة جديدة
        bot.send_message(
            chat_id=call.message.chat.id,
            text="❌ تم الإلغاء.\nأرسل اليوزر الصحيح على شكل @username"
        )
        
        if user_id in pending_users:
            del pending_users[user_id]
        return
    
    # action == "confirm_yes"
    if user_id not in pending_users or pending_users[user_id].get("username") != username:
        bot.answer_callback_query(call.id, "⚠️ يرجى إعادة إرسال اليوزر من جديد.")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        return
    
    user_data = pending_users[user_id]
    
    # حذف الرسالة القديمة (التي تحتوي على الأزرار)
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # أيضاً حذف رسالة "جاري التحقق" إذا كانت موجودة
        if "confirm_message_id" in user_data:
            bot.delete_message(chat_id=call.message.chat.id, message_id=user_data["confirm_message_id"])
    except Exception as e:
        print(f"Error deleting message: {e}")
    
    bot.answer_callback_query(call.id, "✅ جاري التحقق من متابعتك للمطور...")
    
    # إرسال رسالة جديدة بدلاً من تعديل القديمة
    new_msg = bot.reply_to(
        message=pending_users[user_id]['message'],
        text=f"⏳ جاري التحقق من معلوماتك"
    )
    
    # تحديث pending_users بالرسالة الجديدة
    pending_users[user_id]["processing_msg_id"] = new_msg.message_id
    
#    # التحقق من متابعة المطور
#    pk = user_data.get("pk")
    
#    isfo=is_follow(username,pk)
#    if not isfo:
#        bot.edit_message_text(
#            chat_id=call.message.chat.id,
#            message_id=new_msg.message_id,
#            text=f"⚠️ لا يمكنك استخدام البوت إلا إذا قمت بمتابعة المطور أولاً!\n\n👤 مطور البوت: @6b.bw\n\nقم بمتابعته ثم أعد إرسال اليوزر.",
#            reply_markup=follo
#        )
#        if user_id in pending_users:
#            del pending_users[user_id]
#        return
#    bot.edit_message_text(
#        chat_id=call.message.chat.id,
#        message_id=new_msg.message_id,
#        text=f"✅ تم التأكيد! أنت تتابع المطور.\n\n⏳ جاري جلب قائمة غير المتابعين لحساب <code>{username}</code>..."
#    )
    
    # حذف المستخدم من pending
    del pending_users[user_id]
    
    # تشغيل عملية جلب غير المتابعين مع معرف الرسالة الجديد
    start_fetching_nonfollowers(call.message.chat.id, user_id, username, new_msg.message_id)

def start_fetching_nonfollowers(chat_id, user_id, username, edit_msg_id):
    """استكمال جلب غير المتابعين بعد التأكيد"""
    
    an_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
    s = requests.Session()
    r = s.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers={'user-agent': an_agent}, timeout=30).cookies
    csrf = r["csrftoken"]
    mid = r["mid"]
    did = r["ig_did"]
    
    headers = {
        'sec-fetch-mode': 'navigate',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7',
        'user-agent': an_agent,
        'cookie': f'dpr=3; csrftoken={csrf}; mid={mid}; ig_nrcb=1; ig_did={did}; sessionid={si}',
    }
    url = f'https://www.instagram.com/{username}/'
    rse = s.get(url, headers=headers)
    
    # استخراج ID المستخدم
    user_id_from_html = get_user_pk_from_html(rse.text, username)
    if not user_id_from_html:
        user_id_from_html = find(rse.text, '{"content_type":"PROFILE","target_id":"', '"}}}')
    
    if not user_id_from_html:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=edit_msg_id,
            text="❌ لم يتم العثور على الحساب. تأكد من صحة اليوزر.",
            reply_markup=support
        )
        return
    
    cookies = f'dpr=3; ds_user_id={si.split("%3A")[0]}; csrftoken={csrf}; mid={mid}; ig_nrcb=1; ig_did={did}; sessionid={si}'
    
    following_dict = {}
    followers_dict = {}
    despicable_dict = {}
    dots = 0
    
    for page_type in ['following', 'followers']:
        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'cookie': cookies,
            'referer': f'https://www.instagram.com/6b.bw/{page_type}/',
            'user-agent': an_agent,
            'x-csrftoken': csrf,
            'x-ig-app-id': '1217981644879628',
        }
        
        url = f'https://www.instagram.com/api/v1/friendships/{user_id_from_html}/{page_type}/'
        max_id = None
        
        while True:
            dots = (dots % 3) + 1
            try:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=edit_msg_id,
                    text=f"⏳ جاري التحميل{'.' * dots}\n📌 {page_type}..."
                )
            except:
                pass
            
            params = {'count': '50'}
            if max_id:
                params['max_id'] = max_id
            if page_type == 'followers':
                params['search_surface'] = 'follow_list_page'
            
            response = s.get(url, params=params, headers=headers)
            data = response.json()
            
            if data.get('require_login', False):
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=edit_msg_id,
                    text="❌ انتهت صلاحية الجلسة. يرجى المحاولة لاحقاً.",
                    reply_markup=support
                )
                return
            
            if data.get("status") != "ok":
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=edit_msg_id,
                    text=f"❌ حدث خطأ: {data.get('message', 'خطأ غير معروف')}",
                    reply_markup=support
                )
                return
            
            for user in data["users"]:
                username_user = user.get("username", "")
                full_name = user.get("full_name", "")
                pic_url = user.get("profile_pic_url", "")
                
                if page_type == 'followers':
                    followers_dict[username_user] = {"name": full_name, "pic": pic_url}
                else:
                    following_dict[username_user] = {"name": full_name, "pic": pic_url}
            
            if not data.get("has_more"):
                break
            max_id = data.get("next_max_id")
            time.sleep(0.5)
    
    s.close()
    
    if len(following_dict) == 0:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=edit_msg_id,
            text="❌ لم يتم العثور على متابعين/متابَعين. تأكد من أن الحساب عام!",
            reply_markup=support
        )
        return
    
    for username_user in following_dict:
        if username_user not in followers_dict:
            despicable_dict[username_user] = following_dict[username_user]
    
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=edit_msg_id,
        text=f"""✅ تم جلب المستخدمين غير المتابعين بنجاح!

📊 العدد: <code>{len(despicable_dict)}</code>

📌 ملاحظة: قد تجد أشخاصاً يتابعونك ولكن لا يظهرون بسبب إعدادات الخصوصية.
🛑 استخدم زر "إيقاف الإرسال" لإيقاف العملية في أي وقت.
""",
        reply_markup=stop_keyboard
    )
    
    for username_user, info in despicable_dict.items():
        if user_id in stopped_users:
            bot.send_message(chat_id=user_id, text="🛑 تم إيقاف العملية بناءً على طلبك.")
            break
        
        name = info.get("name", "")
        pic = info.get("pic", "")
        profile_url = f"https://www.instagram.com/{username_user}/"
        
        caption = f"""🚫 هذا المستخدم لا يتابعك!

👤 <b>اليوزر:</b> <code>@{username_user}</code>
📝 <b>الاسم:</b> {name}
"""
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="🔗 فتح الحساب", url=profile_url,style="danger"))
        
        try:
            if pic:
                bot.send_photo(chat_id=user_id, caption=caption, photo=pic, parse_mode="HTML", reply_markup=keyboard)
            else:
                bot.send_message(chat_id=user_id, text=caption, parse_mode="HTML", reply_markup=keyboard)
        except Exception as e:
            print("ERROR sending:", e)
        
        time.sleep(1)
    
    stopped_users.discard(user_id)
    bot.send_message(chat_id=user_id, text="✅ اكتملت العملية بنجاح!")

bot.remove_webhook()
time.sleep(1)
print("Polling...")
bot.infinity_polling(timeout=10, long_polling_timeout=5, skip_pending=True)
