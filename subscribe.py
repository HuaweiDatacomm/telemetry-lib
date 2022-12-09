#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能：生产数据类，该类主要用于从路由器采集数据，包括dialin(Subscribe)和dialout(DataPublish)
修改记录：2022-11-17 hwx1045592 创建
"""
import grpc

from proto_py import huawei_grpc_dialin_pb2_grpc, huawei_grpc_dialin_pb2, huawei_grpc_dialout_pb2_grpc

class Subscribe(object):
    """Subscribe dialin rpc method."""
    def __init__(self,
                 username = None,
                 password = None,
                 address = None,
                 paths = None,
                 sample_interval = 1000,
                 request_id = 3):
        # 基础信息
        self.username = username
        self.password = password
        self.address = address
        # 订阅状态，暂无实际意义
        self.status = False

        self.request_id = request_id

        # 订阅ID，用于取消订阅，订阅成功后会回写
        self.subscription_id = None
        self.metadata = Subscribe.generate_metadata(username, password)
        self.sub_req = self.generate_subArgs(paths, request_id, sample_interval)
        self.stub = Subscribe.getStub(address)

    # 动态订阅
    def dailin(self):
        try:
            data = None
            # 开始订阅
            sub_resps = self.stub.Subscribe(self.sub_req, metadata=self.metadata)
            for sub_resp in sub_resps:
                data_is_valid = Subscribe.check_sub_reply_is_data(sub_resp)  # 检查是否为数据
                if data_is_valid is False:
                    # 第一条数据，返回ok
                    self.status = True
                else:
                    data = sub_resp
                    cancel_res = Subscribe.Cancel(self.username, self.password, self.address, self.request_id, sub_resp.subscription_id)
                    if cancel_res == 'success':
                        break
            # print(data, 333)
            return data
        except Exception as e:
            print("dialin error, exception {0}".format(e))

    # 检查 dialin reply 是否为正常数据
    @staticmethod
    def check_sub_reply_is_data(sub_resp):
        resp_code = sub_resp.response_code
        if (resp_code == ""):
            return True
        if (resp_code == "200"):
            return False
        if (resp_code != "200" and resp_code != ""):
            return False
        if (sub_resp.message == "ok"):
            return False

    # 生成元数据
    @staticmethod
    def generate_metadata(username, password):
        metadata = tuple([('username', username), ('password', password)])
        return metadata

    # 生成订阅grpc连接参数
    def generate_subArgs(self, paths, request_id, sample_interval):
        sub_req = huawei_grpc_dialin_pb2.SubsArgs()
        for path in paths:
            sub_path = huawei_grpc_dialin_pb2.Path(path=path['path'], depth=path['depth'])
            sub_req.path.append(sub_path)
        sub_req.encoding = 0  # 固定值0:gpb编码
        sub_req.request_id = request_id
        sub_req.sample_interval = sample_interval
        return sub_req

    # 生成取消订阅连接参数
    @staticmethod
    def generate_canArgs(request_id, subscription_id):
        cancel_req = huawei_grpc_dialin_pb2.CancelArgs()
        cancel_req.request_id = request_id
        cancel_req.subscription_id = subscription_id
        return cancel_req

    # 生成stub对象，用于订阅或取消订阅
    @staticmethod
    def getStub(dialin_server):
        # 新建grpc客户端，建立grpc连接
        server = dialin_server
        channel = grpc.insecure_channel(server)
        stub = huawei_grpc_dialin_pb2_grpc.gRPCConfigOperStub(channel)
        return stub


    # 取消订阅，因可以外部调用，故设置成静态方法
    @staticmethod
    def Cancel(username, password, address, request_id, subscription_id):
        metadata = Subscribe.generate_metadata(username, password)
        cancel_req = Subscribe.generate_canArgs(request_id, subscription_id)
        stub = Subscribe.getStub(address)
        res = stub.Cancel(cancel_req, metadata=metadata)
        if res.response_code == '200':
            return 'success'
        else:
            return 'fail'