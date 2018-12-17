#!/usr/bin/env python

# WSS (WS over TLS) client example, with a self-signed certificate

import asyncio
import json
import pathlib
import ssl
import websockets

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(
    pathlib.Path(__file__).with_name('localhost.pem'))

        '''ws://39.96.20.147/ws/OptionsFuturesTradingPlatform/ll/'''
async def hello():
    async with websockets.connect(
            'ws://39.96.20.147:8000/ws/') as websocket:
        # hedecho
        print(websocket)
        print(websockets)
        await websocket.send(json.dumps({"purpose": "login_request", "client_type": "transaction", "user_name": "tom",
                                         "password": "e10adc3949ba59abbe56e057f20f883e"}))

        greeting = await websocket.recv()
        print(f"< {greeting}")
        print(json.loads(greeting))


#
async def hello2():
    async with websockets.connect(
            'ws://192.168.0.112:8888/hedecho') as websocket:
        # hedecho
        print(websocket)
        await websocket.send(json.dumps({"test": None}))

        greeting = await websocket.recv()
        print(f"< {greeting}")
        print(json.loads(greeting))


asyncio.get_event_loop().run_until_complete(hello())
# asyncio.get_event_loop().run_until_complete(hello2())
# import asyncio
# import datetime
# import random
# import websockets
#
# async def time(websocket, path):
#     while True:
#         now = datetime.datetime.utcnow().isoformat() + 'Z'
#         await websocket.send(now)
#         await asyncio.sleep(random.random() * 3)
#
# start_server = websockets.serve(time, '127.0.0.1', 5678)

# asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
