#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples/webhook_examples

import logging
import ssl
from aiohttp import web
import telebot
import asyncio

API_TOKEN = '94106868:AAGNHwQpHiwnwVTaZo0AqzQB_IwGLhQMkyQ'

WEBHOOK_HOST = 'scriptlab.net'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = web.Application()

# Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Examples:\n"
                  "/group\n"
                  "/user"))

# Handle '/user'
@bot.message_handler(commands=['user'])
def send_user(message):
            bot.reply_to(message,   str(message.from_user.id) )	
	
# Handle '/group'
@bot.message_handler(commands=['group'])
def send_user(message):
            bot.reply_to(message,   str(message.chat.id) )

async def get_relay_text(request):
	print('relay_text')
	return web.Response(
		text='ok',
		content_type="text/html")

app.router.add_post('/{token}/', handle)
app.router.add_route('GET', '/relay_text', get_relay_text)

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Build ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

#wakeup log
bot.send_message('106129214', 'Bot online!')

# Start aiohttp server
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)

'''
loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, port=WEBHOOK_PORT, ssl=context)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("serving off...")
finally:
    loop.run_until_complete(handler.finish_connections(1.0))
    srv.close()
'''