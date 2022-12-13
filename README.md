# **telemetry-lib**

## **Overview**
Some lib interfaces about huawei telemetry operations for Python Developers.

## **Installation**
### **Prerequisites**
1. Python version needs greater than **3.7** and the latest module **grpc**.
- Python: 3.7+
- gprc: `pip install grpcio`
2. copy some files to your working dependency folder, sometimes **lib**.
- `subscribe.py`
- `message.py`
- all files in the folder `proto_py`

## **Hot to use**
### 一、Subscribe dailin (动态订阅)
1. import related classes:
   ```
   from subscribe import Subscribe
   ```
2. get instance and call corresponding method:   
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

   | name     | type   | required(必填) | default(默认值) | description(描述)  |
   |----------|--------|--------------|--------------|:----------|
   | username | string | yes          | None         | 用户名                           |
   | password | string | yes          | None         | 密码                            |
   | address  | string | yes          | None         | 订阅设备地址                        |
   | paths  | list   | yes          | None         | 一个列表，元素是包含path和depth的字典，见以上示例 |
   | sample_interval  | int    | no      | 1000     | 采用时间间隔，单位：毫秒 |
   | request_id  | int    | no           | 3            | 订阅ID                          |
   
   returns:  
   an object(instanceof SubsReply) which contains some attributes below.
   
   | name | desc      | example |
   | ---  |-----------| ---------- |
   | subscription_id | 订阅ID      | 33306  |
   | request_id | 请求ID      | 3      |
   | message | 报文实体，bytes类型 |   /   |

### 二、Decode Message(解析信息实体Message)
1. import related classes:
   ```
   from message import Message
   ```
2. init Message and call decode method:   
   Examples: 
   ```
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

   | name     | type   | required(必填) | default(默认值) | description(描述)   |
   |----------|--------|--------------|--------------|:---------------------|
   | message | bytes  | yes          | None         | 报文实体Message          |
   
   returns:  
   an tuple (info, list) below.
   
   | name | desc             | example               |
   | ---  |------------------|-----------------------|
   | info | Telemetry信息的基本信息 | `Telemetry`           |
   | list | 订阅具体数据           | some special info |

   
