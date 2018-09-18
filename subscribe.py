import time, signal
import paho.mqtt.client as mqtt

client = None
mqtt_looping = False

class mqtt_client_program():
    def __ini__(self,):
        pass
    def on_connect(self,mq, userdata, rc, _):
        # subscribe when connected.
        mq.subscribe("SMG/P5/OA/#")

    def on_message(self,q, userdata, msg):
        print ("topic: %s" % msg.topic)
        print ("payload: %s" % msg.payload.decode('utf8'))
    #    print( "qos: %d" % msg.qos)

    def mqtt_client_thread(self,):
        global client, mqtt_looping
        client_id = "" # If broker asks client ID.
        client = mqtt.Client(client_id=client_id)

        # If broker asks user/password.
        user = ""
        password = ""
        client.username_pw_set(user, password)

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        try:
            client.connect("10.192.245.57", 1883, 60)
        except:
            print( "MQTT Broker is not online. Connect later.")

        mqtt_looping = True
        print ("Looping...")

        #mqtt_loop.loop_forever()
        cnt = 0
        while mqtt_looping:
            client.loop()

            cnt += 1
            if cnt > 20:
                try:
                    client.reconnect() # to avoid 'Broken pipe' error.
                except:
                    time.sleep(1)
                cnt = 0

        print ("quit mqtt thread")
        client.disconnect()

    def stop_all(*args):
        global mqtt_looping
        mqtt_looping = False

if __name__ == '__main__':
    mqtt_client = mqtt_client_program()
    mqtt_client.mqtt_client_thread()

    print ("exit program")
    