# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from proto_py import huawei_grpc_dialout_pb2 as huawei__grpc__dialout__pb2


class gRPCDataserviceStub(object):
    """The service name is gRPCDataservice.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.dataPublish = channel.stream_stream(
                '/huawei_dialout.gRPCDataservice/dataPublish',
                request_serializer=huawei__grpc__dialout__pb2.serviceArgs.SerializeToString,
                response_deserializer=huawei__grpc__dialout__pb2.serviceArgs.FromString,
                )


class gRPCDataserviceServicer(object):
    """The service name is gRPCDataservice.
    """

    def dataPublish(self, request_iterator, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_gRPCDataserviceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'dataPublish': grpc.stream_stream_rpc_method_handler(
                    servicer.dataPublish,
                    request_deserializer=huawei__grpc__dialout__pb2.serviceArgs.FromString,
                    response_serializer=huawei__grpc__dialout__pb2.serviceArgs.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'huawei_dialout.gRPCDataservice', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class gRPCDataservice(object):
    """The service name is gRPCDataservice.
    """

    @staticmethod
    def dataPublish(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/huawei_dialout.gRPCDataservice/dataPublish',
            huawei__grpc__dialout__pb2.serviceArgs.SerializeToString,
            huawei__grpc__dialout__pb2.serviceArgs.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
