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
    "company_name": "南华",
    "type_option_combox": ["认抛止盈", "认购存档"],
    "main_lineEdit_widget": {"行权价": "main_strike_price_lineEdit", "向下止盈": "main_down_target_profit_lineEdit",
                             "向上止盈": "main_up_target_profit_lineEdit"},
    "second_lineEdit_widget": {"行权价": "second_strike_price_lineEdit", "向下止盈": "second_down_target_profit_lineEdit"},
    "time_widget": {"可行权前一日": "before_exercise_dateEdit"},
    "control_module_page_label":{
        "交易书编号": "transaction_number_label",
        "客户名称": "customer_name_label",
        "合约代码": "contract_code_label",
        "期权类型": "option_type_label",
        "每手份数": "number_per_hand_label",
        "状态": "state_label",
        "系统编号":"system_number_label",
        "销售总价": "total_price_label",
        "手数": "lots_label",
        "单价": "unit_price_label",
        "主行权价": "main_strike_price_label",
        "主行权日": "main_exercise_date_label",
        "次行权价": "second_strike_price_label",
        "次行权日": "second_exercise_date_label"

    },
    "tableWidget": {
        "on_way_for_guest_tableWidget": {"交易书编号": "transaction_number", "客户名称": "customer_name",
                                         "合约代码": "contract_code",
                                         "期权类型": "option_type", "销售总价": "total_price", "销售单价": "unit_price",
                                         "手数": "lots",
                                         "每手份数": "number_per_hand", "系统单号": "system_number",
                                         "主行权价": "main_strike_price", "主行权日": "main_exercise_date",
                                         "次行权价": "second_strike_price", "次行权日": "second_exercise_date"},
        "today_close_for_guest_tableWidget": {"交易书编号": "transaction_number", "客户名称": "customer_name",
                                              "合约代码": "contract_code",
                                              "期权类型": "option_type", "销售总价": "total_price", "销售单价": "unit_price",
                                              "手数": "lots",
                                              "每手份数": "number_per_hand", "系统单号": "system_number",
                                              "主行权价": "main_strike_price", "主行权日": "main_exercise_date",
                                              "次行权价": "second_strike_price", "次行权日": "second_exercise_date"},
        "on_way_for_company_tableWidget": {"交易书编号": "transaction_number", "客户名称": "customer_name",
                                           "合约代码": "contract_code",
                                           "期权类型": "option_type", "销售总价": "total_price", "销售单价": "unit_price",
                                           "手数": "lots",
                                           "每手份数": "number_per_hand", "系统单号": "system_number",
                                           "主行权价": "main_strike_price", "主行权日": "main_exercise_date",
                                           "次行权价": "second_strike_price", "次行权日": "second_exercise_date"},
        "today_open_for_company_tableWidget": {"交易书编号": "transaction_number", "客户名称": "customer_name",
                                               "合约代码": "contract_code",
                                               "期权类型": "option_type", "销售总价": "total_price", "销售单价": "unit_price",
                                               "手数": "lots",
                                               "每手份数": "number_per_hand", "系统单号": "system_number",
                                               "主行权价": "main_strike_price", "主行权日": "main_exercise_date",
                                               "次行权价": "second_strike_price", "次行权日": "second_exercise_date"},
        "today_close_for_company_tableWidget": {"交易书编号": "transaction_number", "客户名称": "customer_name",
                                                "合约代码": "contract_code",
                                                "期权类型": "option_type", "销售总价": "total_price", "销售单价": "unit_price",
                                                "手数": "lots",
                                                "每手份数": "number_per_hand",
                                                "系统单号": "system_number",
                                                "主行权价": "main_strike_price", "主行权日": "main_exercise_date",
                                                "次行权价": "second_strike_price", "次行权日": "second_exercise_date"},
        "today_open_for_guest_tableWidget": {"交易书编号": "transaction_number", "客户名称": "customer_name",
                                             "合约代码": "contract_code",
                                             "期权类型": "option_type", "销售总价": "total_price", "销售单价": "unit_price",
                                             "手数": "lots",
                                             "每手份数": "number_per_hand", "系统单号": "system_number",
                                             "主行权价": "main_strike_price", "主行权日": "main_exercise_date",
                                             "次行权价": "second_strike_price", "次行权日": "second_exercise_date"},
    }
})
option_infomation = json.dumps({
    "purpose": "option_table_info",
    "table_data": {
        "transaction_number": "S79426", "customer_name": "壹号土猪",
        "contract_code": "M1901",
        "option_type": "M1901", "total_price": 4640000, "unit_price": 46,
        "lots": 1000,
        "number_per_hand": 10, "system_number": "1809045",
        "main_strike_price": 659, "main_exercise_date": 1539273600.0,
        "second_strike_price": 7320, "second_exercise_date": 1539273600.0,
    },
    "state": "对客在途"
})
option_infomation1 = json.dumps({
    "purpose": "option_table_info",
    "table_data": {
        "transaction_number": "S79426", "customer_name": "壹号土猪",
        "contract_code": "M1901",
        "option_type": "M1901", "total_price": 4640000, "unit_price": 46,
        "lots": 1000,
        "number_per_hand": 10, "system_number": "1809045",
        "main_strike_price": 659, "main_exercise_date": 1539273600.0,
        "second_strike_price": 7320, "second_exercise_date": 1539273600.0
    },
    "state": "对公在途"
})
option_infomation2 = json.dumps({
    "purpose": "option_table_info",
    "table_data": {
        "transaction_number": "S79426", "customer_name": "壹号土猪",
        "contract_code": "M1901",
        "option_type": "M1901", "total_price": 4640000, "unit_price": 46,
        "lots": 1000,
        "number_per_hand": 10, "system_number": "1809045",
        "main_strike_price": 659, "main_exercise_date": 1539273600.0,
        "second_strike_price": 7320, "second_exercise_date": 1539273600.0
    },
    "state": "对公今开"
})
option_infomation3 = json.dumps({
    "purpose": "option_table_info",
    "table_data": {
        "transaction_number": "S79426", "customer_name": "壹号土猪",
        "contract_code": "M1901",
        "option_type": "M1901", "total_price": 4640000, "unit_price": 46,
        "lots": 1000,
        "number_per_hand": 10, "system_number": "1809045",
        "main_strike_price": 659, "main_exercise_date": 1539273600.0,
        "second_strike_price": 7320, "second_exercise_date": 1539273600.0
    },
    "state": "对客今开"
})
option_infomation4 = json.dumps({
    "purpose": "option_table_info",
    "table_data": {
        "transaction_number": "S79426", "customer_name": "壹号土猪",
        "contract_code": "M1901",
        "option_type": "M1901", "total_price": 4640000, "unit_price": 46,
        "lots": 1000,
        "number_per_hand": 10, "system_number": "1809045",
        "main_strike_price": 659, "main_exercise_date": 1539273600.0,
        "second_strike_price": 7320, "second_exercise_date": 1539273600.0
    },
    "state": "对公今止"
})
option_infomation5 = json.dumps({
    "purpose": "option_table_info",
    "table_data": {
        "transaction_number": "S79426", "customer_name": "壹号土猪",
        "contract_code": "M1901",
        "option_type": "M1901", "total_price": 4640000, "unit_price": 46,
        "lots": 1000,
        "number_per_hand": 10, "system_number": "1809045",
        "main_strike_price": 659, "main_exercise_date": 1539273600.0,
        "second_strike_price": 7320, "second_exercise_date": 1539273600.0
    },
    "state": "对客今止"
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
        for i in range(4):
            await websocket.send(option_infomation)
            await websocket.send(option_infomation1)
            await websocket.send(option_infomation2)
            await websocket.send(option_infomation3)
            await websocket.send(option_infomation4)
            await websocket.send(option_infomation5)


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
