# This Code Is Under GNU General Public License v3.0
# Read More Here: https://github.com/XolvaID/iptools-bot/blob/main/LICENSE

"""
GitHub: github.com/xolvaid
Partner: github.com/kgyya
"""
from telethon import TelegramClient, events
import re,json,requests,json,socket,os
from requests.exceptions import ReadTimeout, Timeout, ConnectionError
from bs4 import BeautifulSoup as bs
api_id = os.getenv("API_ID") # get api_id
api_hash = os.getenv("API_HASH") # get api_hash
bot_token = os.getenv("BOT_TOKEN") # get bot_token
ses = requests.Session()
bot = TelegramClient('bot',api_id,api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern="/start"))
async def xx_(event):
        await event.reply("""**Menu Commands & Syntax:
==============================
/httpheader
- Check HTTP Header
==============================
/httpproxy
- Check HTTP Proxy Status & Information
==============================
/subnet
- Subnet Mask Lookup
==============================
/hosttoip
- Convert Host To IP
==============================
/iptohost
- Convert IP To Host
==============================
/port
- Check Open Port
==============================
/cf
- Check Cloudflare Host
==============================
/whois
- Check IP/Host Information
==============================
/subdomain
- Scan Subdomain
==============================
/help
- Show This Message
==============================
Author: @xolvaid
GitHub: github.com/xolvaid
Repo  : github.com/xolvaid/iptools-bot**
==============================
**NEW BIG UPDATE CUMMING SOON!**""")


@bot.on(events.NewMessage(pattern="/help"))
async def xx_(event):
	await event.reply("""**Menu Commands & Syntax:
==============================
/httpheader
- Check HTTP Header
==============================
/httpproxy
- Check HTTP Proxy Status & Information
==============================
/subnet
- Subnet Mask Lookup
==============================
/hosttoip
- Convert Host To IP
==============================
/iptohost
- Convert IP To Host
==============================
/port
- Check Open Port
==============================
/cf
- Check Cloudflare Host
==============================
/whois
- Check IP/Host Information
==============================
/subdomain
- Scan Subdomain
==============================
/help
- Show This Message
==============================
Author: @xolvaid
GitHub: github.com/xolvaid
Repo  : github.com/xolvaid/iptools-bot**
==============================
**NEW BIG UPDATE CUMMING SOON!**""")

@bot.on(events.NewMessage(pattern=r"/httpheader"))
async def xn_x(event):
	async with bot.conversation(event.chat_id) as new:
		await event.reply("**Enter Hostname/IP: **")
		host = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		host = await host
		host = host.message.message
		r = requests.get("https://api.hackertarget.com/httpheaders/?q="+host)
		await event.reply("**==============================\n"+r.text+"==============================**")

@bot.on(events.NewMessage(pattern=r"/subnet"))
async def xnxx(event):
	async with bot.conversation(event.chat_id) as new:
		await event.reply("""**Masukkan IP
Contoh Untuk IPv4:** ```176.694.20/24```

**Contoh Untuk IPv6:** ```2001:db8::/32```""")
		ip = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		ip = await ip
		ip = ip.message.message
		r = requests.get("https://api.hackertarget.com/subnetcalc/?q="+ip)
		ip = "==============================**\n"+r.text.replace("=",":")+"**=============================="
		await event.reply(ip)
@bot.on(events.NewMessage(pattern=r"/httpproxy"))
async def x_x(event):
	async with bot.conversation(event.chat_id) as new:
		await event.reply("**Enter HTTP Proxy: (example: 172.6.9.420:8080)**")
		proxy = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		proxy = await proxy
		proxy = proxy.message.message.replace("http://","").replace("https://","")
		try:
			requests.get("http://example.com",proxies={"http":"http://"+proxy},timeout=0.7)
		except IOError:
			await event.reply("**HTTP Proxy "+proxy+" Is Dead**")
		else:
			reproxy = re.search("(.*?):",proxy).group(1)
			r = requests.get("http://ip-api.com/json/"+reproxy)
			js = json.loads(r.text)
			rr = requests.get("http://"+proxy)
			print(js)
			await event.reply(f"""**==============================
PROXY       : {proxy}
STATUS      : Alive
SERVER      : {rr.headers['Server']}
ISP         : {js['isp']}
STATUS CODE : {rr.status_code}
COUNTRY     : {js['country']}
CITY        : {js['city']}
CONTENT-TYPE: {rr.headers['Content-Type']}
DATE        : {rr.headers['Date']}
==============================**""")


@bot.on(events.NewMessage(pattern=r"/port"))
async def x__(event):
	await event.reply("**Enter IP Or Hostname: **")
	async with bot.conversation(event.chat_id) as new:
		ip = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		ip = await ip
		ip = ip.message.message
		await event.reply("**Enter Port: **")
		port = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		port = await port
		port = port.message.message
		ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		inf = (str(ip), int(port))
		status = ssocket.connect_ex(inf)
		if status == 0:
			status = "Open"
		else:
			status = "Closed"
		await event.reply(f"""**===============================
IP/HOST    : {ip}
PORT       : {str(port)}
STATUS     : {status}
===============================**""")


@bot.on(events.NewMessage(pattern=r"/cf"))
async def x_(event):
	result_success = []
	async with bot.conversation(event.chat_id) as new:
		await event.reply("**Enter Hostname: **")
		ip = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		ip = await ip
		ip = ip.message.message
		raw_subd = requests.get("https://api.hackertarget.com/hostsearch/?q="+ip)
		subd = re.findall("(.*?),",raw_subd.text)
		for sub in subd:
			try:
				r = requests.get("http://"+sub,headers={"Host":"id-public1.sshws.net","Upgrade":"websocket"},timeout=0.7)
				if r.status_code == 101:
					await event.reply(f"""
**===============================
IP/HOST     : {sub}
SERVER      : {r.headers['Server']}
STATUS CODE : {r.status_code}
STATUS      : POINTED TO CF / CLOUDFLARE
===============================**""")
					result_success.append(str(sub))
				elif r.status_code != 101:
					await event.reply(f"""
**===============================
IP/HOST     : {sub}
SERVER      : {r.headers['Server']}
STATUS CODE : {r.status_code}
STATUS      : NOT POINTED TO CF / CLOUDFLARE
===============================**""")
			except (Timeout, ReadTimeout, ConnectionError):
				await event.reply(f"""
**===============================
IP/HOST     : {sub}
SERVER      : {r.headers['Server']}
STATUS CODE : {r.status_code}
STATUS      : NOT POINTED TO CF / CLOUDFLARE
===============================**""")
		for result in result_success:
			with open(f"{ip}.txt","a") as (s):
				s.write(result+"\n")
			await bot.send_file(event.chat_id,f"{ip}.txt",caption=f"**Total Cloudflare Host Scanned: {str(len(result_success))}**",reply_to=event.id)


@bot.on(events.NewMessage(pattern=r"/whois"))
async def x(event):
	async with bot.conversation(event.chat_id) as new:
		await event.reply("**Enter IP Or Hostname: **")
		ip = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		ip = await ip
		ip = ip.message.message.replace("https://","").replace("http://","")
		r = requests.get("http://ip-api.com/json/"+ip)
		js = json.loads(r.text)
		rr = requests.get("http://"+ip)
		await event.reply(f"""**===============================
IP          : {ip}
SERVER      : {rr.headers['Server']}
ISP         : {js['isp']}
STATUS CODE : {rr.status_code}
COUNTRY     : {js['country']}
CONTENT-TYPE: {rr.headers['Content-Type']}
DATE        : {rr.headers['Date']}
==============================**""")

@bot.on(events.NewMessage(pattern=r"/iptohost"))
async def _(event):
	async with bot.conversation(event.chat_id) as new:
		await event.reply("**Enter IP: **")
		ip = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		ip = await ip
		ip = ip.message.message
		reverse = ses.get("https://api.hackertarget.com/reverseiplookup/?q="+ip)
		if reverse.text != "error check your search parameter":
				await event.reply("**Host For "+ip+" Is "+reverse.text+"**")

@bot.on(events.NewMessage(pattern=r"/hosttoip"))
async def __(event):
	async with bot.conversation(event.chat_id) as new:
		await event.reply("**Enter Hostname: **")
		host = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		host = await host
		host = host.message.message
		r = ses.get(f"http://ip-api.com/json/{host}").text
		JsonMenu2 = json.loads(r)
		await event.reply("**IP Address For "+host+f" Is "+JsonMenu2["query"]+"**")

@bot.on(events.NewMessage(pattern=r"/subdomain"))
async def ___(event):
	async with bot.conversation(event.chat_id) as new:
		await event.reply("**Enter Hostname: **")
		ip = new.wait_event(events.NewMessage(incoming=True, from_users=event.chat_id))
		ip = await ip
		ip = ip.message.message
		r = ses.get("https://api.hackertarget.com/hostsearch/?q="+ip)
		host = re.findall("(.*?),",r.text)
		for subd in host:
			with open(f"{ip}.txt","a") as (s):
				s.write(str(subd)+"\n")
		await bot.send_file(event.chat_id,f"{ip}.txt",caption=f"**Total Subdomain Scanned: {str(len(host))}**",reply_to=event.id)

bot.start()
bot.run_until_disconnected()
