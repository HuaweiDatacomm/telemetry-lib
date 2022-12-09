# **telemetry-sdk**

## **Overview**
Some lib interfaces about telemetry operations for Python Developers.

## **Installation**
### **Prerequisites**

- Python : 3.10

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