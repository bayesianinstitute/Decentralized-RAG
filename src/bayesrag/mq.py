import paho.mqtt.client as mqtt
import time
import json

from bayesrag.retriever import get_context
from bayesrag.constant import RECEVICE_TOPIC
import queue
from loguru import logger
class Mqttclient:
    def __init__(self,collection_name, broker_address="mqtt.eclipseprojects.io", broker_port=1883,replyTopic="",):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.replyTopic=replyTopic  # Topic to which the response will be sent.
        self.reply_queue = queue.Queue()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.collection_name=collection_name
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def on_connect(self,client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        client.subscribe(RECEVICE_TOPIC)
        client.subscribe(self.replyTopic)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        if msg.topic == self.replyTopic:
            self.handle_reply(msg.payload)  
        else :
            self.handle_message(msg.payload)  # Call the function to handle the received message.

    def handle_reply(self, data):
        # Compare each node reponse and take the highest accurancy
        data = json.loads(data)
        logger.warning(f"Queue size {self.reply_queue.qsize()}")
        # Process the reply here.
        # Need Triggered Method so i can send it to receiver so he get reponse information
        self.reply_queue.put(data)


    def handle_message(self,data):
        data = json.loads(data)
        replayTopic=data.get('replay_topic')
        query=data.get('query')
        context,score=get_context(query,self.collection_name)
        
        if context:
            data={"context":context,"score":score}
            self.send_message(replayTopic,data)

    def send_message(self,send_topic,payload:dict):
        payload = json.dumps(payload)  # Convert the payload to JSON string before sending it.
        self.client.publish(send_topic, payload)
        logger.info(f"Sent message: {payload}")
    
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    
    
if __name__ == "__main__":
    client=Mqttclient("mqtt.eclipseprojects.io", 1883,)

    for i in range(10):
        client.send_message("Hello Send Node",{"id":"1"})
        time.sleep(5) # wait 5 seconds before sending the next message

    client.stop() # stop the MQTT client after 10 messages are sent.
