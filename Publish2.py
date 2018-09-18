import paho.mqtt.client as mqtt
import time 
import sys
import random
from abc import ABCMeta, abstractmethod




class Extraction_interface():
    @abstractmethod
    def message(self, msg):
        pass

class fft(Extraction_interface):
    def message(self, Data):
        Data = Data +1
        return Data
        
    def method2(self, msg):
        pass
class filter(Extraction_interface):
    def message(self, Data):
        Data = Data +1
        return Data
        
    def method2(self, msg):
        pass
    
    
class Mqtt():  
    
    
# The function after connected with Broker
    def on_Connect(self,client, userdata, flags, rc):
        print ("Connected with result code " + str(rc))
        client.subscribe("Nkfust/Building_F/GS_Lab/Cash")
# The function while publishing MQTT message
    def on_Publish(self, client, userdata, mid):
        print("Publish OK")  

    def on_message(self, mq, userdata, msg):
#        print ("topic: %s" % msg.topic)
        Data = int(msg.payload.decode('utf8'))
        print ("payload: %s" % msg.payload.decode('utf8'))
        
        if msg.payload.decode('utf8') != 0:
            Feature = FM.message(Data)
            #收值~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
#                client.publish("Nkfust/Building_F/GS_Lab/OAO", int(1))
            time.sleep(1)
            client.disconnect()
            time.sleep(1)
            client.reconnect()        
            client.publish("Nkfust/Building_F/GS_Lab/OAO", Feature) # 處理完特徵傳回特徵
            
            
if __name__ == '__main__':
    # Set up call back functions
    mqttfun = Mqtt()
    client = mqtt.Client()
    client.on_connect = mqttfun.on_Connect
    client.on_publish = mqttfun.on_Publish
    client.on_message = mqttfun.on_message
# Connect with Broker
    client.connect("127.0.0.1", 1883, 60)
    client.loop_forever()           
    
     
#