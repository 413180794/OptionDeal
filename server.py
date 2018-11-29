#!/usr/bin/env python
# WSS (WS over TLS) server example, with a self-signed certificate
import asyncio
import json
import pathlib
import ssl
import time

import websockets

update_online_users = json.dumps({

    "online_users": ["sam_南华_Transaction", "tom_南华_Transaction", "张帆_国泰君安_Hedge", "李四_国泰君安_Transaction"],

    "purpose": "users_info_update"

})
login_success = json.dumps({
    "purpose": "login_success",
    "userid": "zhangfan_Hedge",
    "company_name":"南华",
    "type_option_combox": ["认抛止盈", "认购存档"],
    "main_lineEdit_widget": {"行权价": "main_strike_price_lineEdit", "向下止盈": "main_down_target_profit_lineEdit","向上止盈":"main_up_target_profit_lineEdit"},
    "second_lineEdit_widget": {"行权价": "second_strike_price_lineEdit", "向下止盈": "second_down_target_profit_lineEdit"},
    "time_widget": {"可行权前一日": "before_exercise_dateEdit"},
    ""
})

login_failed = json.dumps(
    {
        "purpose": "login_failed",
        "failure_reason": "密码错误",
    }
)

opt_ess_info = json.dumps(
    {
        "purpose": "opt_ess_info",
        "fvcode": "asd",
        "detail": [
            {
                "contract_code": "J902",
                "lots": 899,
            },
            {
                "contract_code": "fff",
                "lots": 0,
            }
        ]
    }
)


async def hello(websocket, path):
    while True:
        print(websockets)
        print(path)
        receive_data = await websocket.recv()
        print(f"< {receive_data}")
        print(json.loads(receive_data))
        x = json.loads(receive_data)
        if x['purpose'] == "req_ess_info":
            await websocket.send(opt_ess_info)
        elif x['purpose'] == "login_request":
            await websocket.send(login_success)
            await websocket.send(update_online_users)


async def hello2(websocket, path):
    while True:
        print(websockets)
        receive_data = await websocket.recv()
        print(f"< {receive_data}")
        print(json.loads(receive_data))
        await websocket.send("123")


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    pathlib.Path(__file__).with_name('localhost.pem'))

start_server = websockets.serve(
    hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()

# import asyncio
# import websockets
#
# async def hello(websocket, path):
#     name = await websocket.recv()
#     print(f"< {name}")
#
#     greeting = f"Hello {name}!"
#
#     await websocket.send(greeting)
#     print(f"> {greeting}")
#
# start_server = websockets.serve(hello, 'localhost', 8765)
#
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
