# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
功能：telemetry 动态订阅示例
修改记录：2023-2-20 hwx1045592 创建
"""
import grpc
from proto_py import huawei_grpc_dialin_pb2, huawei_grpc_dialin_pb2_grpc
from parser import config_parser, telemetry_parser


class DialinClient:

    def __init__(self):
        self.config = config_parser.ConfigJson()
        self.config.parse_config()

    ## 创建订阅参数
    def create_subsargs(self):

        subsargs = huawei_grpc_dialin_pb2.SubsArgs()
        subsargs.request_id = self.config.request_id
        subsargs.encoding = self.config.encoding
        for p in self.config.paths:
            subsargs.path.append(huawei_grpc_dialin_pb2.Path(path = p))
        subsargs.sample_interval = self.config.sample_interval

        return subsargs

    # 创建元数据
    def generate_metadata(self, username, password):
        metadata = tuple([('username', username), ('password', password)])
        return metadata

    def subscribe(self):
        subsargs = self.create_subsargs()
        metadata = self.generate_metadata(self.config.username, self.config.password)
        channel = grpc.insecure_channel(self.config.ip + ':' + self.config.port)  # 服务器信息
        stub = huawei_grpc_dialin_pb2_grpc.gRPCConfigOperStub(channel)  # 客户端建立连接
        sub_resps = stub.Subscribe(request=subsargs, metadata=metadata)

        for sub_resp in sub_resps:
            if sub_resp.response_code == "200":
                print("Subscribe Success!")
            if sub_resp.response_code != "200":
                # print(subs_reply.message)
                tel = telemetry_parser.TelemetryParser(sub_resp.message)
                res = tel.decode()
                # break
                for sample_data in res['sample_data']:
                    print(sample_data)


if __name__ == '__main__':

    client = DialinClient()
    client.subscribe()