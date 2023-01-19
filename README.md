# **telemetry-lib**

## **Overview**
Some lib interfaces about huawei telemetry operations for Python Developers.

## **Prerequisites**
- Python: 3.7+
- Module: grpc ( by `pip install grpcio`)

## **Showcase**
Run the `main.py` script, like
```
python main.py -t subscribe/decode
```
`-t` option stands for ultility type, two main values, subscribe and decode.   
The former is by default.

## **How to use**
### Before use
Copy some files to your dependency package folder, sometimes **lib**.
- `subscribe.py` for dynamic subscribe
- `message.py` for decode message
- all files in the folder `proto_py`

### I. Dynamic Subscribe
1. import related class in your main file:
   ```
   from subscribe import Subscribe
   ```
2. Initialize the `Subscribe` class and call the `dailin` method:   
   Examples: 
   ```
   paths = [
        {
            "path": "huawei-debug:debug/cpu-infos/cpu-info",
            "depth": 1
        }
   ]
   subs = Subscribe(username='XXX', password='XXX', address="XXX", paths=paths)
   res = subs.dailin()
   ```
   parameters:

   | name            | type   | required | default | description  |
   |-------------|----------|--------------|--------------|----------|
   | username        | string | yes      | None     | username                           |
   | password        | string | yes      | None    | password                           |
   | address         | string | yes      | None   | ip:port of device                |
   | paths    | list   | yes      | None | The element is a dictionary that contains `path` and `depth`. |
   | sample_interval | int    | no       | 1000     | Sample interval, in milliseconds. |
   | request_id      | int    | no       | 3      | request_id                          |
   
   return:  
   an object(instanceof class `SubsReply`) which contains some attributes below.
   
   | name            | description                      | example     |
   |----------------------------------|-------------| ---------- |
   | subscription_id | subscription_id                  | 33306       |
   | request_id      | request_id                       | 3           |
   | message         | message entities，type of bytes | /           |



### II. Decode Message
1. Import related class:
   ```
   from message import Message
   ```
2. Initialize Message and call `decode` method:   
   Examples: 
   ```python
   msg = Message(res.message)
   info, list = msg.decode()
   
   # info, telemetry object contains basic info
   node_id_str: "PE2"
   subscription_id_str: "_dyn_grpc_b6_8220"
   sensor_path: "huawei-debug:debug/cpu-infos/cpu-info"
   collection_id: 1
   collection_start_time: 1670922576043
   msg_timestamp: 1670922576083
   data_gpb {
     row {
       timestamp: 1670922576080
       content: "\n7\n5\n\0019\020Z\030K \010(\201\200\244\0100\03680@\nJ\0230000-00-00 00:00:00R\nUnoverload"
     }
     row {
       timestamp: 1670922576080
       content: "\n8\n6\n\00210\020Z\030K \010(\201\200\250\0100\01680@\nJ\0230000-00-00 00:00:00R\nUnoverload"
     }
   }
   collection_end_time: 1670922576083
   current_period: 1000
   
   # list 
   cpu_infos {
     cpu_info {
       position: "9"
       overload_threshold: 90
       unoverload_threshold: 75
       interval: 8
       index: 17367041
       system_cpu_usage: 30
       monitor_number: 48
       monitor_cycle: 10
       overload_state_change_time: "0000-00-00 00:00:00"
       current_overload_state: "Unoverload"
     }
   }
   ```
   parameters:

   | name     | type   | required | default | description      |
   |----------|--------|--------------|------------------|:---------------------|
   | message | bytes  | yes          | None         | message entities |
   
   return:  
   a tuple (info, list) below.
   
   | name | desc                                 | example     |
   |--------------------------------------|-------------|-----------------------|
   | info | basic infomation of Telemetry | `Telemetry` |
   | list | some special info                               | /           |

   
