#!/usr/bin/env python
# WSS (WS over TLS) server example, with a self-signed certificate
import asyncio
import json
import pathlib
import ssl
import time

import websockets
option_table_info = json.dumps ({
    "purpose": "option_table_info",
    "header": ["交易书编号", "期权类型","客户名称", "期货合约代码", "手数", "每手份数","销售单价", "销售总价", "系统单号", "主行权价", "主行权日", "辅行权价", "辅行权日","可否转换"],
    "table_data": {
        "对客在途": [
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],0],
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],1],
        ],
        "对客今开": [
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],0],
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],1],
        ],
        "对客今止": [
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],1],
            ["S79426","认购止盈", "壹号土猪", "M1901", 1000,10, 46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],0],
        ],
        "对公在途": [
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],1],
            ["S79426","认购止盈", "壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],0],
        ],
        "对公今开": [
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000,10, 46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],1],
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],0],
        ],
        "对公今止": [
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000, 10,46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],1],
            ["S79426", "认购止盈","壹号土猪", "M1901", 1000,10, 46.4, 464000.0, "1809045", "650", 2539273600.0, [1238, 125, 123, 412],
             [2323145125, 2323145125, 2323145125],0],
        ]
    }
})
update_online_users = json.dumps({

    "online_users": ["sam_南华_Transaction", "tom_南华_Transaction", "张帆_国泰君安_Hedge", "李四_国泰君安_Transaction"],

    "purpose": "users_info_update"

})
login_success = json.dumps({
    "purpose": "login_success",
    "userid": "zhangfan_Hedge",
    "company_name":"南华",
    "pre_rate": {
        "平均":0.2,
        "存档":0.3,
        "止盈":0.2,
    },
    "option_type":{
        "认抛平均":{
            "price_type":["行权价"],
            "time_type":[],
        },
        "认购平均":{
            "price_type":['行权价'],
            "time_type":[],

        },
        "认抛存档":{
            "price_type": ['行权价'],
            "time_type": [],

        },
        "认购存档":{
            "price_type": ['行权价'],
            "time_type": [],

        },
        "认抛止盈":{
            "price_type": ['行权价',"向下止盈"],
            "time_type": ["可行权前一日","可行权后一日"],

        },
        "认购止盈":{
            "price_type": ['行权价'],
            "time_type": ["可行权前一日","可行权后一日"],

        }

    },
    "opt_info":{
        "123":{
            "opt_code":"123",
            "min_deal":10,
            "num_one_hand":5,
            "max_main_num":150,
            "max_sub_num":100
        },
        "456":{
            "opt_code":"456",
            "min_deal": 10,
            "num_one_hand": 5,
            "max_main_num": 150,
            "max_sub_num": 100
        }
    }
})
# opt_code ->品种代码
# min_del -> 最小销量
# num_one_hand -> 每手份数
# max_main_num -> 主单限量
# min_main_num -> 副单限量
# 123: {"opt_code": 123, 'min_deal': 10, 'num_one_hand': 5, 'max_main_num': 150, 'max_sub_num': 100}, }
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
        await websocket.send(option_table_info)

async def hello2(websocket, path):
    while True:
        print(websockets)
        receive_data = await websocket.recv()
        print(f"< {receive_data}")
        print(json.loads(receive_data))
        await websocket.send("123")


# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(
#     pathlib.Path(__file__).with_name('localhost.pem'))

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
