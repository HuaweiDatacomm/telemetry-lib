#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能：message信息相关操作，主要是解码与编码
修改记录：2022-11-28 hwx1045592 创建
"""

from proto_py import huawei_telemetry_pb2, huawei_debug_pb2

class Message(object):
    def __init__(self, message: bytes):
        # 待解析message信息，gpb编码的bytes类型
        self.message = message
        # 订阅路径，用于解析data_gpb内部数据
        self.sensor_path = None
        # 内部数据解析对象，跟订阅路径对应
        self.innerParser = None

    # 解析message数据
    def decode(self):
        try:
            # 第一层数据
            info = huawei_telemetry_pb2.Telemetry.FromString(self.message)
            self.sensor_path = info.sensor_path
            self.getInnerParse()
            innerList = []
            for r in info.data_gpb.row:
                innerList.append(self.innerParser.FromString(r.content))
            return info, innerList
        except Exception as e:
            errorMsg = f"dialin error, exception: {e}"
            return errorMsg

    # 根据订阅路径获取内部解析对象
    def getInnerParse(self):
        if 'debug' in self.sensor_path:
            self.innerParser = huawei_debug_pb2.Debug
        elif 'devm' in self.sensor_path:
            self.innerParser = huawei_debug_pb2.Debug
        else:
            self.innerParser = None

