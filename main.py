#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能：telemetry lib接口，用于订阅、解析message等功能测试
修改记录：2022-11-17 hwx1045592 创建
"""
from subscribe import Subscribe
from message import Message
import argparse


if __name__ == "__main__":
    paths = [
        {
            "path": "huawei-debug:debug/cpu-infos/cpu-info",
            "depth": 1
        }
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', "--utility_type", dest='utility_type' ,default='subscribe',
                        help="utility_type, values contain subscribe or decode")
    args = parser.parse_args()

    utility_type = args.utility_type
    if utility_type == 'subscribe':
        subs = Subscribe(username='dublin123', password='Dublin@123', address="10.137.104.30:57401", paths=paths)
        res = subs.dailin()
        print(res)
    else:
        subs = Subscribe(username='dublin123', password='Dublin@123', address="10.137.104.30:57401", paths=paths)
        res = subs.dailin()
        msg = Message(res.message)
        info, list = msg.decode()
        # for i in list:
        #     print(i.cpu_infos.cpu_info[0].unoverload_threshold)
        print(info, list)
