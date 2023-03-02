#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
功能：telemetry 静态订阅示例
修改记录：2023-2-20 hwx1045592 创建
"""
import grpc
import time
from concurrent import futures
import sys

from proto_py import huawei_grpc_dialout_pb2_grpc
from parser import telemetry_parser

_ONE_DAY_IN_SECONDS = 60*60*24
_HOST = '10.134.205.68'
_PORT = '10001'


class DialoutServicer(huawei_grpc_dialout_pb2_grpc.gRPCDataserviceServicer):

    def dataPublish(self, request_iterator, context):
        for req in request_iterator:
            tel = telemetry_parser.TelemetryParser(req.data)
            sample_data = tel.decode()
            for data in sample_data:
                print(data)

class DialoutServer:

    def __init__(self, host, port):
        try:
            self.grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # 最多有多少work并行执行
            self.grpcServer.add_insecure_port(host + ':' + port)  # 建立服务器和端口
        except RuntimeError as e:
            error_str = "Failed to bind to address " + str(host) + ":" + str(port)
            sys.exit(1)

    def run(self):
        huawei_grpc_dialout_pb2_grpc.add_gRPCDataserviceServicer_to_server(DialoutServicer(),
                                                                           self.grpcServer)  # 添加函数方法和服务器

        self.grpcServer.start()  # 启动服务器
        self.grpcServer.wait_for_termination()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.grpcServer.stop(0)


if __name__ == '__main__':
    host = input("please input IP: ")
    port = input("please input PORT: ")
    server = DialoutServer(_HOST, _PORT)

    server.run()
    input("please input any key to exit")
