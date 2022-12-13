# **telemetry-lib**

## **Overview**
Some lib interfaces about huawei telemetry operations for Python Developers.

## **Installation**
### **Prerequisites**
1. Python version needs greater than **3.7** and the latest module **grpc**.
- Python: 3.7+
- gprc: `pip install grpcio`
2. copy some files to your working dependency folder, sometimes **lib**.
- subscribe.py
- message.py
- all files in the folder `proto_py`
3. import related classes in your header of main file:
   ```
   from subscribe import Subscribe
   from message import Message
   ```

## **Hot to use**

1. import related classes:
   ```
   from subscribe import Subscribe
   from message import Message
   ```
2. get instance and call corresponding method:   
   ```
   paths = [
        {
            "path": "huawei-debug:debug/cpu-infos/cpu-info",
            "depth": 1
        }
   ]
   subs = Subscribe(username='XXX', password='XXX', address="XXX", paths=paths)
   subs.dailin()
   ```

3. decode gpb-encoding message:   
   ```
   msg = Message(res.message)
   info, list = msg.decode()
   ```